import pycountry

from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    DBStorageClient,
)
from weather_api.weather_requests.clients.weather_clients import (
    openweathermap_client,
    weatherapi_client,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.storage_handlers import storage_handler


class NonexistentCountry(Exception):
    pass


def get_request_helper(
    weather_client: openweathermap_client.OpenWeatherMapClient
    | weatherapi_client.WeatherAPIClient,
    city_name: str,
    country_code: str,
    storage_client: DBStorageClient | CSVStorageClient,
    days: int | None = None,
) -> list[WeatherResponseSchema]:
    """Helper for endpoints to get the request and check if empty.
    Also send request to storage handler."""
    request: list = weather_endpoint_handler(weather_client, city_name, country_code, days)

    storage_handler(storage_client, request)

    return request


def weather_endpoint_handler(
    client: openweathermap_client.OpenWeatherMapClient | weatherapi_client.WeatherAPIClient,
    city_name: str,
    country_code: str,
    days: int | None = None,
) -> list[WeatherResponseSchema]:
    """Checks country code correctness.
    Then call the weather client methods for now and forecast.
    """
    try:
        pycountry.countries.get(alpha_2=country_code).name
    except AttributeError:
        raise NonexistentCountry(
            f"""{country_code} is not valid.
            Please refer to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2."""
        )

    if days:
        request = client.get_long_weather_forecast(city_name, country_code, days)
    else:
        request = client.get_current_weather(city_name, country_code)

    days_forecast_list = []
    for entry in request:
        days_forecast_list.append(
            WeatherResponseSchema(
                date=entry.date,
                weather_conditions=entry.weather_conditions,
                temperature=entry.temperature,
                wind_speed=entry.wind_speed,
                humidity=entry.humidity,
                city_name=entry.city_name,
                country=entry.country,
            )
        )

    return days_forecast_list
