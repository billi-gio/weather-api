from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    DBStorageClient,
)
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.weather_models import City, WeatherRequest


def db_storage_handler(
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


def csv_storage_handler(client: CSVStorageClient, data: list[WeatherResponseSchema]) -> None:
    """From a data list, send the data to the client to save it in a csv file."""
    client.save(data)