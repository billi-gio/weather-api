"""Factory for clients for data storage."""

from enum import Enum

from weather_api.weather_requests.clients.storage_clients.storage_clients import DBStorageClient
from weather_api.weather_requests.weather_db_engine import get_engine
import weather_api.config as config


class StorageType(str, Enum):
    DATABASE = "database"
    CSV = "csv"


def get_storage_client(storage_type: StorageType) -> DBStorageClient:
    """Return client depending on storage type chosen."""
    if storage_type == StorageType.DATABASE:
        configuration = get_engine(config.ApplicationConfig.database_url)
        return DBStorageClient(engine=configuration)

    else:
        raise ValueError(f"{storage_type} is not a valid storage type.")
