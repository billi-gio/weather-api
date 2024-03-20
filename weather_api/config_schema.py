"""Schema to validate config before using."""

from pydantic import BaseModel


class ConfigValidationSchema(BaseModel):
    service: str
    host: str
    port: str
    openweather_api_key: str
    weather_api_com_key: str
    weather_now_provider: str
    weather_forecast_provider: str
    storage_type: str
    database_url: str
    directory_path: str
    weather_records_file_name: str
    cities_file_name: str
