import logging
from typing import List

from fastapi import APIRouter, Depends

from app.api.models.channel_state import ChannelState
from app.api.models.status import StatusOut
from app.config import settings
from app.container import Container


class PowerSupplyControl:
    api_router = APIRouter(prefix="/control", tags=["PowerSupplyControl"])

    @staticmethod
    @api_router.get(path="/turn_on")
    async def channel_turn_on(
        channel: int, voltage: float, current: float, power_supply_service=Depends(Container.power_supply_client)
    ) -> StatusOut:
        return StatusOut(status=True)

    @staticmethod
    @api_router.get(path="/turn_off")
    async def channel_turn_off(channel: int, power_supply_service=Depends(Container.power_supply_client)) -> StatusOut:
        return StatusOut(status=True)

    @staticmethod
    @api_router.get(path="/state_request")
    async def channels_state_request(power_supply_service=Depends(Container.power_supply_client)) -> List[ChannelState]:
        return StatusOut(status=True)
