from app.services.power_supply_service import PowerSupplyClient
from app.utils.providers import Singleton


class Container:
    power_supply_client = Singleton(
        PowerSupplyClient,
        telemetry_poll_delay=2,
    )
