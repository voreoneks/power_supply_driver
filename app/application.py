import logging.config

from fastapi import FastAPI

from app.api.routers.health_check import HealthCheckRouter
from app.config import settings

logging.config.dictConfig(settings.LOGGING)

app = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description="Драйвер для работы с промышленным 4-х канальным источником питания",
)
app.include_router(HealthCheckRouter().api_router)
