import pytest

from app.services.power_supply_service import PowerSupplyClient


@pytest.mark.parametrize(
    "data, result",
    [
        (
            "1987-11-05T17:42:44 64922353520409.9 -913705313606.17",
            {
                "measure_time": "1987-11-05T17:42:44",
                "voltage": "64922353520409.9",
                "current": "-913705313606.17",
            },
        ),
        (
            "1987-11-05T17:42:44 0 -1",
            {
                "measure_time": "1987-11-05T17:42:44",
                "voltage": "0",
                "current": "-1",
            },
        ),
        (
            "13187812 64922353520409.9 -1",
            {
                "measure_time": "13187812",
                "voltage": "64922353520409.9",
                "current": "-1",
            },
        ),
    ],
)
def test_validate_data(
    data,
    result,
    power_supply_service: PowerSupplyClient,
):
    assert power_supply_service.validate_data(data) == result
