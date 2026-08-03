from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


def test_health_endpoint_returns_healthy_response(
    client: TestClient,
    mock_database_session: AsyncSession,
) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }


def test_health_endpoint_returns_503_when_database_is_unavailable(
    client: TestClient,
    mock_database_session: AsyncSession,
) -> None:
    mock_database_session.execute.side_effect = SQLAlchemyError("Database unavailable")

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "unhealthy",
            "database": "disconnected",
        }
    }
