from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
import textwrap

from requests import HTTPError
import pytz
import requests


@dataclass
class ForecastClientConfig:
    api_key: str


class WeatherMapClient:
    """Client to call endpoint"""

    def __init__(self, config: ForecastClientConfig) -> None:
        self.api_key = config.api_key

    @staticmethod
    def call_endpoint(endpoint: str, parameters: dict) -> dict:
        response = requests.get(endpoint, params=parameters, verify=False)
        response = requests.get(endpoint, params=parameters, verify=False)
        weather_dictionary: dict = response.json()
        if response.status_code != 200:
            raise HTTPError

        return weather_dictionary


class BuildURLMixin:
    base_url = "http://api.weatherapi.com/v1"

    def build_url(self, endpoint: str) -> str:
        """Call to url builder, with given parameters"""
        url = f"{self.base_url}/{endpoint}"
        return url


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

        utc_date = weather_dictionary["location"]["localtime_epoch"]
        local_date = datetime.utcfromtimestamp(utc_date)
        local_date = local_date.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))

        weather_forecast = cls(
            date=local_date,
            temperature=weather_dictionary["current"]["temp_c"],
            weather_conditions=weather_dictionary["current"]["condition"]["text"],
            wind_speed=weather_dictionary["current"]["wind_kph"],
            humidity=weather_dictionary["current"]["humidity"],
            city=city_name,
            country=country_name,
        )

        return weather_forecast


class WeatherNow(WeatherMapClient, BuildURLMixin):
    """Client to get today's weather in given city."""

    endpoint = "current.json"

    def get_weather_forecast(
        self,
        city: str,
        country_code: str | None = None,
    ) -> DayForecast:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        weather_url = self.build_url(self.endpoint)
        parameters = {"key": self.api_key, "q": f"{city},{country_code if country_code else ''}"}

        try:
            weather_dictionary = self.call_endpoint(weather_url, parameters)
        except HTTPError:
            raise HTTPError

        city_tz = pytz.timezone(weather_dictionary["location"]["tz_id"])
        city_timezone = int(city_tz.utcoffset(datetime.now()).total_seconds())
        city_name = weather_dictionary["location"]["name"]
        country = weather_dictionary["location"]["country"]
        weather_forecast = DayForecast.from_weather_dict(
            weather_dictionary,
            city_timezone,
            city_name,
            country,
        )
        return weather_forecast


class WeatherForecast(WeatherMapClient, BuildURLMixin):
    """Client to get today's weather in given city."""

    endpoint = "forecast.json"

    @staticmethod
    def transform_forecast_dict(day_forecast: dict) -> dict:
        """Transform the forecast json into a dictionary that can be sent to from_weather_dict."""
        one_day_forecast = {}
        one_day_forecast["location"] = {"localtime_epoch": day_forecast["date_epoch"]}
        one_day_forecast["current"] = {
            "temp_c": day_forecast["day"]["avgtemp_c"],
            "condition": {"text": day_forecast["day"]["condition"]["text"]},
            "wind_kph": day_forecast["day"]["avgvis_km"],
            "humidity": day_forecast["day"]["avghumidity"],
        }
        return one_day_forecast

    def get_weather_forecast(
        self,
        city: str,
        days: int,
        country_code: str | None = None,
    ) -> list[DayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        weather_url = self.build_url(self.endpoint)
        parameters = {
            "key": self.api_key,
            "q": f"{city},{country_code if country_code else ''}",
            "days": days,
        }

        try:
            weather_dictionary = self.call_endpoint(weather_url, parameters)
        except HTTPError:
            raise HTTPError

        city_tz = pytz.timezone(weather_dictionary["location"]["tz_id"])
        city_timezone = int(city_tz.utcoffset(datetime.now()).total_seconds())
        city_name = weather_dictionary["location"]["name"]
        country = weather_dictionary["location"]["country"]
        weather_forecast = []
        for index, day_forecast in enumerate(weather_dictionary["forecast"]["forecastday"]):
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


def main():
    city = "camposampiero"
    country = "it"
    config = ForecastClientConfig
    client: Any = WeatherForecast(config)
    forecast = client.get_weather_forecast(city, country)
    return forecast


if __name__ == "__main__":
    print(main())
