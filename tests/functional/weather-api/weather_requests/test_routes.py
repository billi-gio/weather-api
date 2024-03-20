from unittest.mock import patch

from weather_api.weather_requests.schemas import WeatherResponseSchema


@patch("weather_api.weather_requests.weather_db_engine.get_engine")
@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
def test_weather_now_returns_correct_response(
    dummy_weather_handler,
    engine,
    dummy_day_forecast,
    test_client,
    override_get_engine,
):
    city_name = "who cares"
    country_code = "IT"

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

    engine.return_value = override_get_engine

    response = test_client.get(f"/weather-now/{country_code}/{city_name}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "date": "2023-12-04T00:00:00+01:00",
            "weather_conditions": "dummy",
            "temperature": 0.0,
            "wind_speed": 0.0,
            "humidity": 0.0,
            "city_name": "dummy",
            "country": "dummy",
        }
    ]


@patch("weather_api.weather_requests.weather_db_engine.get_engine")
@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
def test_weatherforecast_returns_correct_response(
    dummy_weather_handler,
    engine,
    dummy_day_forecast,
    test_client,
    override_get_engine,
):
    city_name = "who cares"
    country_code = "IT"

    dummy_weather_handler.return_value = [
        WeatherResponseSchema(
            date=dummy_day_forecast.date,
            weather_conditions=dummy_day_forecast.weather_conditions,
            temperature=dummy_day_forecast.temperature,
            wind_speed=dummy_day_forecast.wind_speed,
            humidity=dummy_day_forecast.humidity,
            city_name=dummy_day_forecast.city_name,
            country=dummy_day_forecast.country,
        ),
        WeatherResponseSchema(
            date=dummy_day_forecast.date,
            weather_conditions=dummy_day_forecast.weather_conditions,
            temperature=dummy_day_forecast.temperature,
            wind_speed=dummy_day_forecast.wind_speed,
            humidity=dummy_day_forecast.humidity,
            city_name=dummy_day_forecast.city_name,
            country=dummy_day_forecast.country,
        ),
    ]
    engine.return_value = override_get_engine

    response = test_client.get(f"/weather-forecast/{country_code}/{city_name}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "date": "2023-12-04T00:00:00+01:00",
            "weather_conditions": "dummy",
            "temperature": 0.0,
            "wind_speed": 0.0,
            "humidity": 0.0,
            "city_name": "dummy",
            "country": "dummy",
        },
        {
            "date": "2023-12-04T00:00:00+01:00",
            "weather_conditions": "dummy",
            "temperature": 0.0,
            "wind_speed": 0.0,
            "humidity": 0.0,
            "city_name": "dummy",
            "country": "dummy",
        },
    ]
