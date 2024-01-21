from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import textwrap

from requests import Response
import requests


class BadCityException(Exception):
    pass


class BadApiException(Exception):
    pass


@dataclass
class ForecastClientConfig:
    api_key: str
    units: Optional[str] = "metric"


class BaseWeatherClient(ABC):
    def __init__(self, config: ForecastClientConfig) -> None:
        self.api_key = config.api_key
        self.units = config.units

    @abstractmethod
    def build_url(self, base_url: str, endpoint: str) -> str:
        """Build url to send to call_endpoint."""

    @abstractmethod
    def call_endpoint(self, endpoint: str, parameters: dict) -> Response:
        """Call the endpoint and return the reponse."""


class CallEndpointMixin(BaseWeatherClient):
    def build_url(self, base_url: str, endpoint: str) -> str:
        url = f"{base_url}/{endpoint}"
        return url

    def call_endpoint(self, endpoint: str, parameters: dict) -> Response:
        response = requests.get(endpoint, params=parameters, verify=False)
        return response


@dataclass
class DayForecast:
    """Dataclass that will be filled by the weather clients"""

    date: datetime
    temperature: float
    weather_conditions: str
    city_name: str
    country: str
    wind_speed: float
    humidity: float

    def __str__(self) -> str:
        return textwrap.dedent(
            f"""
        Date: {self.date.date().isoformat()}
        Temperature: {self.temperature} Celsius
        Weather conditions: {self.weather_conditions}
        Wind Speed: {self.wind_speed}
        Humidity; {self.humidity}
        City: {self.city_name}
        Country: {self.country}
        """
        )
