import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from weather_api.app import create_app
from weather_api.weather_requests.weather_models import Table


class DummyDayForecast:
    date: datetime = datetime.datetime(
        2023, 12, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
    )
    temperature: str = 0.0
    weather_conditions: str = "dummy"
    city_name: str = "dummy"
    country: str = "dummy"
    wind_speed: float = 0.0
    humidity: float = 0.0


@pytest.fixture(scope="module")
def dummy_day_forecast():
    return DummyDayForecast


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    app = create_app()

    return TestClient(app)


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Table.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
