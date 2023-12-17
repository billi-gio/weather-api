from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeatherRequestSchema(BaseModel):
    weather_conditions: str
    temperature: float
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None


class WeatherForecast(BaseModel):
    weather_conditions: str
    temperature: float
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
