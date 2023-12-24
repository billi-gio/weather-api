from fastapi import APIRouter, Depends, HTTPException, status
from requests import HTTPError
from sqlalchemy.orm import Session
import pycountry

from weather_api.config import get_db
from weather_api.weather_requests.add_new_request_to_db import (
    add_forecast_entry,
    add_weather_request_entry_to_db,
)
from weather_api.weather_requests.schemas import WeatherForecast, WeatherRequestSchema
from weather_api.weather_requests.weather_clients.clients import get_client

weather_router = APIRouter()


@weather_router.get(
    "/weather-now/{city_name}",
    response_model=WeatherRequestSchema,
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weathernow(
    city_name: str,
    country: str | None = None,
    db: Session = Depends(get_db),
) -> WeatherRequestSchema:
    client = get_client("now")
    if country:
        country = pycountry.countries.get(name=country).alpha_2
    try:
        request = client.get_weather_forecast(city_name, country)  # type: ignore
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")

    add_weather_request_entry_to_db(request, db)  # type: ignore

    return WeatherRequestSchema(**request.__dict__)


@weather_router.get(
    "/weather-forecast/{city_name}",
    response_model=list[WeatherForecast],
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weather_forecast(
    city_name: str,
    country: str | None = None,
    days: int = 10,
    db: Session = Depends(get_db),
) -> list[WeatherForecast]:
    client = get_client("forecast")
    if country:
        country = pycountry.countries.get(name=country).alpha_2
    try:
        weather = client.get_weather_forecast(city_name, days, country)  # type: ignore
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")

    add_forecast_entry(weather, db)  # type: ignore

    days_forecast_list = []
    for entry in weather:  # type: ignore
        days_forecast_list.append(
            WeatherForecast(
                date=str(entry.date.date()),
                weather_conditions=entry.weather_conditions,
                temperature=entry.temperature,
                wind_speed=entry.wind_speed,
                humidity=entry.humidity,
            )
        )
    return days_forecast_list
