"""Clients for data storage."""

from abc import ABC, abstractmethod

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from weather_api.weather_requests.weather_models import City, WeatherRequest
import weather_api.config as config


class BaseStorageClient(ABC):
    @abstractmethod
    def save(self, data: list) -> None:
        """Save object(s) to the storage"""

    @abstractmethod
    def read(self, model: type[City] | type[WeatherRequest], filter: dict) -> list:
        """Read object(s) from the storage"""


class DBStorageClient(BaseStorageClient):
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.session: Session = next(config.get_db(engine))

    def save(self, data: list) -> None:
        """Save list of entries in db."""
        self.session.add_all(data)
        self.session.commit()

    def read(self, model: type[City] | type[WeatherRequest], filter: dict) -> list:
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
