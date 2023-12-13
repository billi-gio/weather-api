from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from weather_api.weather_requests.weatherclient import DayForecast


class WeatherRequestSchema(BaseModel):
    weather_conditions: str
    temperature: float
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None


class WeatherForecast(BaseModel):
    forecast: Optional[List]
