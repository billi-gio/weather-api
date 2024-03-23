import datetime
import uuid

from weather_api.weather_requests.clients.storage_clients.storage_clients import DBStorageClient
from weather_api.weather_requests.weather_models import City, WeatherRequest


def test_dbstorageclient_save(override_get_engine):
    engine = override_get_engine
    client = DBStorageClient(engine)
    entry = [
        City(
            id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            country="WW",
            city_name="Very_beautiful_city",
        )
    ]
    client.save(entry)

    result = client.read(model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"})

    assert result == entry


def test_dbstorageclient_read(override_get_engine):
    engine = override_get_engine
    client = DBStorageClient(engine)
    city = client.read(model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"})
    weather_to_save = WeatherRequest(
        id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        date=datetime.datetime(
            2023, 12, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
        ),
        weather_conditions="quite bad",
        temperature=3.5,
        wind_speed=0.0,
        humidity=22,
    )

    weather_to_save.city = city[0]
    entries = [weather_to_save]
    client.save(entries)

    result2 = client.read(
        model=WeatherRequest, filter={"weather_conditions": "quite bad", "temperature": 3.5}
    )

    assert result2[0] == weather_to_save
