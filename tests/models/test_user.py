"""Tests for user model definitions."""

from datetime import UTC
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel

from app.models.user import User, UserCreate, UserPublic


def test_user_generates_uuid_and_utc_timestamps() -> None:
    """User instances should receive application-generated identity fields."""

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
    )

    assert isinstance(user.id, UUID)
    assert user.created_at.tzinfo is UTC
    assert user.updated_at.tzinfo is UTC


def test_user_defaults_to_active_non_superuser() -> None:
    """New users should receive safe account defaults."""

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
    )

    assert user.is_active is True
    assert user.is_superuser is False


def test_user_table_is_registered_in_sqlmodel_metadata() -> None:
    """The persisted user model should register the expected database table."""

    assert "users" in SQLModel.metadata.tables

    users_table = SQLModel.metadata.tables["users"]

    assert users_table.primary_key.name == "pk_users"


def test_user_fields_have_named_unique_constraints() -> None:
    """Username and email uniqueness should use deterministic constraint names."""

    users_table = SQLModel.metadata.tables["users"]

    unique_constraint_names = {
        constraint.name
        for constraint in users_table.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert unique_constraint_names == {
        "uq_users_email",
        "uq_users_username",
    }


def test_user_create_accepts_plaintext_password() -> None:
    """Registration input should accept a password without exposing its hash."""

    user_create = UserCreate(
        username="testuser",
        email="test@example.com",
        password="strong-password",
    )

    assert user_create.password == "strong-password"
    assert not hasattr(user_create, "hashed_password")


def test_user_public_does_not_expose_password_fields() -> None:
    """Public user representations should never contain password data."""

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
    )

    public_user = UserPublic.model_validate(user)

    public_data = public_user.model_dump()

    assert "password" not in public_data
    assert "hashed_password" not in public_data
