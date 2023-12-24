from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from weather_api.weather_requests.weather_requests_database import (
    City,
    WeatherForecast,
    WeatherRequest,
)

if TYPE_CHECKING:
    from weather_api.weather_requests.weather_clients.weatherclient import DayForecast


def add_weather_request_entry_to_db(request: "DayForecast", session: Session) -> None:
    """Take the api result for the weather at the moment and a db session
    and add the entry to the database."""
    city_entry = (
        session.query(City)
        .filter(City.city_name == request.city, City.country == request.country)
        .one_or_none()
    )
    weather = WeatherRequest(
        date=request.date,
        weather_conditions=request.weather_conditions,
        temperature=request.temperature,
        wind_speed=request.wind_speed,
        humidity=request.humidity,
    )

    if city_entry is None:
        city_entry = City(
            country=request.country,
            city_name=request.city,
        )
        session.add(city_entry)

    weather.city = city_entry  # type: ignore

    session.add(weather)

    session.commit()


def add_forecast_entry(forecast: list["DayForecast"], session: Session) -> None:
    """Take the 14 days forecast api result and a db session and add the entry to the database."""

    city_entry = (
        session.query(City)
        .filter(City.city_name == forecast[0].city, City.country == forecast[0].country)
        .one_or_none()
    )

    if city_entry is None:
        city_entry = City(
            country=forecast[0].country,
            city_name=forecast[0].city,
        )
        session.add(city_entry)

    for day in forecast:
        weather_forecast = WeatherForecast(
            date=day.date,
            weather_conditions=day.weather_conditions,
            temperature=day.temperature,
            wind_speed=day.wind_speed,
            humidity=day.humidity,
        )

        weather_forecast.city = city_entry  # type: ignore

        session.add(weather_forecast)

    session.commit()
