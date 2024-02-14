from unittest.mock import patch

from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    find_if_file_exist,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema


def test_find_if_file_exist(dummy_day_forecast, tmp_path):
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

    assert find_if_file_exist(temp_dir, header).endswith(".csv")


@patch("weather_api.weather_requests.clients.storage_clients.storage_clients.find_if_file_exist")
def test_csvstorageclient_save_and_read(dummy_find_file, dummy_day_forecast, tmp_path):
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
    client = CSVStorageClient(temp_dir, "temp_file.csv")

    dummy_find_file.return_value = "temp_file.csv"
    client.save(entry_list)

    entry = ["2023-12-04 00:00:00+01:00", "dummy", "0.0", "0.0", "0.0", "dummy", "dummy"]

    filter = entry_list[0].model_dump()
    response = client.read(filter=filter)

    assert response[1] == entry
