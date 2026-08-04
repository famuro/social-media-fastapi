"""Shared configuration and fields for database table models."""

from datetime import UTC, datetime
from uuid import UUID, uuid7

from sqlalchemy import DateTime, MetaData, func
from sqlmodel import Field, SQLModel

NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": ("fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s"),
    "pk": "pk_%(table_name)s",
}

# Replace SQLModel's default metadata before importing any table models.
# This gives indexes and constraints deterministic, readable names that
# Alembic can safely reference in generated migrations.
SQLModel.metadata = MetaData(naming_convention=NAMING_CONVENTION)


def utc_now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""

    return datetime.now(UTC)


class TableBase(SQLModel):
    """Provide fields shared by all persisted application entities.

    This class does not declare ``table=True`` and therefore does not create
    its own database table. Concrete table models inherit these fields.
    """

    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )
