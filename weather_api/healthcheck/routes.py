from fastapi import APIRouter, Depends, status

from weather_api.config import load_config
from weather_api.healthcheck.schemas import ServiceHealthcheck

router = APIRouter()


@router.get(
    "/healthcheck",
    response_model=ServiceHealthcheck,
    status_code=status.HTTP_200_OK,
    tags=["healthcheck"],
)
async def healthcheck(config=Depends(load_config)) -> dict[str, str]:
    return {
        "service": config.service,
        # "environment": config.environment,
    }
