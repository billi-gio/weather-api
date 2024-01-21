"""WEATHERAPI client to get weather today for given city"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
import os

import pytz

from weather_api.weather_requests.clients.weather_clients_folder.base_day_forecast import (
    BadApiException,
    BadCityException,
    CallEndpointMixin,
    DayForecast,
    ForecastClientConfig,
)


@dataclass
class WeatherApiDayForecast(DayForecast):
    @classmethod
    def from_weather_dict(
        cls,
        weather_dictionary: dict,
        city_timezone: int,
        city_name: str,
        country_name: str,
    ) -> "WeatherApiDayForecast":
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
            city_name=city_name,
            country=country_name,
        )
        return weather_forecast


class WeatherAPIClient(CallEndpointMixin):
    """Client to get current weather, current or forecast."""

    base_url = "http://api.weatherapi.com/v1"

    def get_weather_dictionary(self, weather_url: str, parameters: dict) -> dict:
        """Helper to call the endpoint and extract values for both methods, now and long forecast."""

        response = self.call_endpoint(weather_url, parameters)
        if response.status_code == 400:
            raise BadCityException(f"{parameters['q']} does not match any location.")
        elif response.status_code == 403:
            raise BadApiException(
                f"""Failure core: {response.status_code}. {response.json()['error']['message']} 
                                  Please check https://www.weatherapi.com/api-explorer.aspx#forecast for more info"""
            )

        weather_dictionary = response.json()

        city_tz = pytz.timezone(weather_dictionary["location"]["tz_id"])

        return_dictionary = {
            "weather_dictionary": weather_dictionary,
            "city_timezone": int(city_tz.utcoffset(datetime.now()).total_seconds()),
            "city_name": weather_dictionary["location"]["name"],
            "country": weather_dictionary["location"]["country"],
        }
        return return_dictionary

    def get_current_weather(
        self,
        city: str,
        country_code: str,
    ) -> list[WeatherApiDayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        endpoint = "current.json"
        weather_url = self.build_url(self.base_url, endpoint)
        parameters = {"key": self.api_key, "q": f"{city},{country_code}"}

        weather_dictionary = self.get_weather_dictionary(weather_url, parameters)

        day = WeatherApiDayForecast.from_weather_dict(
            weather_dictionary["weather_dictionary"],
            weather_dictionary["city_timezone"],
            weather_dictionary["city_name"],
            weather_dictionary["country"],
        )
        weather_forecast = []
        weather_forecast.append(day)
        return weather_forecast

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

    def get_long_weather_forecast(
        self,
        city: str,
        country_code: str,
        days: int = 10,
    ) -> list[WeatherApiDayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        endpoint = "forecast.json"
        weather_url = self.build_url(self.base_url, endpoint)
        parameters = {
            "key": self.api_key,
            "q": f"{city},{country_code}",
            "days": days,
        }

        weather_dictionary = self.get_weather_dictionary(weather_url, parameters)

        weather_forecast = []
        for index, day_forecast in enumerate(
            weather_dictionary["weather_dictionary"]["forecast"]["forecastday"]
        ):
            one_day_forecast = WeatherApiDayForecast.from_weather_dict(
                self.transform_forecast_dict(day_forecast),
                weather_dictionary["city_timezone"],
                weather_dictionary["city_name"],
                weather_dictionary["country"],
            )
            weather_forecast.append(one_day_forecast)
            if index == days:
                break
        return weather_forecast


def main():
    city = "camposampiero"
    country = "it"
    config = ForecastClientConfig(str(os.getenv("API_KEY_WEATHERAPI")))
    client: Any = WeatherAPIClient(config)
    forecast = client.get_current_weather(city, country)
    return forecast


if __name__ == "__main__":
    print(main())
