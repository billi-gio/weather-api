from weather_api.config import ApplicationConfig
from weather_api.weather_requests import weatherclient


def get_client(
    forecast_length: str,
) -> weatherclient.OneDayForecastClient | weatherclient.LongTermForecastClient:
    configuration = weatherclient.ForecastClientConfig(ApplicationConfig.api_key)
    if forecast_length == "now":
        return weatherclient.OneDayForecastClient(configuration)
    elif forecast_length == "forecast":
        return weatherclient.LongTermForecastClient(configuration)
    else:
        raise ValueError(forecast_length)
