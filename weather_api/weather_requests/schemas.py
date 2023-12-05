from pydantic import BaseModel


class WeatherRequest(BaseModel):
    service: str
    weather_conditions: str
    temperature: float
    # environment: str
