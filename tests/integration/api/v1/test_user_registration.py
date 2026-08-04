"""Integration tests for user registration."""

import pytest
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import verify_password
from app.models.user import User

pytestmark = pytest.mark.integration  # explicitly mark every test as an integration test

REGISTER_USER_URL = "/api/v1/users"


async def test_register_user_persists_user_with_hashed_password(
    integration_client: AsyncClient,
    integration_session: AsyncSession,
) -> None:
    """Registration should persist a user without storing plaintext."""

    response = await integration_client.post(
        REGISTER_USER_URL,
        json={
            "username": "integration-user",
            "email": "integration@example.com",
            "password": "strong-password",
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["username"] == "integration-user"
    assert response_data["email"] == "integration@example.com"
    assert response_data["is_active"] is True
    assert "password" not in response_data
    assert "hashed_password" not in response_data

    statement = select(User).where(User.username == "integration-user")
    stored_user = await integration_session.scalar(statement)

    assert stored_user is not None
    assert stored_user.email == "integration@example.com"
    assert stored_user.hashed_password != "strong-password"
    assert (
        verify_password(
            "strong-password",
            stored_user.hashed_password,
        )
        is True
    )


async def test_register_user_rejects_duplicate_username(
    integration_client: AsyncClient,
) -> None:
    """Registration should reject a username already stored in PostgreSQL."""

    first_response = await integration_client.post(
        REGISTER_USER_URL,
        json={
            "username": "duplicate-user",
            "email": "first@example.com",
            "password": "strong-password",
        },
    )

    duplicate_response = await integration_client.post(
        REGISTER_USER_URL,
        json={
            "username": "duplicate-user",
            "email": "second@example.com",
            "password": "another-password",
        },
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {
        "detail": "A user with that username already exists.",
    }


async def test_register_user_rejects_duplicate_email(
    integration_client: AsyncClient,
) -> None:
    """Registration should reject an email already stored in PostgreSQL."""

    first_response = await integration_client.post(
        REGISTER_USER_URL,
        json={
            "username": "first-user",
            "email": "duplicate@example.com",
            "password": "strong-password",
        },
    )

    duplicate_response = await integration_client.post(
        REGISTER_USER_URL,
        json={
            "username": "second-user",
            "email": "duplicate@example.com",
            "password": "another-password",
        },
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {
        "detail": "A user with that email already exists.",
    }
