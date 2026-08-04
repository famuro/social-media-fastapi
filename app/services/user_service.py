"""Business workflows for users."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class UserService:
    """Coordinate user-related business workflows."""

    def __init__(self, repository: UserRepository, session: AsyncSession) -> None:
        """Initialize the service with its persistence dependencies."""

        self._repository = repository
        self._session = session

    async def register(self, user_create: UserCreate) -> User:
        """Register and persist a new user.

        Raises:
            UserAlreadyExistsError: If the username or email is already used.
        """

        existing_username = await self._repository.get_by_username(user_create.username)
        if existing_username is not None:
            raise UserAlreadyExistsError(field="username")

        existing_email = await self._repository.get_by_email(user_create.email)
        if existing_email is not None:
            raise UserAlreadyExistsError(field="email")

        user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
        )

        try:
            created_user = await self._repository.add(user)
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()

            raise UserAlreadyExistsError() from error

        return created_user
