import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.main import create_app
from app.api.v1 import auth as auth_module  # used to override dependency
from httpx import AsyncClient, ASGITransport

def _run_sync(coro):
    """Helper to run an async coroutine from sync fixture context."""
    return asyncio.get_event_loop_policy().new_event_loop().run_until_complete(coro)

@pytest.fixture(scope="session")
def test_db_dir(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("test_db")
    db_path = tmp / "test.db"
    return db_path

@pytest.fixture(scope="session")
def test_engine(test_db_dir):
    """
    Create an async engine and create all tables once for the test session.
    We run the async create_all() using asyncio.run() so this fixture is sync.
    """
    db_url = f"sqlite+aiosqlite:///{test_db_dir}"
    engine = create_async_engine(db_url, future=True, echo=False)

    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # run the coroutine synchronously to create tables
    _run_sync(_create())

    yield engine

    # dispose engine at teardown
    _run_sync(engine.dispose())

@pytest.fixture
def test_sessionmaker(test_engine):
    TestSessionLocal = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return TestSessionLocal

@pytest.fixture
def app_override(test_sessionmaker):
    """
    Create app and override its DB dependency to use the test session factory.
    This fixture can remain sync; it provides an async dependency for endpoints.
    """
    app = create_app()

    async def get_test_db():
        async with test_sessionmaker() as session:
            yield session

    app.dependency_overrides[auth_module.get_db] = get_test_db
    return app

@pytest.fixture
async def async_client(app_override):
    """
    Async fixture used by async tests. Uses ASGITransport so no real network.
    """
    transport = ASGITransport(app=app_override)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
