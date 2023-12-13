from datetime import datetime
from typing import Generator, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from requests import HTTPError
from sqlalchemy.orm import Session, sessionmaker

from weather_api.config import ApplicationConfig, load_application_config
from weather_api.weather_requests.add_new_request_to_db import (
    add_forecast_entry,
    add_weather_request_entry_to_db,
)
from weather_api.weather_requests.schemas import WeatherForecast, WeatherRequestSchema
from weather_api.weather_requests.weather_db_engine import engine
from weather_api.weather_requests.weatherclient import DayForecast
import weather_api.weather_requests.weatherclient as weatherclient

weather_router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_weather_now_client(
    config: ApplicationConfig = Depends(load_application_config),
) -> weatherclient.OneDayForecastClient:
    configuration = weatherclient.ForecastClientConfig(config.api_key)
    client = weatherclient.OneDayForecastClient(configuration)
    return client


def get_forecast_client(
    config: ApplicationConfig = Depends(load_application_config),
) -> weatherclient.LongTermForecastClient:
    configuration = weatherclient.ForecastClientConfig(config.api_key)
    client = weatherclient.LongTermForecastClient(configuration)
    return client


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
    client: weatherclient.OneDayForecastClient = Depends(get_weather_now_client),
) -> dict[str, str | float | datetime | None]:
    try:
        request = client.get_weather_forecast(city_name, verbosity)
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")
    print(request)
    add_weather_request_entry_to_db(request, db)

    return {
        "weather_conditions": request.weather_conditions,
        "temperature": request.temperature,
        "sunrise": request.sunrise,
        "sunset": request.sunset,
    }


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
    client: weatherclient.LongTermForecastClient = Depends(get_forecast_client),
) -> dict[str, list[DayForecast]]:
    try:
        weather = client.get_weather_forecast(city_name, verbosity, days)
    except HTTPError:
        raise HTTPException(status_code=404, detail="Check city name or api key")
    add_forecast_entry(weather, db)
    return {
        "forecast": weather,
    }
