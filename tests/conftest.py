from collections.abc import AsyncGenerator, Generator
from typing import cast
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.user_deps import get_user_service
from app.db.session import get_session
from app.main import app
from app.services.user_service import UserService


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide a reusable FastAPI test client."""

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> Generator[None]:
    """Reset FastAPI dependency overrides after each test."""

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def mock_database_session() -> AsyncSession:
    """Provide a mocked database session."""

    session: AsyncSession = cast(AsyncSession, AsyncMock(spec=AsyncSession))

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = override_get_session

    return session


@pytest.fixture
def mock_user_service() -> UserService:
    """Override the user service with an isolated mock."""

    service: UserService = cast(UserService, AsyncMock(spec=UserService))

    def override_get_user_service() -> UserService:
        return service

    app.dependency_overrides[get_user_service] = override_get_user_service

    return service
