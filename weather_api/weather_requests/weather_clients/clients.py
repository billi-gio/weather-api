from enum import Enum

from weather_api.config import ApplicationConfig
from weather_api.weather_requests.weather_clients import weatherapi_client, weatherclient


class ClientType(str, Enum):
    NOW = "now"
    FORECAST = "forecast"
    WEATHERAPICOM = "weatherapi.com"


def get_client(
    client_type: str,
) -> (
    weatherclient.OneDayForecastClient
    | weatherapi_client.WeatherForecast
    | weatherapi_client.WeatherNow
):
    configuration = weatherapi_client.ForecastClientConfig(ApplicationConfig.weather_api_com)
    if client_type == ClientType.NOW:
        configuration = weatherclient.ForecastClientConfig(ApplicationConfig.openweather_api_key)  # type: ignore
        return weatherclient.OneDayForecastClient(configuration)  # type: ignore
    elif client_type == ClientType.FORECAST:
        return weatherapi_client.WeatherForecast(configuration)
    elif client_type == ClientType.WEATHERAPICOM:
        return weatherapi_client.WeatherNow(configuration)
    else:
        raise ValueError(client_type)
