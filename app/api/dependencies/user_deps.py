"""Dependencies for user-related API workflows."""

from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database_deps import DatabaseSession
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_service(session: DatabaseSession) -> UserService:
    """Provide a user service for the current request."""

    repository = UserRepository(session=session)

    return UserService(repository=repository, session=session)


# A FastAPI sub-dependency that depends on the database session dependency
# The users endpoint only needs this dependency
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
