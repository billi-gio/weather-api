from fastapi import APIRouter

from weather_api.healthcheck.routes import router as healtcheck_router
from weather_api.weather_requests.routes import weather_router

api_router = APIRouter()

api_router.include_router(healtcheck_router)
api_router.include_router(weather_router)
