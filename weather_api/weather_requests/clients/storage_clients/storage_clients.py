"""Clients for data storage."""

from abc import ABC, abstractmethod
from os import listdir
import csv

from pydantic import BaseModel
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.weather_models import City, WeatherRequest


def find_if_file_exist(path: str, header: list) -> str | None:
    """Check if the csv file with correct type of headers exists."""
    for file in listdir(path):
        if file.endswith(".csv"):
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                if header == reader.fieldnames:
                    return f.name
    else:
        return None


class BaseStorageClient(ABC):
    @abstractmethod
    def save(self, data: list) -> None:
        """Save object(s) to the storage"""

    @abstractmethod
    def read(
        self,
        filter: dict,
        model: type[City] | type[WeatherRequest] | None = None,
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
        model: type[City] | type[WeatherRequest] | None = None,
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
    def __init__(self, directory: str, name_to_use_if_file_doesnot_exist: str) -> None:
        super().__init__()
        self.directory = directory
        self.file_name = name_to_use_if_file_doesnot_exist

    def save(self, data: list):
        """Save list of entries in a csv file."""
        if isinstance(data[0], BaseModel):
            header = data[0].model_dump().keys()

        csv_file = find_if_file_exist(self.directory, list(header))

        if csv_file:
            with open(csv_file, "a") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                for entry in data:
                    writer.writerow(entry.model_dump())

        else:
            with open(self.file_name, "w") as file:
                csv_writer = csv.DictWriter(file, fieldnames=header)
                csv_writer.writeheader()
                for entry in data:
                    csv_writer.writerow(entry.model_dump())

    def read(
        self,
        filter,
        model: type[City] | type[WeatherRequest] | None = None,
    ) -> list:
        csv_file = find_if_file_exist(self.directory, list(filter.keys()))

        if csv_file:
            rows = []
            with open(csv_file, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    rows.append(row)
                return rows

        else:
            return []
