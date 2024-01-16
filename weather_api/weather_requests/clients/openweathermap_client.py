"""OPENWEATHER client to get weather today for given city"""

from datetime import datetime, timedelta, timezone
import os

import pycountry

from weather_api.weather_requests.clients.base_day_forecast import (
    BadApiException,
    BadCityException,
    BuildURLMixin,
    DayForecast,
    ForecastClientConfig,
    WeatherMapClient,
)


class WeatherOpenWeatherForecast(DayForecast):
    @classmethod
    def from_weather_dict(
        cls,
        weather_dictionary: dict,
        city_timezone: int,
        city_name: str,
        country_name: str,
    ) -> "DayForecast":
        """Populates DayForecast for the openweathermap_client."""
        weather_condition_list: list = weather_dictionary["weather"]

        utc_date = weather_dictionary["dt"]
        local_date = datetime.utcfromtimestamp(utc_date)
        local_date = local_date.replace(tzinfo=timezone(timedelta(seconds=city_timezone)))

        weather_forecast = cls(
            date=local_date,
            temperature=weather_dictionary["main"]["temp"],
            weather_conditions=weather_condition_list[0]["description"],
            city_name=city_name,
            country=country_name,
            wind_speed=weather_dictionary["wind"]["speed"],
            humidity=weather_dictionary["main"]["humidity"],
        )

        return weather_forecast


class OpenWeatherClient(WeatherMapClient, BuildURLMixin):
    """Client to get today's weather in given city."""

    base_url = "https://api.openweathermap.org/data/2.5/"

    def get_weather_dictionary(self, weather_url: str, parameters: dict) -> dict:
        """Helper to call the endpoint and extract values for both methods, now and long forecast."""

        response = self.call_endpoint(weather_url, parameters)
        if response.status_code == 404:
            raise BadCityException(f"Location {parameters['q']} is not found.")
        elif response.status_code == 401:
            raise BadApiException

        weather_dictionary = response.json()
        return weather_dictionary

    def get_current_weather(
        self,
        city: str,
        country_code: str,
    ) -> list[DayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have today's weather"""
        endpoint = "weather"
        weather_url = self.build_url(self.base_url, endpoint)
        parameters = {"q": f"{city},{country_code}", "units": self.units, "appid": self.api_key}

        weather_dictionary = self.get_weather_dictionary(weather_url, parameters)

        city_timezone = weather_dictionary["timezone"]
        city_name = weather_dictionary["name"]
        country = pycountry.countries.get(alpha_2=weather_dictionary["sys"]["country"]).name
        day = WeatherOpenWeatherForecast.from_weather_dict(
            weather_dictionary, city_timezone, city_name, country
        )
        weather_forecast = []
        weather_forecast.append(day)
        return weather_forecast

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

    def get_long_weather_forecast(
        self, city: str, country_code: str, days: int | None = None
    ) -> list[DayForecast]:
        """First builds the url and call the endpoints, which returns a dict
        then sends the dict to dataclass to have 14 days weather"""
        endpoint = "forecast/daily"
        weather_url = self.build_url(self.base_url, endpoint)
        parameters = {"q": f"{city},{country_code}", "units": self.units, "appid": self.api_key}

        weather_dictionary = self.get_weather_dictionary(weather_url, parameters)

        city_timezone = weather_dictionary["city"]["timezone"]
        city_name = weather_dictionary["city"]["name"]
        country = pycountry.countries.get(alpha_2=weather_dictionary["city"]["country"]).name

        weather_forecast = []
        for index, day_forecast in enumerate(weather_dictionary["list"]):
            one_day_forecast = WeatherOpenWeatherForecast.from_weather_dict(
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

    client = OpenWeatherClient(config)

    if forecast_bool:
        forecast = client.get_long_weather_forecast(city, country_code, days)
    else:
        forecast = client.get_current_weather(city, country_code)  # type: ignore

    return forecast


if __name__ == "__main__":
    print(main())
