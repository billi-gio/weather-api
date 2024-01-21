"""Factory for clients for api weather requests."""

from weather_api.config import ApplicationConfig, ClientProvider
from weather_api.weather_requests.clients.weather_clients_folder import (
    openweathermap_client,
    weatherapi_client,
)


def get_weather_client(
    client_provider: ClientProvider = ClientProvider.WEATHERAPI,
) -> openweathermap_client.OpenWeatherMapClient | weatherapi_client.WeatherAPIClient:
    """Return client depending on api provider"""
    if client_provider == ClientProvider.OPENWEATHER:
        configuration = openweathermap_client.ForecastClientConfig(ApplicationConfig.openweather_api_key)  # type: ignore
        return openweathermap_client.OpenWeatherMapClient(configuration)  # type: ignore

    elif client_provider == ClientProvider.WEATHERAPI:
        configuration = weatherapi_client.ForecastClientConfig(ApplicationConfig.weather_api_com_key)  # type: ignore
        return weatherapi_client.WeatherAPIClient(configuration)  # type: ignore

    else:
        raise ValueError(f"Invalid client provider: {client_provider}")
