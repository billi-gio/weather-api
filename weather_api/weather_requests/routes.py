from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from weather_api.config import ApplicationConfig, load_application_config
from weather_api.weather_requests.schemas import WeatherRequest
from weather_api.weather_requests.weatherclient import DayForecast, main

weather_router = APIRouter()


@weather_router.get(
    "/weather-now/{city_name}",
    response_model=WeatherRequest,
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weather(
    city_name: str,
    verbosity: Optional[str] = None,
    config: ApplicationConfig = Depends(load_application_config),
) -> dict[str, str | float]:
    try:
        weather: DayForecast = main(city_name, verbosity)
    except:
        raise HTTPException(status_code=404, detail="Something went wrong, check city name")
    return {
        "service": config.service,
        "weather_conditions": weather.weather_conditions,
        "temperature": weather.temperature,
        # "environment": config.environment,
    }
