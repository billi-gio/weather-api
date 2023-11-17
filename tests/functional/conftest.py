from fastapi.testclient import TestClient
import pytest

from weather_api.app import create_app


@pytest.fixture(scope="session")
def test_client(application_config) -> TestClient:
    app = create_app()
    return TestClient(app)
