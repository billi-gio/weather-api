from datetime import datetime

from pydantic import BaseModel


class WeatherResponseSchema(BaseModel):
    date: datetime
    weather_conditions: str
    temperature: float
    wind_speed: float
    humidity: float
    city_name: str
    country: str
