from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from weather_api.app import create_app


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    app = create_app()

    return TestClient(app)
