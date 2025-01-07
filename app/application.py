import asyncio
import logging.config
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.routers.health_check import HealthCheckRouter
from app.api.routers.power_supply_control import PowerSupplyControl
from app.config import settings
from app.services.power_supply_service import PowerSupplyClient
from app.container import Container
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncGenerator:
    
    power_supply: PowerSupplyClient = Container.power_supply_client()
    loop = asyncio.get_event_loop()
    loop.create_task(power_supply.telemetry_poll_task())
    logging.info("Инициализация startup callbacks прошла успешно")

    yield

    power_supply.close_connection()
    logging.info("Инициализация shutdown callbacks прошла успешно")


logging.config.dictConfig(settings.LOGGING)


app = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description="Драйвер для работы с промышленным 4-х канальным источником питания",
    lifespan=_lifespan,
)
app.include_router(HealthCheckRouter().api_router)
app.include_router(PowerSupplyControl().api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS.allow_origins,
    allow_methods=settings.CORS.allow_methods,
    allow_headers=settings.CORS.allow_headers,
    allow_credentials=settings.CORS.allow_credentials,
    expose_headers=settings.CORS.expose_headers,
    max_age=settings.CORS.max_age,
)
