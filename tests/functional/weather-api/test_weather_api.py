import datetime

from mock import patch
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.routes import get_db
from weather_api.weather_requests.weather_requests_database import Table
from weather_api.weather_requests.weatherclient import DayForecast, LongTermForecastClient


class DummyDayForecast:
    date: datetime = "2023-12-04 12:56:54+01:00"
    temperature: str = 0.0
    weather_conditions: str = "dummy"
    city: str = "dummy"
    country: str = "dummy"
    sunrise: datetime = "2023-12-04 12:56:54+01:00"
    sunset: datetime = "2023-12-04 12:56:54+01:00"


@patch("weather_api.weather_requests.weatherclient.OneDayForecastClient.get_weather_forecast")
def test_weather_now_returns_correct_response(dummy_onedayforecast_client, test_client):
    city_name = "who cares"

    dummy_onedayforecast_client.return_value = DummyDayForecast

    response = test_client.get(f"/weather-now/{city_name}")

    assert response.status_code == 200
    assert response.json() == {
        "weather_conditions": "dummy",
        "temperature": 0.0,
        "sunrise": "2023-12-04T12:56:54+01:00",
        "sunset": "2023-12-04T12:56:54+01:00",
    }


@patch("weather_api.weather_requests.weatherclient.LongTermForecastClient.get_weather_forecast")
def test_weatherforecast_returns_correct_response(dummy_longforecast_client, test_client):
    city_name = "who cares"

    ls = []
    ls.append(DummyDayForecast)
    dummy_longforecast_client.return_value = ls

    response = test_client.get(f"/weather-forecast/{city_name}")

    assert response.status_code == 200
    assert response.json() == {
        "weather_conditions": "dummy",
        "temperature": 0.0,
        "sunrise": "2023-12-04T12:56:54+01:00",
        "sunset": "2023-12-04T12:56:54+01:00",
    }


def test_14_day_forecast():
    data = {
        "city": {
            "id": 3163858,
            "name": "Zocca",
            "coord": {"lon": 10.99, "lat": 44.34},
            "country": "IT",
            "population": 4593,
            "timezone": 7200,
        },
        "cod": "200",
        "message": 0.0582563,
        "cnt": 7,
        "list": [
            {
                "dt": 1661857200,
                "sunrise": 1661834187,
                "sunset": 1661882248,
                "temp": {
                    "day": 299.66,
                    "min": 288.93,
                    "max": 299.66,
                    "night": 290.31,
                    "eve": 297.16,
                    "morn": 288.93,
                },
                "feels_like": {
                    "day": 299.66,
                    "night": 290.3,
                    "eve": 297.1,
                    "morn": 288.73,
                },
                "pressure": 1017,
                "humidity": 44,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d",
                    }
                ],
                "speed": 2.7,
                "deg": 209,
                "gust": 3.58,
                "clouds": 53,
                "pop": 0.7,
                "rain": 2.51,
            },
            {
                "dt": 1661943600,
                "sunrise": 1661920656,
                "sunset": 1661968542,
                "temp": {
                    "day": 295.76,
                    "min": 287.73,
                    "max": 295.76,
                    "night": 289.37,
                    "eve": 292.76,
                    "morn": 287.73,
                },
                "feels_like": {
                    "day": 295.64,
                    "night": 289.45,
                    "eve": 292.97,
                    "morn": 287.59,
                },
                "pressure": 1014,
                "humidity": 60,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d",
                    }
                ],
                "speed": 2.29,
                "deg": 215,
                "gust": 3.27,
                "clouds": 66,
                "pop": 0.82,
                "rain": 5.32,
            },
            {
                "dt": 1662030000,
                "sunrise": 1662007126,
                "sunset": 1662054835,
                "temp": {
                    "day": 293.38,
                    "min": 287.06,
                    "max": 293.38,
                    "night": 287.06,
                    "eve": 289.01,
                    "morn": 287.84,
                },
                "feels_like": {
                    "day": 293.31,
                    "night": 287.01,
                    "eve": 289.05,
                    "morn": 287.85,
                },
                "pressure": 1014,
                "humidity": 71,
                "weather": [
                    {
                        "id": 500,
                        "main": "Rain",
                        "description": "light rain",
                        "icon": "10d",
                    }
                ],
                "speed": 2.67,
                "deg": 60,
                "gust": 2.66,
                "clouds": 97,
                "pop": 0.84,
                "rain": 4.49,
            },
        ],
    }
    city_timezone = data["city"]["timezone"]
    city = data["city"]["name"]
    country = data["city"]["country"]
    result = []
    for day_forecast in data["list"]:
        one_day_forecast = DayForecast.from_weather_dict(
            LongTermForecastClient.transform_forecast_dict(day_forecast),
            city_timezone,
            city_name=city,
            country_name=country,
            verbosity="brief",
        )
        result.append(one_day_forecast)

    expected_output = [
        DayForecast(
            temperature=299.66,
            weather_conditions="light rain",
            city="Zocca",
            country="IT",
            date=datetime.datetime(
                2022,
                8,
                30,
                11,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),
            wind_speed=None,
            sunrise=None,
            sunset=None,
        ),
        DayForecast(
            temperature=295.76,
            weather_conditions="light rain",
            city="Zocca",
            country="IT",
            date=datetime.datetime(
                2022,
                8,
                31,
                11,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),
            wind_speed=None,
            sunrise=None,
            sunset=None,
        ),
        DayForecast(
            temperature=293.38,
            weather_conditions="light rain",
            city="Zocca",
            country="IT",
            date=datetime.datetime(
                2022,
                9,
                1,
                11,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),
            wind_speed=None,
            sunrise=None,
            sunset=None,
        ),
    ]
    assert result == expected_output
