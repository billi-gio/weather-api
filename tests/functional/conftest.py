from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
import pytest

from weather_api.app import create_app


@pytest.fixture(scope="session")
def test_client(application_config) -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope="session")
def test_engine():
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    return engine
