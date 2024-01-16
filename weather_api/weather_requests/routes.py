from fastapi import APIRouter, HTTPException, status

from weather_api.weather_requests import service_handler
from weather_api.weather_requests.clients.base_day_forecast import (
    BadApiException,
    BadCityException,
)
from weather_api.weather_requests.clients.storage_clients import DBStorageClient
from weather_api.weather_requests.clients.weather_clients import ClientProvider, get_weather_client
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
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url and 2 letters country code as a url parameter.
    returns the weather results from selected weather client."""
    client = get_weather_client(ClientProvider.OPENWEATHER)
    try:
        request = service_handler.weather_endpoint_handler(client, city_name, country_code)
    except AttributeError:
        raise HTTPException(
            status_code=404,
            detail=f"{country_code} is not valid. Please refer to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.",
        )
    except BadCityException as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except BadApiException:
        raise HTTPException(status_code=500, detail="Internal error.")

    if not request:
        raise IndexError("No Forecast available.")

    storage_client = DBStorageClient
    service_handler.storage_handler(storage_client, request)

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
) -> list[WeatherResponseSchema]:
    """Expect a city name in the url, 2 letters country code and days of forecast as a url parameter.
    returns weather forecast in a list from selected weather client."""
    client = get_weather_client(ClientProvider.WEATHERAPI)
    try:
        request = service_handler.weather_endpoint_handler(client, city_name, country_code, days)
    except AttributeError:
        raise HTTPException(
            status_code=404,
            detail=f"{country_code} is not valid. Please refer to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.",
        )
    except BadCityException:
        raise HTTPException(status_code=404, detail="City does not exist.")
    except BadApiException:
        raise HTTPException(status_code=500, detail="Internal error.")

    if not request:
        raise IndexError("No Forecast available.")

    storage_client = DBStorageClient
    service_handler.storage_handler(storage_client, request)

    return request
