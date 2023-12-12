from functools import lru_cache
import os


class ApplicationConfig:
    service: str = "weather-api"
    host: str = "0.0.0.0"
    port: str = "8080"
    api_key = str(os.getenv("API_KEY"))


@lru_cache
def load_application_config() -> ApplicationConfig:
    return ApplicationConfig()


config = load_application_config()
