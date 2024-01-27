from pytest import raises

from weather_api.weather_requests.clients.storage_clients.storage_factory import get_storage_client


def test_storage_client_factory_raises_with_invalid_provider():
    with raises(ValueError, match="non_existant_storage_type is not a valid storage type."):
        get_storage_client("non_existant_storage_type")
