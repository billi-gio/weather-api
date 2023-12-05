from sqlalchemy.orm import Session

from weather_api.weather_requests.weather_db_engine import engine
from weather_api.weather_requests.weather_requests_database import City, WeatherRequest


def add_entry(request):
    session = Session(bind=engine)

    entry = (
        session.query(City)
        .filter(request.city == City.city_name, request.country == City.country)
        .one_or_none()
    )
    weather = WeatherRequest(
        date=request.date,
        weather_conditions=request.weather_conditions,
        temperature=request.temperature,
    )

    if entry is None:
        city_entry = City(
            country=request.country,
            city_name=request.city,
        )
        session.add(city_entry)

        weather.city = city_entry

    else:
        weather.city_id = entry.id

    session.add(weather)

    session.commit()
