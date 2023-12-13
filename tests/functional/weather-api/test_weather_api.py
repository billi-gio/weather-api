import datetime

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.routes import get_db, get_forecast_client, get_weather_now_client
from weather_api.weather_requests.weather_requests_database import Table
from weather_api.weather_requests.weatherclient import DayForecast, LongTermForecastClient


def test_returns_correct_response(test_client):
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
        database = TestingSessionLocal()
        yield database
        database.close()

    test_client.app.dependency_overrides[get_db] = override_get_db

    class DummyDayForecast:
        date: datetime = "2023-12-04 12:56:54+01:00"
        temperature: str = 0.0
        weather_conditions: str = "dummy"
        city: str = "dummy"
        country: str = "dummy"
        sunrise: datetime = "2023-12-04 12:56:54+01:00"
        sunset: datetime = "2023-12-04 12:56:54+01:00"

    class DummyClient:
        def get_weather_forecast(city_name, verbosity):
            return DummyDayForecast

    def override_get_client():
        return DummyClient

    test_client.app.dependency_overrides[get_weather_now_client] = override_get_client

    city_name = "camposampiero"

    response = test_client.get(f"/weather-now/{city_name}")

    assert response.status_code == 200
    assert response.json() == {
        "weather_conditions": "dummy",
        "temperature": 0.0,
        "sunrise": "2023-12-04T12:56:54+01:00",
        "sunset": "2023-12-04T12:56:54+01:00",
    }

    Table.metadata.drop_all(bind=engine)


# def test_returns_correct_response(test_client):
#     DATABASE_URL = "sqlite:///:memory:"
#     engine = create_engine(
#         DATABASE_URL,
#         connect_args={
#             "check_same_thread": False,
#         },
#         poolclass=StaticPool,
#     )
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Table.metadata.create_all(bind=engine)

#     def override_get_db():
#         database = TestingSessionLocal()
#         yield database
#         database.close()

#     test_client.app.dependency_overrides[get_db] = override_get_db

#     class DummyDayForecast:
#         date: datetime = "2023-12-04 12:56:54+01:00"
#         temperature: str = 0.0
#         weather_conditions: str = "dummy"
#         city: str = "dummy"
#         country: str = "dummy"
#         sunrise: datetime = "2023-12-04 12:56:54+01:00"
#         sunset: datetime = "2023-12-04 12:56:54+01:00"

#     class DummyClient:
#         def get_weather_forecast(city_name, verbosity, days):
#             day_forecast_instance = DummyDayForecast
#             day_forecast_instance.date = "2023-12-04 12:56:54+01:00"
#             day_forecast_instance.temperature = 0.0
#             day_forecast_instance.weather_conditions = "dummy"
#             day_forecast_instance.city = "dummy"
#             day_forecast_instance.country = "dummy"
#             day_forecast_instance.sunrise= "2023-12-04 12:56:54+01:00"
#             day_forecast_instance.sunset = "2023-12-04 12:56:54+01:00"
#             forecast_ls = []
#             forecast_ls.append(day_forecast_instance)
#             return forecast_ls

#     def override_get_client():
#         return DummyClient

#     test_client.app.dependency_overrides[get_forecast_client] = override_get_client

#     city_name = "camposampiero"

#     response = test_client.get(f"/weather-forecast/{city_name}")

#     assert response.status_code == 200
#     # assert response.json() == {
#     #     "weather_conditions": "dummy",
#     #     "temperature": 0.0,
#     #     "sunrise": "2023-12-04T12:56:54+01:00",
#     #     "sunset": "2023-12-04T12:56:54+01:00",
#     # }

#     Table.metadata.drop_all(bind=engine)


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
