"""Endpoints for current and forecast weather."""

from fastapi import APIRouter, Depends, HTTPException, status

from weather_api.config import ApplicationConfig, load_application_config
from weather_api.weather_requests import service_handler
from weather_api.weather_requests.clients.storage_clients_folder.storage_factory import (
    get_storage_client,
)
from weather_api.weather_requests.clients.weather_clients_folder.base_day_forecast import (
    BadApiException,
    BadCityException,
)
from weather_api.weather_requests.clients.weather_clients_folder.weather_factory import (
    get_weather_client,
)
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
    config: ApplicationConfig = Depends(load_application_config),
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url and 2 letters country code as a url parameter.
    returns the weather results from selected weather client."""
    try:
        client = get_weather_client(config.weather_now_provider)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"""{config.weather_now_provider} is not a valid provider.""",
        )
    try:
        storage_client = get_storage_client(config.storage_type)
    except:
        raise HTTPException(
            status_code=400,
            detail=f"""{config.storage_type} is not a valid storage type.""",
        )

    try:
        request = service_handler.get_request_helper(
            client, city_name, country_code, storage_client
        )
    except AttributeError:
        raise HTTPException(
            status_code=404,
            detail=f"""{country_code} is not valid.
            Please refer to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.""",
        )
    except BadCityException as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except BadApiException:
        raise HTTPException(status_code=500, detail="Internal error.")
    except IndexError:
        raise HTTPException(
            status_code=404, detail=f"No Forecast available for {city_name, country_code}."
        )

    return request


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
    config: ApplicationConfig = Depends(load_application_config),
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url,
    2 letters country code and days of forecast as a url parameter.
    returns weather forecast in a list from selected weather client."""
    try:
        client = get_weather_client(config.weather_forecast_provider)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"""{config.weather_forecast_provider} is not a valid provider.""",
        )
    try:
        storage_client = get_storage_client(config.storage_type)
    except:
        raise HTTPException(
            status_code=400,
            detail=f"""{config.storage_type} is not a valid storage type.""",
        )
    try:
        request = service_handler.get_request_helper(
            client, city_name, country_code, storage_client, days
        )
    except AttributeError:
        raise HTTPException(
            status_code=404,
            detail=f"""{country_code} is not valid.
            Please refer to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.""",
        )
    except BadCityException as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except BadApiException:
        raise HTTPException(status_code=500, detail="Internal error.")
    except IndexError:
        raise HTTPException(
            status_code=404, detail=f"No Forecast available for {city_name, country_code}."
        )

    return request
