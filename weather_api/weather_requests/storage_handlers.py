"""Handles the data storage."""
import uuid

from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    DBStorageClient,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.weather_models import City, WeatherRequest


def storage_handler(
    client: DBStorageClient | CSVStorageClient, data: list[WeatherResponseSchema]
) -> None:
    """From a data list, create a db storage client, checks for existing city entries in db,
    finally send a list to the client to save in db."""
    data_to_add_to_db = []

    city_entry = client.read(
        model=City, filter={"city_name": data[0].city_name, "country": data[0].country}
    )

    if not city_entry:
        city_entry = City(
            id=str(uuid.uuid4()),
            country=data[0].country,
            city_name=data[0].city_name,
        )
        data_to_add_to_db.append(city_entry)
    else:
        if isinstance(city_entry[0], dict):
            city_entry = City(
                id=city_entry[0]["id"],
                country=city_entry[0]["country"],
                city_name=city_entry[0]["city_name"],
            )
        else:
            city_entry = city_entry[0]

    for dayforecast in data:
        weather = WeatherRequest(
            id=str(uuid.uuid4()),
            date=dayforecast.date,
            weather_conditions=dayforecast.weather_conditions,
            temperature=dayforecast.temperature,
            wind_speed=dayforecast.wind_speed,
            humidity=dayforecast.humidity,
        )
        weather.city = city_entry  # type: ignore

        data_to_add_to_db.append(weather)

    client.save(data_to_add_to_db)
