"""Clients for data storage."""

from abc import ABC, abstractmethod
import csv
import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from weather_api.config import load_config
from weather_api.weather_requests.weather_models import City, WeatherRequest


def retrieve_file_name(directory_path: str, model: type[City] | type[WeatherRequest]) -> str:
    """Retrieves the file name."""
    if isinstance(model, City) or isinstance(model, type(City)):
        file_path = f"{directory_path}{load_config().cities_file_name}"
    elif isinstance(model, WeatherRequest) or isinstance(model, type(WeatherRequest)):
        file_path = f"{directory_path}{load_config().weather_records_file_name}"
    return file_path


def file_exists(file_path: str) -> bool:
    """Given a file path, checks if the file exists."""
    if os.path.isfile(file_path):
        return True
    else:
        return False


def headers_exist(file_name: str, headers: list[str]) -> bool:
    """Checks if given file has the given headers."""
    with open(file_name, "r") as f:
        reader = csv.DictReader(f)
        for header in headers:
            if reader.fieldnames and header not in reader.fieldnames:
                return False
        return True


def check_row_match_filters(row: dict[str, str], filters: dict[str, str]) -> bool:
    """Given a csv row, check if the values in filters match with the ones in the row."""
    for column, value in filters.items():
        if row.get(column) != value:
            return False
    return True


class BaseStorageClient(ABC):
    @abstractmethod
    def save(self, data: list) -> None:
        """Save object(s) to the storage"""

    @abstractmethod
    def read(
        self,
        filter: dict,
        model: type[City] | type[WeatherRequest],
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
        model: type[City] | type[WeatherRequest],
    ) -> list:
        """Read the model with selected filters."""
        keys_list = list(filter.keys())
        if keys_list:
            filter_conditions_list = []
            for key in keys_list:
                filter_conditions_list.append(getattr(model, key) == filter[key])
            result = self.session.query(model).filter(*filter_conditions_list).all()
        else:
            result = self.session.query(model).all()

        return result


class CSVStorageClient(BaseStorageClient):
    def __init__(self, directory_path: str) -> None:
        super().__init__()
        self.directory_path = directory_path

    def save(self, data: list):
        """Append to an existing csv file or in a created file a list of entries."""
        for entry in data:
            file_name = retrieve_file_name(self.directory_path, entry)
            headers = [column.key for column in entry.__table__.columns]
            if file_exists(file_name):
                with open(file_name, "a") as file:
                    writer = csv.DictWriter(file, fieldnames=headers)
                    writer.writerow({field: getattr(entry, field) for field in headers})
            else:
                with open(file_name, "w") as file:
                    writer = csv.DictWriter(file, fieldnames=headers)
                    writer.writeheader()
                    writer.writerow({field: getattr(entry, field) for field in headers})

    def read(
        self,
        filter: dict,
        model: type[City] | type[WeatherRequest],
    ) -> list:
        """Checks if the file exists and if so, checks if a certain entry is already in the file."""
        csv_file = retrieve_file_name(self.directory_path, model)
        rows = []
        if file_exists(csv_file) and headers_exist(csv_file, list(filter)):
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if check_row_match_filters(row, filter):
                        rows.append(row)
                        break
        return rows
