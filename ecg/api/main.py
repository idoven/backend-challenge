import logging

from fastapi import FastAPI

from ecg.config import settings
from .routers.auth import router as auth_router
from .routers.admin import router as admin_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_app():
    logger.info(f"Creating server for: {settings.app_name} version {settings.version}")

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
    )
    # Add routers
    app.include_router(prefix="/auth", router=auth_router)
    app.include_router(prefix="/admin", router=admin_router)

    return app
