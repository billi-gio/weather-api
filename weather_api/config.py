"""Config file to load yaml file and return it as a dict."""
import os

from dotenv import find_dotenv, load_dotenv
import yaml

load_dotenv(find_dotenv())


def load_config() -> dict:
    """Load config yaml file and returns it as a dict."""
    yaml_config_file = os.getenv("CONFIG_FILE")
    if not yaml_config_file:
        raise TypeError("CONFIG FILE env variable is not set.")
    with open(yaml_config_file) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config
