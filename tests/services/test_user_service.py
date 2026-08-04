"""Tests for the user registration service."""

from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


@pytest.fixture
def mock_repository() -> UserRepository:
    """Provide a mocked user repository."""

    return cast(UserRepository, AsyncMock(spec=UserRepository))


@pytest.fixture
def mock_session() -> AsyncSession:
    """Provide a mocked asynchronous database session."""

    return cast(AsyncSession, AsyncMock(spec=AsyncSession))


@pytest.fixture
def service(mock_repository: UserRepository, mock_session: AsyncSession) -> UserService:
    """Provide a user service with mocked persistence dependencies."""

    return UserService(repository=mock_repository, session=mock_session)


@pytest.fixture
def user_create() -> UserCreate:
    """Provide valid user registration data."""

    return UserCreate(
        username="testuser",
        email="test@example.com",
        password="strong-password",
    )


async def test_register_creates_user_with_hashed_password(
    service: UserService,
    mock_repository: UserRepository,
    mock_session: AsyncSession,
    user_create: UserCreate,
) -> None:
    """Registration should hash the password and persist the new user."""

    mock_repository.get_by_username.return_value = None
    mock_repository.get_by_email.return_value = None
    mock_repository.add.side_effect = lambda user: user

    with patch(
        "app.services.user_service.hash_password",
        return_value="hashed-password",
    ) as mock_hash_password:
        result = await service.register(user_create)

    mock_hash_password.assert_called_once_with("strong-password")

    added_user = mock_repository.add.await_args.args[0]

    assert isinstance(added_user, User)
    assert added_user.username == "testuser"
    assert added_user.email == "test@example.com"
    assert added_user.hashed_password == "hashed-password"
    assert result is added_user

    mock_repository.get_by_username.assert_awaited_once_with("testuser")
    mock_repository.get_by_email.assert_awaited_once_with("test@example.com")
    mock_repository.add.assert_awaited_once_with(added_user)
    mock_session.commit.assert_awaited_once_with()
    mock_session.rollback.assert_not_awaited()


async def test_register_rejects_existing_username(
    service: UserService,
    mock_repository: UserRepository,
    mock_session: AsyncSession,
    user_create: UserCreate,
) -> None:
    """Registration should reject an existing username."""

    existing_user = User(
        username="testuser",
        email="other@example.com",
        hashed_password="hashed-password",
    )
    mock_repository.get_by_username.return_value = existing_user

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await service.register(user_create)

    assert exc_info.value.field == "username"

    mock_repository.get_by_email.assert_not_awaited()
    mock_repository.add.assert_not_awaited()
    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_not_awaited()


async def test_register_rejects_existing_email(
    service: UserService,
    mock_repository: UserRepository,
    mock_session: AsyncSession,
    user_create: UserCreate,
) -> None:
    """Registration should reject an existing email address."""

    existing_user = User(
        username="other-user",
        email="test@example.com",
        hashed_password="hashed-password",
    )

    mock_repository.get_by_username.return_value = None
    mock_repository.get_by_email.return_value = existing_user

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await service.register(user_create)

    assert exc_info.value.field == "email"

    mock_repository.add.assert_not_awaited()
    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_not_awaited()


async def test_register_rolls_back_when_database_rejects_user(
    service: UserService,
    mock_repository: UserRepository,
    mock_session: AsyncSession,
    user_create: UserCreate,
) -> None:
    """Registration should roll back a rejected database transaction."""

    mock_repository.get_by_username.return_value = None
    mock_repository.get_by_email.return_value = None
    mock_repository.add.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("Unique constraint violation"),
    )

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await service.register(user_create)

    assert exc_info.value.field is None

    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_awaited_once_with()


async def test_register_propagates_unexpected_repository_errors(
    service: UserService,
    mock_repository: UserRepository,
    mock_session: AsyncSession,
    user_create: UserCreate,
) -> None:
    """Registration should not disguise unexpected failures."""

    mock_repository.get_by_username.return_value = None
    mock_repository.get_by_email.return_value = None
    mock_repository.add.side_effect = RuntimeError("Unexpected failure")

    with pytest.raises(RuntimeError, match="Unexpected failure"):
        await service.register(user_create)

    # Mocking no duplicate username or email to isolate an unexpected adding failure
    # Session should not commit
    mock_repository.get_by_username.assert_awaited_once_with(user_create.username)
    mock_repository.get_by_email.assert_awaited_once_with(user_create.email)
    mock_repository.add.assert_awaited_once()

    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_not_awaited()
