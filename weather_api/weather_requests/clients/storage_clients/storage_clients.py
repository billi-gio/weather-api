"""Clients for data storage."""

from abc import ABC, abstractmethod
import csv
import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.weather_models import City, WeatherRequest


def find_file(path: str) -> bool:
    """Given a file path, checks if the file exists."""
    return os.path.isfile(path)


def find_headers(file_name: str, header: list) -> bool:
    with open(file_name, "r") as f:
        """Checks if given file has the given headers."""
        reader = csv.DictReader(f)
        return header == reader.fieldnames


class BaseStorageClient(ABC):
    @abstractmethod
    def save(self, data: list) -> None:
        """Save object(s) to the storage"""

    @abstractmethod
    def read(
        self,
        filter: dict,
        model: type[City] | type[WeatherRequest] | str,
    ) -> list:
        """Read object(s) from the storage"""


class DBStorageClient(BaseStorageClient):
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = SessionLocal()

    def save(self, data: list) -> None:
        """Save list of entries in db."""
        self.session.add_all(data)
        self.session.commit()

    def read(
        self,
        filter: dict,
        model: type[City] | type[WeatherRequest] | str,
    ) -> list:
        """Read the model with selected filters."""
        if model:
            if filter:
                keys_list = list(filter.keys())
            else:
                raise TypeError("Filter cannot be None for database reading.")
        else:
            raise TypeError("Model cannot be None for database reading.")
        if keys_list:
            filter_conditions_list = []
            for key in keys_list:
                filter_conditions_list.append(getattr(model, key) == filter[key])
            result = self.session.query(model).filter(*filter_conditions_list).all()
        else:
            result = self.session.query(model).all()

        return result


class CSVStorageClient(BaseStorageClient):
    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name

    def save(self, data: list):
        """Save list of entries in a csv file."""
        header = data[0].model_dump().keys()

        with open(self.file_name, "a") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            for entry in data:
                writer.writerow(entry.model_dump())

    def read(
        self,
        filter,
        model: type[City] | type[WeatherRequest] | str,
    ) -> list:
        """Checks if the file exists and if so, returns the content"""
        csv_file = find_file(f"{model}{self.file_name}")
        if csv_file and find_headers(self.file_name, list(filter)):
            rows = []
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    rows.append(row)
                return rows

        else:
            return []
