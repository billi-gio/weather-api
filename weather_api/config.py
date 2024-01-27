from functools import lru_cache
from typing import Generator
import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.clients.storage_clients.storage_factory import StorageType
from weather_api.weather_requests.clients.weather_clients.weather_factory import ClientProvider

load_dotenv(find_dotenv())


class ApplicationConfig:
    service: str = "weather-api"
    host: str = "0.0.0.0"
    port: str = "8080"
    openweather_api_key: str = str(os.getenv("API_KEY_OPENWEATHER"))
    weather_api_com_key: str = str(os.getenv("API_KEY_WEATHERAPI"))
    weather_now_provider = ClientProvider.OPENWEATHER
    weather_forecast_provider = ClientProvider.WEATHERAPI
    storage_type = StorageType.DATABASE
    database_url: str | None = "sqlite:///weatherclient.db"


@lru_cache
def load_application_config() -> ApplicationConfig:
    return ApplicationConfig()


config = load_application_config()


def get_db(engine: Engine) -> Generator:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
