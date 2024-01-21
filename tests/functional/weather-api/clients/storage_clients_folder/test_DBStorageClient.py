import datetime

from weather_api.weather_requests.clients.storage_clients_folder.storage_clients import (
    DBStorageClient,
)
from weather_api.weather_requests.weather_models import City, WeatherRequest


def test_DBStorageClient_read(override_get_db):
    client = DBStorageClient()
    client.session = override_get_db
    entry = [City(country="WW", city_name="Very_beautiful_city")]
    client.save(entry)

    result = client.read(model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"})

    assert result == entry


def test_DBStorageClient_read(override_get_db):
    client = DBStorageClient()
    client.session = override_get_db
    city_to_save = City(country="WW", city_name="Very_beautiful_city")
    weather_to_save = WeatherRequest(
        date=datetime.datetime(
            2023, 12, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
        ),
        weather_conditions="quite bad",
        temperature=3.5,
        wind_speed=0.0,
        humidity=22,
    )
    weather_to_save.city = city_to_save
    entries = [city_to_save, weather_to_save]
    client.save(entries)

    result1 = client.read(model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"})
    result2 = client.read(
        model=WeatherRequest, filter={"weather_conditions": "quite bad", "temperature": 3.5}
    )

    assert result1[0] == city_to_save
    assert result2[0] == weather_to_save
