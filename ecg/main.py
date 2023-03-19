import logging

from fastapi import FastAPI

from .config import settings
from .views import router as ecg_router

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


def get_app():
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
    )
    app.include_router(ecg_router)

    logger.info(f"Creating server for: {settings.app_name} version {settings.version}")
    return app


app = get_app()
