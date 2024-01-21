from pytest import raises

from weather_api.weather_requests.clients.storage_clients_folder.storage_factory import (
    get_storage_client,
)


def test_weather_client_factory_invalid_provider():
    expected_result = ValueError

    with raises(ValueError, match="Invalid storage type: non_existant_storage_type") as err:
        get_storage_client("non_existant_storage_type")
    assert err.type == expected_result
