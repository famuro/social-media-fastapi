"""User API endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.auth_deps import CurrentUser
from app.api.dependencies.user_deps import UserServiceDependency
from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.models.user import User, UserCreate, UserPublic

router: APIRouter = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, service: UserServiceDependency) -> User:
    """Register a new user."""

    try:
        user: User = await service.register(user_create)
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

    return user


@router.get("/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def read_current_user(current_user: CurrentUser) -> User:
    """Return the currently authenticated user."""

    return current_user
