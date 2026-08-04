import logging
import socket

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import DatabaseSession
from app.models.health import HealthResponse

logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the current health status of the API.",
)
async def health_check(session: DatabaseSession) -> HealthResponse:
    """Verify that the API is running and can establish a database connection."""

    try:
        await session.execute(text("SELECT 1"))

    except SQLAlchemyError, socket.gaierror:
        logger.exception("Database health check failed")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )

    return HealthResponse(status="healthy", database="connected")
