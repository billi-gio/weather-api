"""Client to get weather today for given city"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
import os
import textwrap

from requests import HTTPError
import pycountry
import requests


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
        City: {self.city}
        Country: {self.country}
        """
        )

    @classmethod
    def from_weather_dict(
        cls,
        weather_dictionary: dict,
        city_timezone: int,
        city_name: str,
        country_name: str,
    ) -> "DayForecast":
        """First changes times from UTC to local, then populates DayForecast"""
        weather_condition_list: list = weather_dictionary["weather"]

        utc_date = weather_dictionary["dt"]
        local_date = datetime.utcfromtimestamp(utc_date)
        local_date = local_date.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))

        weather_forecast = cls(
            date=local_date,
            temperature=weather_dictionary["main"]["temp"],
            weather_conditions=weather_condition_list[0]["description"],
            city=city_name,
            country=country_name,
            wind_speed=weather_dictionary["wind"]["speed"],
            humidity=weather_dictionary["main"]["humidity"],
        )

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
            raise HTTPError

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
        self,
        city: str | None = None,
        country_code: str | None = None,
    ) -> DayForecast:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        weather_url = self.build_url(self.endpoint)
        parameters = {"q": f"{city},{country_code}", "units": self.units, "appid": self.api_key}
        try:
            weather_dictionary = self.call_endpoint(weather_url, parameters)
        except HTTPError:
            raise HTTPError

        city_timezone = weather_dictionary["timezone"]
        city_name = weather_dictionary["name"]
        country = pycountry.countries.get(alpha_2=weather_dictionary["sys"]["country"]).name
        weather_forecast = DayForecast.from_weather_dict(
            weather_dictionary, city_timezone, city_name, country
        )
        return weather_forecast


class LongTermForecastClient(WeatherMapClient, BuildURLMixin):
    """Client to get 14 days weather in given city."""

    endpoint = "forecast/daily"

    @staticmethod
    def transform_forecast_dict(day_forecast: dict) -> dict:
        """Transform the 14 days json into a dictionary that can be sent to from_weather_dict.
        Input json example: https://openweathermap.org/forecast16.
        Output mirrors json: https://openweathermap.org/current
        """
        one_day_forecast = {}
        one_day_forecast["dt"] = day_forecast["dt"]
        one_day_forecast["main"] = {"temp": day_forecast["temp"]["day"]}
        weather_conditions_list = day_forecast["weather"]
        weather_conditions = weather_conditions_list[0]["description"]
        one_day_forecast["weather"] = [{"description": weather_conditions}]
        one_day_forecast["wind"] = {"speed": day_forecast["speed"]}
        one_day_forecast["main"] = {"humidity": day_forecast["humidity"]}

        return one_day_forecast

    def get_weather_forecast(
        self, city: str, country_code: str | None = None, days: int | None = None
    ) -> list[DayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have 14 days weather"""
        weather_url = self.build_url(self.endpoint)
        parameters = {"q": f"{city},{country_code}", "units": self.units, "appid": self.api_key}
        try:
            weather_dictionary = self.call_endpoint(weather_url, parameters)
        except HTTPError:
            raise HTTPError
        city_timezone = weather_dictionary["city"]["timezone"]
        city_name = weather_dictionary["city"]["name"]
        country = pycountry.countries.get(alpha_2=weather_dictionary["city"]["country"]).name

        weather_forecast = []
        for index, day_forecast in enumerate(weather_dictionary["list"]):
            one_day_forecast = DayForecast.from_weather_dict(
                self.transform_forecast_dict(day_forecast),
                city_timezone,
                city_name,
                country,
            )
            weather_forecast.append(one_day_forecast)
            if index == days:
                break

        return weather_forecast


def main() -> DayForecast | list[DayForecast]:
    city: str = "camposampiero"
    country_code: str = "it"
    days: int = 10
    forecast_bool: bool = True
    config = ForecastClientConfig(str(os.getenv("API_KEY_OPENWEATHER")))

    if forecast_bool:
        client: Any = LongTermForecastClient(config)
        forecast = client.get_weather_forecast(city, country_code, days)
    else:
        client = OneDayForecastClient(config)
        forecast = client.get_weather_forecast(city, country_code)

    return forecast


if __name__ == "__main__":
    print(main())
