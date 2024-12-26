from app.config import settings
from app.services.power_supply_service import PowerSupplyClient
from app.utils.providers import Singleton


class Container:
    power_supply_client = Singleton(
        PowerSupplyClient,
    )
