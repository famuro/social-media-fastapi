"""Authentication API endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.auth_deps import AuthServiceDependency, OAuth2LoginForm
from app.exceptions.auth_exceptions import InvalidCredentialsError
from app.models.auth import Token

router: APIRouter = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def create_access_token(
    form_data: OAuth2LoginForm,
    auth_service: AuthServiceDependency,
) -> Token:
    """Authenticate a user and return a bearer access token."""

    try:
        return await auth_service.create_token(
            username=form_data.username,
            password=form_data.password,
        )
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
