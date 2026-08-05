"""Dependencies for authentication API workflows."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.database_deps import DatabaseSession
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_auth_service(session: DatabaseSession) -> AuthService:
    """Provide an authentication service for the current request."""

    repository = UserRepository(session=session)

    return AuthService(repository=repository)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

OAuth2LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]
