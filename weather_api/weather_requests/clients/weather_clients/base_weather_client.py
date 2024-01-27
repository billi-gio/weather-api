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
    @abstractmethod
    def get_current_weather(
        self,
        city: str,
        country_code: str,
    ) -> list["DayForecast"]:
        "Get current weather in given city."

    @abstractmethod
    def get_long_weather_forecast(
        self, city: str, country_code: str, days: int = 10
    ) -> list["DayForecast"]:
        "Get weather forecast for n days, depending on days variable."


class CallEndpointMixin:
    def __init__(self, config: ForecastClientConfig) -> None:
        self.api_key = config.api_key
        self.units = config.units

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
