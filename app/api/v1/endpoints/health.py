from fastapi import APIRouter, status

from app.schemas.health import HealthResponse

router: APIRouter = APIRouter(prefix="/health", tags=["Health"])


@router.get("",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the current health status of the API.",
)
async def health_check() -> HealthResponse:
    """
    Check API availability.

    This endpoint currently verifies that the application
    process is running. Future iterations may include
    dependency checks such as database connectivity.
    """

    return HealthResponse(status="healthy")
