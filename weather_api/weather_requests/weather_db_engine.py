from sqlalchemy import create_engine

from weather_api.weather_requests.weather_models import Table

engine = create_engine("sqlite:///weatherclient.db", echo=True)

Table.metadata.create_all(bind=engine)
