"""Factory for clients for data storage."""

from weather_api.config import StorageType
from weather_api.weather_requests.clients.storage_clients_folder.storage_clients import (
    DBStorageClient,
)


def get_storage_client(storage_type: StorageType) -> DBStorageClient:
    """Return client depending on storage type chosen."""
    if storage_type == StorageType.DATABASE:
        return DBStorageClient()

    else:
        raise ValueError(f"Invalid storage type: {storage_type}.")
