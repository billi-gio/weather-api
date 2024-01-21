import pycountry

from weather_api.weather_requests.clients.storage_clients_folder.storage_clients import (
    DBStorageClient,
)
from weather_api.weather_requests.clients.weather_clients_folder import (
    openweathermap_client,
    weatherapi_client,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.weather_models import City, WeatherRequest


def get_request_helper(
    weather_client: openweathermap_client.OpenWeatherMapClient
    | weatherapi_client.WeatherAPIClient,
    city_name: str,
    country_code: str,
    storage_client: DBStorageClient,
    days: int | None = None,
) -> list[WeatherResponseSchema]:
    """Helper for endpoints to get the request and check if empty.
    Also send request to storage handler."""
    if days:
        request = weather_endpoint_handler(weather_client, city_name, country_code, days)
    else:
        request = weather_endpoint_handler(weather_client, city_name, country_code)

    if not request:
        raise IndexError

    storage_handler(storage_client, request)

    return request


def weather_endpoint_handler(
    client: openweathermap_client.OpenWeatherMapClient | weatherapi_client.WeatherAPIClient,
    city_name: str,
    country_code: str,
    days: int | None = None,
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url and 2 letters country code as a url parameter.
    returns the weather results from selected weather client."""

    pycountry.countries.get(alpha_2=country_code).name

    if days:
        request = client.get_long_weather_forecast(city_name, country_code, days)  # type: ignore
    else:
        request = client.get_current_weather(city_name, country_code)  # type: ignore

    days_forecast_list = []
    for entry in request:  # type: ignore
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


def storage_handler(client: DBStorageClient, data: list[WeatherResponseSchema]) -> None:
    """From data list, create a db storage client, checks for existing city entries in db,
    finally send a list to the client to save in db."""
    data_to_add_to_db = []

    city_entry = client.read(
        model=City, filter={"city_name": data[0].city_name, "country": data[0].country}
    )

    if not city_entry:
        city_entry = City(
            country=data[0].country,
            city_name=data[0].city_name,
        )
        data_to_add_to_db.append(city_entry)
    else:
        city_entry = city_entry[0]

    for dayforecast in data:
        weather = WeatherRequest(
            date=dayforecast.date,
            weather_conditions=dayforecast.weather_conditions,
            temperature=dayforecast.temperature,
            wind_speed=dayforecast.wind_speed,
            humidity=dayforecast.humidity,
        )
        weather.city = city_entry  # type: ignore

        data_to_add_to_db.append(weather)

    client.save(data_to_add_to_db)
