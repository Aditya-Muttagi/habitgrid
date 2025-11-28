import asyncio
import os
import tempfile
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app as fastapi_app
from app.db.base import Base
from app.db.session import get_db
from app.api.v1.habits import get_current_user

# Use a temporary SQLite file for reliability across connections
_TMP_DB = os.path.join(tempfile.gettempdir(), "test_habitgrid.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_TMP_DB}"

# Async engine and session factory for tests
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    # Use a module/session-scoped event loop for faster tests
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    try:
        if os.path.exists(_TMP_DB):
            os.remove(_TMP_DB)
    except Exception:
        pass

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # drop tables and remove file
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    try:
        if os.path.exists(_TMP_DB):
            os.remove(_TMP_DB)
    except Exception:
        pass


# override dependency to return an AsyncSession bound to test engine
async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


# override current-user dependency to return a fixed test user id
async def override_get_current_user():
    return 1


@pytest.fixture(autouse=True)
def override_dependencies():
    fastapi_app.dependency_overrides[get_db] = override_get_db
    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# replace current clear_overrides fixture with this
@pytest.fixture
def clear_overrides():
    """
    Clear only auth-related overrides (so we use real authentication flow)
    but retain the DB override so endpoints still use the test DB.
    """
    orig = fastapi_app.dependency_overrides.copy()
    # Keep DB override if present
    db_override = orig.get(get_db)
    # Clear all overrides then restore only the DB override
    fastapi_app.dependency_overrides.clear()
    if db_override is not None:
        fastapi_app.dependency_overrides[get_db] = db_override

    yield

    # restore everything to original
    fastapi_app.dependency_overrides.clear()
    fastapi_app.dependency_overrides.update(orig)
