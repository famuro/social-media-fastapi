"""Dependencies for authentication API workflows."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.api.dependencies.database_deps import DatabaseSession
from app.exceptions import InvalidTokenError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_auth_service(session: DatabaseSession) -> AuthService:
    """Provide an authentication service for the current request."""

    repository = UserRepository(session=session)

    return AuthService(repository=repository)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

OAuth2LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
AccessToken = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: AccessToken, auth_service: AuthServiceDependency) -> User:
    """Return the user represented by a valid bearer token."""

    try:
        return await auth_service.authenticate_token(token)
    except InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error


CurrentUser = Annotated[User, Depends(get_current_user)]
