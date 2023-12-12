from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from weather_api.weather_requests.weather_requests_database import (
    City,
    WeatherForecast,
    WeatherRequest,
)

if TYPE_CHECKING:
    from weather_api.weather_requests.weatherclient import DayForecast


def add_weather_request_entry_to_db(request: "DayForecast", session: Session) -> None:
    """Take the api result for the weather at the moment and a db session and add the entry to the database."""
    city_entry = (
        session.query(City)
        .filter(City.city_name == request.city, City.country == request.country)
        .one_or_none()
    )
    weather = WeatherRequest(
        date=request.date,
        weather_conditions=request.weather_conditions,
        temperature=request.temperature,
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
    for day in forecast:
        city_entry = (
            session.query(City)
            .filter(day.city == City.city_name, day.country == City.country)
            .one_or_none()
        )
        weather_forecast = WeatherForecast(
            weather_forecast=forecast,
        )

        if city_entry is None:
            city_entry = City(
                country=day.country,
                city_name=day.city,
            )
            session.add(city_entry)

        weather_forecast.city = city_entry  # type: ignore

        session.add(weather_forecast)

    session.commit()
