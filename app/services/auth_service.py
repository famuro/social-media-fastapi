"""Business workflows for user authentication."""

from app.core.security import verify_password
from app.core.tokens import create_access_token, decode_access_token
from app.exceptions.auth_exceptions import InvalidCredentialsError, InvalidTokenError
from app.models.auth import Token, TokenPayload
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    """Authenticate users and issue access tokens."""

    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with its user repository."""

        self._repository = repository

    async def authenticate(self, username: str, password: str) -> User:
        """Validate credentials and return the authenticated user."""

        user: User | None = await self._repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError()

        return user

    async def create_token(self, username: str, password: str) -> Token:
        """Authenticate a user and issue a bearer access token."""

        user: User = await self.authenticate(username=username, password=password)

        access_token: str = create_access_token(subject=user.id)

        return Token(access_token=access_token)

    async def authenticate_token(self, token: str) -> User:
        """Validate an access token and return its active user."""

        payload: TokenPayload = decode_access_token(token)
        user: User | None = await self._repository.get_by_id(payload.subject)

        if user is None or not user.is_active:
            raise InvalidTokenError()

        return user
