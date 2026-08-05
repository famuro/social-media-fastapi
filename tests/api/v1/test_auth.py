"""Tests for authentication API endpoints."""

from fastapi import status
from fastapi.testclient import TestClient

from app.exceptions.auth_exceptions import InvalidCredentialsError
from app.models.auth import Token
from app.services.auth_service import AuthService

TOKEN_URL: str = "/api/v1/auth/token"


def test_create_access_token_returns_bearer_token(
    client: TestClient,
    mock_auth_service: AuthService,
) -> None:
    """Valid credentials should return an access token."""

    mock_auth_service.create_token.return_value = Token(
        access_token="signed-access-token",
    )

    response = client.post(
        TOKEN_URL,
        data={
            "username": "testuser",
            "password": "correct-password",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": "signed-access-token",
        "token_type": "bearer",
    }

    mock_auth_service.create_token.assert_awaited_once_with(
        username="testuser",
        password="correct-password",
    )


def test_create_access_token_rejects_invalid_credentials(
    client: TestClient,
    mock_auth_service: AuthService,
) -> None:
    """Invalid credentials should return an authentication failure."""

    mock_auth_service.create_token.side_effect = InvalidCredentialsError()

    response = client.post(
        TOKEN_URL,
        data={
            "username": "testuser",
            "password": "incorrect-password",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid username or password."}
    assert response.headers["www-authenticate"] == "Bearer"

    mock_auth_service.create_token.assert_awaited_once_with(
        username="testuser",
        password="incorrect-password",
    )


def test_create_access_token_requires_username(
    client: TestClient,
    mock_auth_service: AuthService,
) -> None:
    """Login should require the OAuth2 username field."""

    response = client.post(
        TOKEN_URL,
        data={
            "password": "correct-password",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    mock_auth_service.create_token.assert_not_awaited()


def test_create_access_token_requires_password(
    client: TestClient,
    mock_auth_service: AuthService,
) -> None:
    """Login should require the OAuth2 password field."""

    response = client.post(
        TOKEN_URL,
        data={
            "username": "testuser",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    mock_auth_service.create_token.assert_not_awaited()


def test_create_access_token_rejects_json_credentials(
    client: TestClient,
    mock_auth_service: AuthService,
) -> None:
    """The OAuth2 token endpoint should require form data."""

    response = client.post(
        TOKEN_URL,
        json={
            "username": "testuser",
            "password": "correct-password",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    mock_auth_service.create_token.assert_not_awaited()
