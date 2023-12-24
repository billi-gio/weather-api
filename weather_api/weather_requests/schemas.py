from typing import Optional

from pydantic import BaseModel


class WeatherRequestSchema(BaseModel):
    weather_conditions: str
    temperature: float
    wind_speed: float
    humidity: float


class WeatherForecast(BaseModel):
    date: str
    weather_conditions: str
    temperature: float
    wind_speed: float
    humidity: float
