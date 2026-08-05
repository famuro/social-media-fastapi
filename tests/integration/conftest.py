"""Fixtures for integration tests using PostgreSQL."""

import os
import subprocess
from collections.abc import AsyncGenerator, Generator

import pytest
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.db.session import get_session
from app.main import app


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Return and validate the dedicated integration-test database URL."""

    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.fail("TEST_DATABASE_URL must be configured before running integration tests.")

    parsed_url = make_url(database_url)
    database_name = parsed_url.database

    if database_name is None or "test" not in database_name.lower():
        pytest.fail(
            "Integration tests must use a database whose name contains "
            "'test'. Refusing to run against a non-test database."
        )

    return database_url


@pytest.fixture(scope="session", autouse=True)
def apply_test_migrations(test_database_url: str) -> Generator[None]:
    """Apply all Alembic migrations to the integration-test database."""

    migration_environment = {
        **os.environ,
        "DATABASE_URL": test_database_url,
    }

    subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        check=True,
        env=migration_environment,
    )

    yield


@pytest.fixture
async def integration_engine(test_database_url: str) -> AsyncGenerator[AsyncEngine]:
    """Provide a disposable async engine for one integration test."""

    engine = create_async_engine(test_database_url, pool_pre_ping=True)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def integration_session(integration_engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    """Provide a transaction-isolated database session.

    The application may call commit or rollback normally. SQLAlchemy handles
    those operations through save points while the outer transaction remains
    under the test fixture's control.
    """

    async with integration_engine.connect() as connection:
        outer_transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            await session.close()

            if outer_transaction.is_active:
                await outer_transaction.rollback()


@pytest.fixture
async def integration_client(integration_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    """Provide an async API client using the real database-backed service."""

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        yield integration_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_session, None)
