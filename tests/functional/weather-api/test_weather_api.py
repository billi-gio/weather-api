from unittest.mock import patch
import datetime


class DummyDayForecast:
    date: datetime = datetime.datetime(
        2023, 12, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
    )
    temperature: str = 0.0
    weather_conditions: str = "dummy"
    city: str = "dummy"
    country: str = "dummy"
    wind_speed: float = 0.0
    humidity: float = 0.0


@patch(
    "weather_api.weather_requests.weather_clients.weatherclient.OneDayForecastClient.get_weather_forecast"
)
def test_weather_now_returns_correct_response(dummy_onedayforecast_client, test_client):
    city_name = "who cares"

    dummy_onedayforecast_client.return_value = DummyDayForecast

    response = test_client.get(f"/weather-now/{city_name}")

    assert response.status_code == 200
    assert response.json() == {
        "weather_conditions": "dummy",
        "temperature": 0.0,
        "wind_speed": 0.0,
        "humidity": 0.0,
    }


@patch(
    "weather_api.weather_requests.weather_clients.weatherapi_client.WeatherForecast.get_weather_forecast"
)
def test_weatherforecast_returns_correct_response(dummy_longforecast_client, test_client):
    city_name = "who cares"

    dummy_listof_forecasts = []
    dummy_listof_forecasts.append(DummyDayForecast)
    dummy_longforecast_client.return_value = dummy_listof_forecasts

    response = test_client.get(f"/weather-forecast/{city_name}")

    assert response.status_code == 200
    assert response.json() == [
        {
            "date": "2023-12-04",
            "weather_conditions": "dummy",
            "temperature": 0.0,
            "wind_speed": 0.0,
            "humidity": 0.0,
        }
    ]
