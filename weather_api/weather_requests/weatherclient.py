"""Client to get weather today for given city"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
import os
import textwrap

from requests import HTTPError
import pycountry  # type: ignore
import requests

from weather_api.weather_requests.add_new_request_to_db import add_entry


class ForecastVerbosity(str, Enum):
    BRIEF = "brief"
    DETAILED = "detailed"


@dataclass
class ForecastClientConfig:
    api_key: str
    units: str = "metric"


@dataclass
class DayForecast:
    """dataclass that will be filled by the weather clients"""

    date: datetime
    temperature: float
    weather_conditions: str
    city: str
    country: str
    wind_speed: float | None = None
    sunrise: datetime | None = None
    sunset: datetime | None = None

    def __str__(self) -> str:
        return textwrap.dedent(
            f"""
        Date: {self.date.date().isoformat()}
        Temperature: {self.temperature} Celsius
        Weather conditions: {self.weather_conditions}
        City: {self.city}
        Country: {self.country}
        {(f"Wind Speed: {self.wind_speed}") if self.wind_speed else ''}
        {(f"Sunrise: {self.sunrise.strftime('%H:%M:%S%z')}") if self.sunrise else ''}
        {(f"Sunset: {self.sunset.strftime('%H:%M:%S%z')}") if self.sunset else ''}
        """
        )

    @classmethod
    def from_weather_dict(
        cls,
        weather_dictionary: dict,
        city_timezone: int,
        city_name: str,
        country_name: str,
        verbosity: str | None = "brief",
    ) -> "DayForecast":
        """First changes times from UTC to local, then populates DayForecast"""
        weather_condition_list: list = weather_dictionary["weather"]

        utc_date = weather_dictionary["dt"]
        local_date = datetime.utcfromtimestamp(utc_date)
        local_date = local_date.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))
        utc_sunrise = weather_dictionary["sys"]["sunrise"]
        local_sunrise = datetime.utcfromtimestamp(utc_sunrise)
        local_sunrise = local_sunrise.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))
        utc_sunset = weather_dictionary["sys"]["sunset"]
        local_sunset = datetime.utcfromtimestamp(utc_sunset)
        local_sunset = local_sunset.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))

        weather_forecast = cls(
            date=local_date,
            temperature=weather_dictionary["main"]["temp"],
            weather_conditions=weather_condition_list[0]["description"],
            city=city_name,
            country=country_name,
        )
        if verbosity == ForecastVerbosity.DETAILED:
            weather_forecast.wind_speed = weather_dictionary["wind"]["speed"]
            weather_forecast.sunrise = local_sunrise
            weather_forecast.sunset = local_sunset

        add_entry(weather_forecast)
        return weather_forecast


class WeatherMapClient:
    """Client to call endpoint"""

    def __init__(self, config: ForecastClientConfig) -> None:
        self.api_key = config.api_key
        self.units = config.units

    @staticmethod
    def call_endpoint(endpoint: str, parameters: dict) -> dict:
        response = requests.get(endpoint, params=parameters, verify=False)

        response = requests.get(endpoint, params=parameters, verify=False)
        weather_dictionary: dict = response.json()
        if response.status_code != 200:
            raise HTTPError(
                f"Request failed, code: {response.status_code}, reason: {weather_dictionary['message']}",
                response=response,
            )
        return weather_dictionary


class BuildURLMixin:
    base_url = "https://api.openweathermap.org/data/2.5/"

    def build_url(self, endpoint: str) -> str:
        """Call to url builder, with given parameters"""
        url = f"{self.base_url}/{endpoint}"
        return url


class OneDayForecastClient(WeatherMapClient, BuildURLMixin):
    """Client to get today's weather in given city."""

    endpoint = "weather"

    def get_weather_forecast(
        self, city: str | None = None, verbosity: str | None = "brief"
    ) -> DayForecast:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        weather_url = self.build_url(self.endpoint)
        parameters = {"q": city, "units": self.units, "appid": self.api_key}

        weather_dictionary = self.call_endpoint(weather_url, parameters)
        city_timezone = weather_dictionary["timezone"]
        city_name = weather_dictionary["name"]
        country = pycountry.countries.get(alpha_2=weather_dictionary["sys"]["country"]).name
        weather_forecast = DayForecast.from_weather_dict(
            weather_dictionary, city_timezone, city_name, country, verbosity
        )
        return weather_forecast


def main(city: str | None = None, verbosity: str | None = None) -> DayForecast:
    config = ForecastClientConfig(str(os.getenv("API_KEY")))

    client = OneDayForecastClient(config)
    forecast = client.get_weather_forecast(city, verbosity)

    return forecast


if __name__ == "__main__":
    print(main())
