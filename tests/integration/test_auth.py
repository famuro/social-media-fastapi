"""PostgreSQL integration tests for authentication workflows."""

import pytest
from httpx2 import AsyncClient

pytestmark = pytest.mark.integration  # explicitly mark every test as an integration test

REGISTER_URL = "/api/v1/users"
TOKEN_URL = "/api/v1/auth/token"
CURRENT_USER_URL = "/api/v1/users/me"


async def test_registered_user_can_log_in_and_access_current_user(
    integration_client: AsyncClient,
) -> None:
    """A registered user should authenticate and access a protected route."""

    registration_payload = {
        "username": "authenticateduser",
        "email": "authenticated@example.com",
        "password": "strong-password",
    }

    registration_response = await integration_client.post(
        REGISTER_URL,
        json=registration_payload,
    )

    assert registration_response.status_code == 201

    login_response = await integration_client.post(
        TOKEN_URL,
        data={
            "username": registration_payload["username"],
            "password": registration_payload["password"],
        },
    )

    assert login_response.status_code == 200

    token_response = login_response.json()

    assert token_response["token_type"] == "bearer"
    assert isinstance(token_response["access_token"], str)
    assert token_response["access_token"]

    current_user_response = await integration_client.get(
        CURRENT_USER_URL,
        headers={
            "Authorization": (f"Bearer {token_response['access_token']}"),
        },
    )

    assert current_user_response.status_code == 200

    current_user = current_user_response.json()

    assert current_user["username"] == registration_payload["username"]
    assert current_user["email"] == registration_payload["email"]
    assert current_user["is_active"] is True
    assert "id" in current_user
    assert "hashed_password" not in current_user


async def test_login_rejects_incorrect_password(
    integration_client: AsyncClient,
) -> None:
    """A registered user should not authenticate with a wrong password."""

    registration_payload = {
        "username": "invalidpassworduser",
        "email": "invalidpassword@example.com",
        "password": "correct-password",
    }

    registration_response = await integration_client.post(
        REGISTER_URL,
        json=registration_payload,
    )

    assert registration_response.status_code == 201

    login_response = await integration_client.post(
        TOKEN_URL,
        data={
            "username": registration_payload["username"],
            "password": "incorrect-password",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json() == {
        "detail": "Invalid username or password.",
    }
    assert login_response.headers["www-authenticate"] == "Bearer"


async def test_current_user_rejects_invalid_access_token(
    integration_client: AsyncClient,
) -> None:
    """A protected route should reject an invalid access token."""

    response = await integration_client.get(
        CURRENT_USER_URL,
        headers={
            "Authorization": "Bearer invalid-access-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials.",
    }
    assert response.headers["www-authenticate"] == "Bearer"
