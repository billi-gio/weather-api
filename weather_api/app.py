import os
import shutil

from fastapi import FastAPI
from loguru import logger

from weather_api.config import load_application_config
from weather_api.routes import api_router


def create_app() -> FastAPI:
    config = load_application_config()

    app = FastAPI(title=config.service, docs_url=None, redoc_url=None)
    app.include_router(api_router)

    logger.info("Started %s %s", config.service)
    return app


def start_server(host: str, port: str) -> None:
    args = [
        shutil.which("gunicorn"),
        "gunicorn",
        "weather_api.app:create_app",
        "-b",
        f"{host}:{port}",
    ]
    os.execl(*[str(v) for v in args])


if __name__ == "__main__":
    application_config = load_application_config()
    start_server(application_config.host, application_config.port)
