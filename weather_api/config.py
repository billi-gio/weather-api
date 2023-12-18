from functools import lru_cache
from typing import Generator
import os

from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.weather_db_engine import engine


class ApplicationConfig:
    service: str = "weather-api"
    host: str = "0.0.0.0"
    port: str = "8080"
    api_key: str = str(os.getenv("API_KEY_OPENWEATHER"))


@lru_cache
def load_application_config() -> ApplicationConfig:
    return ApplicationConfig()


config = load_application_config()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
