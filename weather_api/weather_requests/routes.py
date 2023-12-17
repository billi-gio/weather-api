from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from requests import HTTPError
from sqlalchemy.orm import Session

from weather_api.config import get_db
from weather_api.weather_requests.add_new_request_to_db import (
    add_forecast_entry,
    add_weather_request_entry_to_db,
)
from weather_api.weather_requests.clients.clients import get_client
from weather_api.weather_requests.schemas import WeatherForecast, WeatherRequestSchema
import weather_api.weather_requests.weatherclient as weatherclient

weather_router = APIRouter()


@weather_router.get(
    "/weather-now/{city_name}",
    response_model=WeatherRequestSchema,
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weather(
    city_name: str,
    verbosity: Optional[weatherclient.ForecastVerbosity] = None,
    db: Session = Depends(get_db),
) -> WeatherRequestSchema:
    client = get_client("now")
    try:
        request = client.get_weather_forecast(city_name, verbosity)
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")

    add_weather_request_entry_to_db(request, db)  # type: ignore

    return WeatherRequestSchema(**request.__dict__)


@weather_router.get(
    "/weather-forecast/{city_name}",
    response_model=WeatherForecast,
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weather_forecast(
    city_name: str,
    days: Optional[int] = None,
    verbosity: Optional[weatherclient.ForecastVerbosity] = None,
    db: Session = Depends(get_db),
) -> WeatherForecast | None:
    client = get_client("forecast")
    try:
        weather = client.get_weather_forecast(city_name, verbosity, days)  # type: ignore
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")

    add_forecast_entry(weather, db)  # type: ignore

    for entry in weather:  # type: ignore
        return WeatherForecast(**entry.__dict__)
    return None
