"""User database and API models."""

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict
from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel

from app.models.base import TableBase

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 50
EMAIL_MAX_LENGTH = 320
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128


class UserBase(SQLModel):
    """Define user fields shared across table and API models."""

    username: str = Field(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
    )
    email: str = Field(
        min_length=3,
        max_length=EMAIL_MAX_LENGTH,
    )


class User(TableBase, UserBase, table=True):
    """Represent a persisted application user."""

    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            f"char_length(username) >= {USERNAME_MIN_LENGTH}",
            name="username_min_length",
        ),
    )

    username: str = Field(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        nullable=False,
        unique=True,
    )
    email: str = Field(
        min_length=3,
        max_length=EMAIL_MAX_LENGTH,
        nullable=False,
        unique=True,
    )
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
    )
    is_active: bool = Field(
        default=True,
        nullable=False,
    )
    is_superuser: bool = Field(
        default=False,
        nullable=False,
    )


class UserCreate(UserBase):
    """Validate the data accepted when registering a user."""

    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


class UserPublic(UserBase):
    """Define the safe user data to return through the API."""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(SQLModel):
    """Validate fields accepted by a partial user update."""

    username: str | None = Field(
        default=None,
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
    )

    email: str | None = Field(
        default=None,
        min_length=3,
        max_length=EMAIL_MAX_LENGTH,
    )

    password: str | None = Field(
        default=None,
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
