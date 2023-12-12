from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from weather_api.weather_requests.routes import get_db
from weather_api.weather_requests.weather_requests_database import Table


def test_returns_correct_response(test_client):
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Table.metadata.create_all(bind=engine)

    def override_get_db():
        database = TestingSessionLocal()
        yield database
        database.close()

    test_client.app.dependency_overrides[get_db] = override_get_db

    city_name = "camposampiero"

    response = test_client.get(f"/weather-now/{city_name}")

    assert response.status_code == 200

    Table.metadata.drop_all(bind=engine)
