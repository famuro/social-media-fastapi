"""Tests for user API endpoints."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.models.user import User, UserCreate, UserPublic
from app.services.user_service import UserService

REGISTER_USER_URL = "/api/v1/users"

VALID_REGISTRATION_PAYLOAD = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "strong-password",
}


def test_register_user_returns_created_user(
    client: TestClient,
    mock_user_service: UserService,
) -> None:
    """Successful registration should return the public user representation."""

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
    )
    mock_user_service.register.return_value = user

    response = client.post(
        REGISTER_USER_URL,
        json=VALID_REGISTRATION_PAYLOAD,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == UserPublic.model_validate(user).model_dump(mode="json")

    response_data = response.json()

    assert "password" not in response_data
    assert "hashed_password" not in response_data

    registered_user = mock_user_service.register.await_args.args[0]

    assert isinstance(registered_user, UserCreate)
    assert registered_user.username == "testuser"
    assert registered_user.email == "test@example.com"
    assert registered_user.password == "strong-password"


@pytest.mark.parametrize(
    ("field", "expected_detail"),
    [
        (
            "username",
            "A user with that username already exists.",
        ),
        (
            "email",
            "A user with that email already exists.",
        ),
        (
            None,
            "A user with the supplied details already exists.",
        ),
    ],
)
def test_register_user_returns_conflict_for_existing_user(
    client: TestClient,
    mock_user_service: UserService,
    field: str | None,
    expected_detail: str,
) -> None:
    """Duplicate registration should return an HTTP conflict response."""

    mock_user_service.register.side_effect = UserAlreadyExistsError(field=field)

    response = client.post(
        REGISTER_USER_URL,
        json=VALID_REGISTRATION_PAYLOAD,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": expected_detail,
    }


def test_register_user_rejects_invalid_request(
    client: TestClient,
    mock_user_service: UserService,
) -> None:
    """Invalid registration input should fail before reaching the service."""

    response = client.post(
        REGISTER_USER_URL,
        json={
            "username": "ab",
            "email": "test@example.com",
            "password": "short",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    mock_user_service.register.assert_not_awaited()
