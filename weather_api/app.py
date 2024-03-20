import os
import shutil

from fastapi import FastAPI
from loguru import logger

from weather_api.config import load_config
from weather_api.routes import api_router


def create_app() -> FastAPI:
    configuration = load_config()
    app = FastAPI(title=configuration.service, docs_url=None, redoc_url=None)
    app.include_router(api_router)
    logger.info("Started %s %s", configuration.service)
    return app


def start_server(config) -> None:
    args = [
        shutil.which("gunicorn"),
        "gunicorn",
        "weather_api.app:create_app",
        "-b",
        f"{config.host}:{config.port}",
    ]
    os.execl(*[str(v) for v in args])


if __name__ == "__main__":
    configuration = load_config()
    start_server(configuration)
