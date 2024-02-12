from unittest.mock import patch

from pytest import raises

from weather_api.weather_requests.clients.storage_clients.storage_clients import DBStorageClient
from weather_api.weather_requests.clients.weather_clients import openweathermap_client
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.service_handler import (
    NonexistentCountry,
    get_request_helper,
    weather_endpoint_handler,
)


@patch(
    "weather_api.weather_requests.clients.weather_clients.openweathermap_client.OpenWeatherMapClient.get_current_weather"
)
def test_weather_service_handler(dummy_onedayforecast_client, dummy_day_forecast):
    city_name = "who cares"
    country_code = "PT"

    dummy_onedayforecast_client.return_value = [dummy_day_forecast]

    response = weather_endpoint_handler(
        client=openweathermap_client.OpenWeatherMapClient,
        city_name=city_name,
        country_code=country_code,
    )

    assert [
        WeatherResponseSchema(
            date=dummy_day_forecast.date,
            weather_conditions=dummy_day_forecast.weather_conditions,
            temperature=dummy_day_forecast.temperature,
            wind_speed=dummy_day_forecast.wind_speed,
            humidity=dummy_day_forecast.humidity,
            city_name=dummy_day_forecast.city_name,
            country=dummy_day_forecast.country,
        )
    ] == response


def test_service_handler_with_nonexistant_country():
    city_name = "who cares"
    country_code = "Nope"
    client = "not_important"

    expected_result = NonexistentCountry

    with raises(NonexistentCountry) as err:
        weather_endpoint_handler(client=client, city_name=city_name, country_code=country_code)
    assert err.type == expected_result


@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
def test_get_request_helper_return(dummy_weather_handler, override_get_engine, dummy_day_forecast):
    city_name = "who cares"
    country_code = "IT"
    weather_client = "not important"
    storage_client = DBStorageClient(override_get_engine)

    dummy_weather_handler.return_value = [
        WeatherResponseSchema(
            date=dummy_day_forecast.date,
            weather_conditions=dummy_day_forecast.weather_conditions,
            temperature=dummy_day_forecast.temperature,
            wind_speed=dummy_day_forecast.wind_speed,
            humidity=dummy_day_forecast.humidity,
            city_name=dummy_day_forecast.city_name,
            country=dummy_day_forecast.country,
        )
    ]

    response = get_request_helper(weather_client, city_name, country_code, storage_client)

    expected_result = [
        WeatherResponseSchema(
            date=dummy_day_forecast.date,
            weather_conditions=dummy_day_forecast.weather_conditions,
            temperature=dummy_day_forecast.temperature,
            wind_speed=dummy_day_forecast.wind_speed,
            humidity=dummy_day_forecast.humidity,
            city_name=dummy_day_forecast.city_name,
            country=dummy_day_forecast.country,
        )
    ]

    assert response == expected_result
