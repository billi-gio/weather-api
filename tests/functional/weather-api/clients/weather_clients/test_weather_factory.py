from pytest import raises

from weather_api.weather_requests.clients.weather_clients import weatherapi_client
from weather_api.weather_requests.clients.weather_clients.weather_factory import get_weather_client


def test_weather_client_factory_with_invalid_provider():
    with raises(ValueError, match="non_existant_provider is not a valid provider."):
        get_weather_client("non_existant_provider")


def test_weather_client_factory():
    client = get_weather_client()
    assert isinstance(client, weatherapi_client.WeatherAPIClient)
