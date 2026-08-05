"""Tests for authentication business workflows."""

from unittest.mock import patch

import pytest

from app.exceptions.auth_exceptions import InvalidCredentialsError, InvalidTokenError
from app.models.auth import Token, TokenPayload
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


@pytest.fixture
def auth_service(mock_user_repository: UserRepository) -> AuthService:
    """Provide an authentication service with mocked persistence."""

    return AuthService(repository=mock_user_repository)


@pytest.fixture
def active_user() -> User:
    """Provide an active user suitable for authentication tests."""

    return User(
        username="testuser",
        email="test@example.com",
        hashed_password="stored-password-hash",
        is_active=True,
    )


async def test_authenticate_returns_user_for_valid_credentials(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """Valid credentials should return the authenticated user."""

    mock_user_repository.get_by_username.return_value = active_user

    with patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ) as verify_password_mock:
        authenticated_user = await auth_service.authenticate(
            username="testuser",
            password="correct-password",
        )

    assert authenticated_user is active_user

    mock_user_repository.get_by_username.assert_awaited_once_with("testuser")
    verify_password_mock.assert_called_once_with(
        "correct-password",
        active_user.hashed_password,
    )


async def test_authenticate_rejects_unknown_username(
    auth_service: AuthService, mock_user_repository: UserRepository
) -> None:
    """An unknown username should produce a generic credential error."""

    mock_user_repository.get_by_username.return_value = None

    with (
        patch("app.services.auth_service.verify_password") as verify_password_mock,
        pytest.raises(
            InvalidCredentialsError,
            match="Invalid username or password.",
        ),
    ):
        await auth_service.authenticate(
            username="unknown-user",
            password="some-password",
        )

    mock_user_repository.get_by_username.assert_awaited_once_with("unknown-user")
    verify_password_mock.assert_not_called()


async def test_authenticate_rejects_incorrect_password(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """An incorrect password should produce a generic credential error."""

    mock_user_repository.get_by_username.return_value = active_user

    with (
        patch(
            "app.services.auth_service.verify_password",
            return_value=False,
        ) as verify_password_mock,
        pytest.raises(
            InvalidCredentialsError,
            match="Invalid username or password.",
        ),
    ):
        await auth_service.authenticate(
            username="testuser",
            password="incorrect-password",
        )

    mock_user_repository.get_by_username.assert_awaited_once_with("testuser")
    verify_password_mock.assert_called_once_with(
        "incorrect-password",
        active_user.hashed_password,
    )


async def test_authenticate_rejects_inactive_user(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """An inactive user should not be authenticated."""

    active_user.is_active = False
    mock_user_repository.get_by_username.return_value = active_user

    with (
        patch(
            "app.services.auth_service.verify_password",
            return_value=True,
        ),
        pytest.raises(
            InvalidCredentialsError,
            match="Invalid username or password.",
        ),
    ):
        await auth_service.authenticate(
            username="testuser",
            password="correct-password",
        )

    mock_user_repository.get_by_username.assert_awaited_once_with("testuser")


async def test_create_token_returns_bearer_token(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """Valid credentials should produce a signed bearer token."""

    mock_user_repository.get_by_username.return_value = active_user

    with (
        patch(
            "app.services.auth_service.verify_password",
            return_value=True,
        ),
        patch(
            "app.services.auth_service.create_access_token",
            return_value="signed-access-token",
        ) as create_access_token_mock,
    ):
        token = await auth_service.create_token(
            username="testuser",
            password="correct-password",
        )

    assert token == Token(
        access_token="signed-access-token",
        token_type="bearer",
    )

    create_access_token_mock.assert_called_once_with(subject=active_user.id)


async def test_create_token_does_not_issue_token_for_invalid_credentials(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
) -> None:
    """Invalid credentials should never result in token creation."""

    mock_user_repository.get_by_username.return_value = None

    with (
        patch("app.services.auth_service.create_access_token") as create_access_token_mock,
        pytest.raises(InvalidCredentialsError),
    ):
        await auth_service.create_token(
            username="unknown-user",
            password="some-password",
        )

    create_access_token_mock.assert_not_called()


async def test_authenticate_token_returns_active_user(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """A valid token should resolve to its active user."""

    token_payload = TokenPayload(
        subject=active_user.id,
        token_type="access",
    )
    mock_user_repository.get_by_id.return_value = active_user

    with patch(
        "app.services.auth_service.decode_access_token",
        return_value=token_payload,
    ) as mock_decode_access_token:
        result = await auth_service.authenticate_token(
            "signed-access-token",
        )

    assert result is active_user

    mock_decode_access_token.assert_called_once_with(
        "signed-access-token",
    )
    mock_user_repository.get_by_id.assert_awaited_once_with(
        active_user.id,
    )


async def test_authenticate_token_rejects_unknown_user(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """A token for a missing user should be rejected."""

    token_payload = TokenPayload(
        subject=active_user.id,
        token_type="access",
    )
    mock_user_repository.get_by_id.return_value = None

    with patch(
        "app.services.auth_service.decode_access_token",
        return_value=token_payload,
    ):
        with pytest.raises(InvalidTokenError):
            await auth_service.authenticate_token(
                "signed-access-token",
            )

    mock_user_repository.get_by_id.assert_awaited_once_with(
        active_user.id,
    )


async def test_authenticate_token_rejects_inactive_user(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
    active_user: User,
) -> None:
    """A token belonging to an inactive user should be rejected."""

    active_user.is_active = False

    token_payload = TokenPayload(
        subject=active_user.id,
        token_type="access",
    )
    mock_user_repository.get_by_id.return_value = active_user

    with patch(
        "app.services.auth_service.decode_access_token",
        return_value=token_payload,
    ):
        with pytest.raises(InvalidTokenError):
            await auth_service.authenticate_token(
                "signed-access-token",
            )

    mock_user_repository.get_by_id.assert_awaited_once_with(
        active_user.id,
    )


async def test_authenticate_token_propagates_invalid_token_error(
    auth_service: AuthService,
    mock_user_repository: UserRepository,
) -> None:
    """A token decoding failure should remain an authentication error."""

    with patch(
        "app.services.auth_service.decode_access_token",
        side_effect=InvalidTokenError(),
    ):
        with pytest.raises(InvalidTokenError):
            await auth_service.authenticate_token(
                "invalid-access-token",
            )

    mock_user_repository.get_by_id.assert_not_awaited()
