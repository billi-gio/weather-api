"""Factory for clients for api weather requests."""

from enum import Enum

from weather_api.weather_requests.clients.weather_clients import (
    openweathermap_client,
    weatherapi_client,
)
import weather_api.config as config


class ClientProvider(str, Enum):
    OPENWEATHER = "openweathermap"
    WEATHERAPI = "weatherapi"


def get_weather_client(
    client_provider: ClientProvider = ClientProvider.WEATHERAPI,
) -> openweathermap_client.OpenWeatherMapClient | weatherapi_client.WeatherAPIClient:
    """Return client depending on api provider"""
    if client_provider == ClientProvider.OPENWEATHER:
        configuration = openweathermap_client.ForecastClientConfig(
            config.ApplicationConfig.openweather_api_key
        )
        return openweathermap_client.OpenWeatherMapClient(configuration)

    elif client_provider == ClientProvider.WEATHERAPI:
        configuration = weatherapi_client.ForecastClientConfig(
            config.ApplicationConfig.weather_api_com_key
        )
        return weatherapi_client.WeatherAPIClient(configuration)

    else:
        raise ValueError(f"{client_provider} is not a valid provider.")
