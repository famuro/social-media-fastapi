"""Tests for the user repository."""

from typing import cast
from unittest.mock import AsyncMock
from uuid import uuid7

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


@pytest.fixture
def mock_session() -> AsyncSession:
    """Provide a mocked asynchronous database session."""

    return cast(
        AsyncSession,
        AsyncMock(spec=AsyncSession),
    )


@pytest.fixture
def repository(mock_session: AsyncSession) -> UserRepository:
    """Provide a user repository backed by the mocked session."""

    return UserRepository(mock_session)


@pytest.fixture
def user() -> User:
    """Provide a reusable user entity."""

    return User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
    )


async def test_get_by_id_returns_matching_user(
    repository: UserRepository,
    mock_session: AsyncSession,
    user: User,
) -> None:
    """The repository should return the session's identifier query result."""

    mock_session.scalar.return_value = user
    user_id = uuid7()

    result = await repository.get_by_id(user_id)

    assert result is user
    mock_session.scalar.assert_awaited_once()


async def test_get_by_id_returns_none_when_user_does_not_exist(
    repository: UserRepository,
    mock_session: AsyncSession,
) -> None:
    """The repository should return None when no identifier matches."""

    mock_session.scalar.return_value = None

    result = await repository.get_by_id(uuid7())

    assert result is None
    mock_session.scalar.assert_awaited_once()


async def test_get_by_username_returns_matching_user(
    repository: UserRepository,
    mock_session: AsyncSession,
    user: User,
) -> None:
    """The repository should return the session's username query result."""

    mock_session.scalar.return_value = user

    result = await repository.get_by_username("testuser")

    assert result is user
    mock_session.scalar.assert_awaited_once()


async def test_get_by_username_returns_none_when_user_does_not_exist(
    repository: UserRepository,
    mock_session: AsyncSession,
) -> None:
    """The repository should return None when no username matches."""

    mock_session.scalar.return_value = None

    result = await repository.get_by_username("missing-user")

    assert result is None
    mock_session.scalar.assert_awaited_once()


async def test_get_by_email_returns_matching_user(
    repository: UserRepository,
    mock_session: AsyncSession,
    user: User,
) -> None:
    """The repository should return the session's email query result."""

    mock_session.scalar.return_value = user

    result = await repository.get_by_email("test@example.com")

    assert result is user
    mock_session.scalar.assert_awaited_once()


async def test_get_by_email_returns_none_when_user_does_not_exist(
    repository: UserRepository,
    mock_session: AsyncSession,
) -> None:
    """The repository should return None when no email address matches."""

    mock_session.scalar.return_value = None

    result = await repository.get_by_email("missing@example.com")

    assert result is None
    mock_session.scalar.assert_awaited_once()


async def test_add_stages_and_flushes_user(
    repository: UserRepository,
    mock_session: AsyncSession,
    user: User,
) -> None:
    """Adding a user should stage and flush it without committing."""

    result = await repository.add(user)

    assert result is user
    mock_session.add.assert_called_once_with(user)
    mock_session.flush.assert_awaited_once_with()
    mock_session.commit.assert_not_awaited()
