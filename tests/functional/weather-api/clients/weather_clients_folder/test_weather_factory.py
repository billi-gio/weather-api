from pytest import raises

from weather_api.weather_requests.clients.weather_clients_folder.weather_factory import (
    get_weather_client,
)


def test_weather_client_factory_invalid_provider():
    expected_result = ValueError

    with raises(ValueError, match="Invalid client provider: non_existant_provider") as err:
        get_weather_client("non_existant_provider")
    assert err.type == expected_result
