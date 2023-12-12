"""DB Tables for weather data from api requests."""
from typing import ClassVar, Never

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import (  # type: ignore
    DeclarativeBase,
    Mapped,
    backref,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.properties import RelationshipProperty


class Table(DeclarativeBase):
    pass


class City(Table):
    """Table to store city name and country, by unique combinations"""

    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("city_name", "country"),)

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    city_name: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)


class WeatherRequest(Table):
    """Table to store requests and weather conditions, with date"""

    __tablename__ = "weather_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    weather_conditions: Mapped[str] = mapped_column(String(250), nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    city: ClassVar[RelationshipProperty[Never]] = relationship(
        "City", backref=backref("weather_conditions")
    )


class WeatherForecast(Table):
    """Table to store weather forecast requests."""

    __tablename__ = "weather_forecast"

    id: Mapped[int] = mapped_column(primary_key=True)
    weather_conditions: Mapped[str] = mapped_column(String(250), nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    city: ClassVar[RelationshipProperty[Never]] = relationship(
        "City", backref=backref("weather_forecast")
    )
