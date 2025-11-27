# tests/conftest.py
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
    """
    Create (and later drop) test DB schema once per test session.
    Uses engine.run_sync to execute synchronous metadata.create_all.
    """
    # ensure old file removed
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
    # adjust if your get_current_user returns a model or id;
    # the earlier code expected token: int (user_id), so return an integer user id
    return 1


@pytest.fixture(autouse=True)
def override_dependencies():
    """
    Automatically override app dependencies for every test.
    Tests may choose to change overrides if needed.
    """
    fastapi_app.dependency_overrides[get_db] = override_get_db
    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
async def client():
    """
    Async httpx client using ASGI transport so requests run in-process.
    """
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
