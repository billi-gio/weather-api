from unittest.mock import patch
import datetime

from pytest import raises
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.clients import openweathermap_client
from weather_api.weather_requests.clients.storage_clients import DBStorageClient
from weather_api.weather_requests.schemas import WeatherResponseSchema
from weather_api.weather_requests.service_handler import weather_endpoint_handler
from weather_api.weather_requests.weather_models import City, Table, WeatherRequest


class DummyDayForecast:
    date: datetime = datetime.datetime(
        2023, 12, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))
    )
    temperature: str = 0.0
    weather_conditions: str = "dummy"
    city_name: str = "dummy"
    country: str = "dummy"
    wind_speed: float = 0.0
    humidity: float = 0.0


@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
@patch("weather_api.weather_requests.service_handler.storage_handler")
def test_weather_now_returns_correct_response(
    dummy_db_handler, dummy_weather_handler, test_client
):
    city_name = "who cares"
    country_code = "IT"

    dummy_weather_handler.return_value = [
        WeatherResponseSchema(
            date=DummyDayForecast.date,
            weather_conditions=DummyDayForecast.weather_conditions,
            temperature=DummyDayForecast.temperature,
            wind_speed=DummyDayForecast.wind_speed,
            humidity=DummyDayForecast.humidity,
            city_name=DummyDayForecast.city_name,
            country=DummyDayForecast.country,
        )
    ]

    dummy_db_handler.return_value = None

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


@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
@patch("weather_api.weather_requests.service_handler.storage_handler")
def test_weatherforecast_returns_correct_response(
    dummy_db_handler, dummy_weather_handler, test_client
):
    city_name = "who cares"
    country_code = "IT"

    dummy_weather_handler.return_value = [
        WeatherResponseSchema(
            date=DummyDayForecast.date,
            weather_conditions=DummyDayForecast.weather_conditions,
            temperature=DummyDayForecast.temperature,
            wind_speed=DummyDayForecast.wind_speed,
            humidity=DummyDayForecast.humidity,
            city_name=DummyDayForecast.city_name,
            country=DummyDayForecast.country,
        ),
        WeatherResponseSchema(
            date=DummyDayForecast.date,
            weather_conditions=DummyDayForecast.weather_conditions,
            temperature=DummyDayForecast.temperature,
            wind_speed=DummyDayForecast.wind_speed,
            humidity=DummyDayForecast.humidity,
            city_name=DummyDayForecast.city_name,
            country=DummyDayForecast.country,
        ),
    ]

    dummy_db_handler.return_value = None

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


@patch("weather_api.weather_requests.service_handler.weather_endpoint_handler")
@patch("weather_api.weather_requests.service_handler.storage_handler")
def test_weatherforecast_returns_empty_list(dummy_db_handler, dummy_weather_handler, test_client):
    city_name = "who cares"
    country_code = "IT"

    dummy_weather_handler.return_value = []

    dummy_db_handler.return_value = None

    expected_result = IndexError

    with raises(IndexError) as err:
        test_client.get(f"/weather-forecast/{country_code}/{city_name}")
    assert err.type == expected_result


@patch(
    "weather_api.weather_requests.clients.openweathermap_client.OpenWeatherClient.get_current_weather"
)
def test_weather_service_handler(dummy_onedayforecast_client):
    city_name = "who cares"
    country_code = "PT"

    dummy_onedayforecast_client.return_value = [DummyDayForecast]

    response = weather_endpoint_handler(
        client=openweathermap_client.OpenWeatherClient,
        city_name=city_name,
        country_code=country_code,
    )

    assert [
        WeatherResponseSchema(
            date=DummyDayForecast.date,
            weather_conditions=DummyDayForecast.weather_conditions,
            temperature=DummyDayForecast.temperature,
            wind_speed=DummyDayForecast.wind_speed,
            humidity=DummyDayForecast.humidity,
            city_name=DummyDayForecast.city_name,
            country=DummyDayForecast.country,
        )
    ] == response


def test_service_handler_nonexistant_country():
    city_name = "who cares"
    country_code = "Nope"
    client = "not_important"

    expected_result = AttributeError

    with raises(AttributeError) as err:
        weather_endpoint_handler(client=client, city_name=city_name, country_code=country_code)
    assert err.type == expected_result


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Table.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def test_DBStorageClient_read():
    client = DBStorageClient
    client.session = next(override_get_db())
    entry = [City(country="WW", city_name="Very_beautiful_city")]
    client().save(entry)

    result = client().read(
        model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"}
    )

    assert result == entry


def test_DBStorageClient_read():
    client = DBStorageClient
    client.session = next(override_get_db())
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
    client().save(entries)

    result1 = client().read(
        model=City, filter={"city_name": "Very_beautiful_city", "country": "WW"}
    )
    result2 = client().read(
        model=WeatherRequest, filter={"weather_conditions": "quite bad", "temperature": 3.5}
    )

    assert result1[0] == city_to_save
    assert result2[0] == weather_to_save
