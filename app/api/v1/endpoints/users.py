"""User API endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.user_deps import UserServiceDependency
from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.models.user import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, service: UserServiceDependency) -> UserPublic:
    """Register a new user."""

    try:
        user = await service.register(user_create)
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

    return UserPublic.model_validate(user)
