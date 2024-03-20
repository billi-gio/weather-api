"""Config file to load yaml file and return it as a dict."""
import os

from dotenv import find_dotenv, load_dotenv
import yaml

from weather_api.config_schema import ConfigValidationSchema

load_dotenv(find_dotenv())


def load_config() -> ConfigValidationSchema:
    """Load config yaml file and returns it as a dict."""
    yaml_config_file = os.getenv("CONFIG_FILE")
    if not yaml_config_file:
        raise TypeError("CONFIG FILE env variable is not set.")
    with open(yaml_config_file) as config_file:
        config_load = yaml.safe_load(config_file)
    config = ConfigValidationSchema(
        service=config_load["service"],
        host=config_load["host"],
        port=config_load["port"],
        openweather_api_key=config_load["openweather_api_key"],
        weather_api_com_key=config_load["weather_api_com_key"],
        weather_now_provider=config_load["weather_now_provider"],
        weather_forecast_provider=config_load["weather_forecast_provider"],
        storage_type=config_load["storage_type"],
        database_url=config_load["database_url"],
        directory_path=config_load["local_directory_for_csv"],
        weather_records_file_name=config_load["weather_records_file_name"],
        cities_file_name=config_load["cities_file_name"],
    )
    return config
