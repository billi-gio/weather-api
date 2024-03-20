from unittest.mock import patch

from pytest import raises

from weather_api.weather_requests.clients.storage_clients.storage_factory import (
    DBStorageClient,
    get_storage_client,
)


def test_storage_client_factory_raises_with_invalid_provider():
    with raises(ValueError, match="non_existant_storage_type is not a valid storage type."):
        get_storage_client("non_existant_storage_type")


@patch("weather_api.weather_requests.weather_db_engine.get_engine")
def test_storage_client_factory(engine, override_get_engine):
    engine.return_value = override_get_engine
    client = get_storage_client("database")

    assert isinstance(client, DBStorageClient)
