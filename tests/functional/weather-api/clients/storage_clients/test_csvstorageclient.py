from unittest.mock import patch

from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    headers_exist,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.weather_models import City, WeatherRequest


def test_headers_exist(dummy_day_forecast, tmp_path):
    entry_list = [
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
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file = temp_dir / "temp_file.csv"
    temp_file.write_text(
        "date,weather_conditions,temperature,wind_speed,humidity,city_name,country"
    )

    header = list(entry_list[0].model_dump().keys())

    assert headers_exist(temp_file, header) is True


@patch("weather_api.weather_requests.clients.storage_clients.storage_clients.headers_exist")
@patch("weather_api.weather_requests.clients.storage_clients.storage_clients.retrieve_file_name")
@patch(
    "weather_api.weather_requests.clients.storage_clients.storage_clients.check_row_match_filters"
)
def test_csvstorageclient_save(
    dummy_row_match_filters, dummy_file_name, dummy_find_headers, tmp_path
):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()
    temp_file = temp_dir / "temp_file.csv"

    client = CSVStorageClient(temp_dir)

    entry = [City(id="", country="WW", city_name="Very_beautiful_city")]
    dummy_file_name.return_value = temp_file
    dummy_find_headers.return_value = True
    dummy_row_match_filters.return_value = True

    outcome = {"id": "", "city_name": "Very_beautiful_city", "country": "WW"}

    client.save(entry)
    result = client.read(
        model=City, filter={"id": "", "city_name": "Very_beautiful_city", "country": "WW"}
    )
    print(result)
    assert result[0] == outcome


@patch("weather_api.weather_requests.clients.storage_clients.storage_clients.headers_exist")
@patch("weather_api.weather_requests.clients.storage_clients.storage_clients.retrieve_file_name")
def test_csvstorageclient_save_and_read(
    dummy_file_name, dummy_find_headers, dummy_day_forecast, tmp_path
):
    weather_entry_list = [
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

    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()
    temp_file = temp_dir / "temp_file.csv"

    dummy_file_name.return_value = temp_file

    client = CSVStorageClient(temp_dir)
    city_entry_list = [City(country="dummy", city_name="dummy")]

    for entry in weather_entry_list:
        weather_list = [
            WeatherRequest(
                date=entry.date,
                weather_conditions=entry.weather_conditions,
                temperature=entry.temperature,
                wind_speed=entry.wind_speed,
                humidity=entry.humidity,
            )
        ]
        weather_list[0].city = city_entry_list[0]
    client.save(weather_list)

    row = {
        "id": "",
        "date": "2023-12-04 00:00:00+01:00",
        "weather_conditions": "dummy",
        "temperature": "0.0",
        "wind_speed": "0.0",
        "humidity": "0.0",
        "city_id": "",
    }

    filter = {
        "id": "",
        "date": "2023-12-04 00:00:00+01:00",
        "weather_conditions": "dummy",
        "temperature": "0.0",
        "wind_speed": "0.0",
        "humidity": "0.0",
        "city_id": "",
    }

    dummy_find_headers.return_value = True

    response = client.read(filter=filter, model=City)

    assert response[0] == row
