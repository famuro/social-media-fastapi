"""Persistence operations for users."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User


class UserRepository:
    """Provide database operations for user entities."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session."""

        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Return the user with the given identifier, if one exists."""

        statement = select(User).where(User.id == user_id)

        return await self._session.scalar(statement)

    async def get_by_username(self, username: str) -> User | None:
        """Return the user with the given username, if one exists."""

        statement = select(User).where(User.username == username)

        return await self._session.scalar(statement)

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with the given email address, if one exists."""

        statement = select(User).where(User.email == email)

        return await self._session.scalar(statement)

    async def add(self, user: User) -> User:
        """Add a user to the current transaction and flush pending changes."""

        self._session.add(user)

        # Send pending changes to PostgreSQL without completing the transaction.
        # In the next commit, the service will commit only after the complete workflow succeeds
        await self._session.flush()

        return user
