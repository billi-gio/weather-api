from enum import Enum

from weather_api.config import ApplicationConfig
from weather_api.weather_requests.clients import openweathermap_client, weatherapi_client


class ClientProvider(str, Enum):
    OPENWEATHER = "openweathermap"
    WEATHERAPI = "weatherapi"


def get_weather_client(
    client_provider: ClientProvider = ClientProvider.WEATHERAPI,
) -> openweathermap_client.OpenWeatherClient | weatherapi_client.WeatherAPIClient:
    """Return client depending on api provider"""
    if client_provider == ClientProvider.OPENWEATHER:
        configuration = openweathermap_client.ForecastClientConfig(ApplicationConfig.openweather_api_key)  # type: ignore
        return openweathermap_client.OpenWeatherClient(configuration)  # type: ignore

    elif client_provider == ClientProvider.WEATHERAPI:
        configuration = weatherapi_client.ForecastClientConfig(ApplicationConfig.weather_api_com)  # type: ignore
        return weatherapi_client.WeatherAPIClient(configuration)  # type: ignore

    else:
        raise ValueError(client_provider)
