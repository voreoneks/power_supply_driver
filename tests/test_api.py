import json

import pytest
from fastapi.testclient import TestClient

from app.api.models.channel_state import ChannelState
from app.api.routers.health_check import HealthCheckRouter
from app.api.routers.power_supply_control import PowerSupplyControlRouter
from tests.mock.mock_data_generator import FakerDataGenerator
from tests.mock.template_objects import TEMPLATE_CHANNEL_STATE


def test_healthcheck(
    client: TestClient,
):
    response = client.get(f"{HealthCheckRouter.api_router.prefix}/")
    assert response.status_code == 200
    assert response.json().get("status")


def test_channel_turn_on(
    client: TestClient,
    mocker,
):
    mocked_channel_turn_on = mocker.patch("app.services.power_supply_service.PowerSupplyClient.channel_turn_on")
    params = {
        "channel": 1,
        "voltage": 12.5,
        "current": 1.2,
    }
    response = client.get(f"{PowerSupplyControlRouter.api_router.prefix}/turn_on", params=params)
    assert response.status_code == 200
    assert response.json().get("status")


def test_channel_turn_off(
    client: TestClient,
    mocker,
):
    mocked_channel_turn_on = mocker.patch("app.services.power_supply_service.PowerSupplyClient.channel_turn_off")
    params = {
        "channel": 1,
    }
    response = client.get(f"{PowerSupplyControlRouter.api_router.prefix}/turn_off", params=params)
    assert response.status_code == 200
    assert response.json().get("status")


def test_channels_state_request(
    client: TestClient,
    faker_generator: FakerDataGenerator,
    mocker,
):
    mocked_channel_turn_on = mocker.patch("app.services.power_supply_service.PowerSupplyClient.channel_state_request")
    fake_data = faker_generator.get_fake_object(TEMPLATE_CHANNEL_STATE)
    mocked_channel_turn_on.return_value = fake_data
    response = client.get(f"{PowerSupplyControlRouter.api_router.prefix}/state_request")
    assert response.status_code == 200
    response_data = response.json()
    expected_data = []
    for i in range(1, 5):
        fake_data.update({"number": i})
        expected_data.append(json.loads(ChannelState.model_validate(fake_data).model_dump_json()))
    assert response_data == expected_data
