from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide a reusable FastAPI test client."""

    with TestClient(app) as test_client:
        yield test_client
