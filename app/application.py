import logging.config

from fastapi import FastAPI

from app.api.routers.health_check import HealthCheckRouter
from app.api.routers.power_supply_control import PowerSupplyControl
from app.config import settings

logging.config.dictConfig(settings.LOGGING)

app = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description="Драйвер для работы с промышленным 4-х канальным источником питания",
)
app.include_router(HealthCheckRouter().api_router)
app.include_router(PowerSupplyControl().api_router)
