import pytest

from weather_api.config import load_application_config


@pytest.fixture(scope="session")
def application_config():
    return load_application_config()
