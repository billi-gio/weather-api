from sqlalchemy import Engine, create_engine

from weather_api.weather_requests.weather_models import Table


def get_engine(database_url: str | None = None) -> Engine:
    engine = create_engine(database_url, echo=True)
    Table.metadata.create_all(bind=engine)
    return engine
