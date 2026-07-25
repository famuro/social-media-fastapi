from fastapi.testclient import TestClient


def test_health_endpoint_returns_200(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_health_endpoint_returns_expected_response(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.json() == {"status": "healthy"}
