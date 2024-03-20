"""Factory for clients for data storage."""

from enum import Enum
import os

from weather_api.weather_requests.clients.storage_clients.storage_clients import (
    CSVStorageClient,
    DBStorageClient,
)
from weather_api.weather_requests.weather_db_engine import get_engine
import weather_api.config as config


class StorageType(str, Enum):
    DATABASE = "database"
    CSV = "csv"


def get_storage_client(storage_type: StorageType) -> DBStorageClient | CSVStorageClient:
    """Return client depending on storage type chosen."""
    if storage_type == StorageType.DATABASE:
        configuration = get_engine(config.load_config().database_url)
        return DBStorageClient(engine=configuration)
    elif storage_type == StorageType.CSV:
        directory_path = os.getenv(config.load_config().directory_path)
        if directory_path:
            return CSVStorageClient(
                directory_path,
            )
        else:
            raise ValueError(f"{directory_path} is not a valid directory path.")
    else:
        raise ValueError(f"{storage_type} is not a valid storage type.")
