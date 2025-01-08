import logging
from asyncio import get_running_loop, new_event_loop, set_event_loop

import pytest as pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routers.health_check import HealthCheckRouter
from app.api.routers.power_supply_control import PowerSupplyControlRouter
from app.container import Container
from tests.mock.mock_data_generator import FakerDataGenerator


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(HealthCheckRouter().api_router)
    app.include_router(PowerSupplyControlRouter().api_router)
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def logger():
    return logging.getLogger("tests")


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    try:
        loop = get_running_loop()
    except RuntimeError:
        loop = new_event_loop()
    set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def faker_generator():
    return FakerDataGenerator()


@pytest.fixture
def power_supply_service():
    return Container.power_supply_client()
