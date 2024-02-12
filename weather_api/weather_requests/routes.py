"""Endpoints for current and forecast weather."""

from fastapi import APIRouter, HTTPException, status

from weather_api.config import load_config
from weather_api.weather_requests import service_handler
from weather_api.weather_requests.clients.storage_clients.storage_factory import get_storage_client
from weather_api.weather_requests.clients.weather_clients.base_weather_client import (
    BadApiException,
    BadCityException,
)
from weather_api.weather_requests.clients.weather_clients.weather_factory import get_weather_client
from weather_api.weather_requests.schemas import WeatherResponseSchema

weather_router = APIRouter()


@weather_router.get(
    "/weather-now/{country_code}/{city_name}",
    response_model=list[WeatherResponseSchema],
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weathernow(
    city_name: str,
    country_code: str,
    config=load_config(),
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url and 2 letters country code as a url parameter.
    returns the weather results from selected weather client."""
    try:
        client = get_weather_client(config["weather_now_provider"])
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    try:
        storage_client = get_storage_client(config["database_storage_type"])
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    try:
        return service_handler.get_request_helper(client, city_name, country_code, storage_client)
    except (AttributeError, BadCityException, IndexError, service_handler.NonexistentCountry) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadApiException as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@weather_router.get(
    "/weather-forecast/{country_code}/{city_name}",
    response_model=list[WeatherResponseSchema],
    status_code=status.HTTP_200_OK,
    tags=["weather_requests"],
)
async def weather_forecast(
    city_name: str,
    country_code: str,
    days: int = 10,
    config=load_config(),
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url,
    2 letters country code and days of forecast as a url parameter.
    returns weather forecast in a list from selected weather client."""
    try:
        client = get_weather_client(config["weather_forecast_provider"])
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    try:
        storage_client = get_storage_client(config["database_storage_type"])
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    try:
        return service_handler.get_request_helper(
            client, city_name, country_code, storage_client, days
        )
    except (AttributeError, BadCityException, IndexError, service_handler.NonexistentCountry) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadApiException as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
