import logging
from typing import List
import asyncio

from fastapi import APIRouter, Depends

from app.api.models.channel_state import ChannelState
from app.api.models.status import StatusOut
from app.config import settings
from app.container import Container
from app.services.power_supply_service import PowerSupplyClient


class PowerSupplyControl:
    api_router = APIRouter(prefix="/control", tags=["PowerSupplyControl"])

    @staticmethod
    @api_router.get(path="/turn_on")
    async def channel_turn_on(
        channel: int, voltage: float, current: float, power_supply_service: PowerSupplyClient=Depends(Container.power_supply_client)
    ) -> StatusOut:
        await asyncio.get_event_loop().run_in_executor(None, power_supply_service.channel_turn_on, channel, voltage, current)
        return StatusOut(status=True)

    @staticmethod
    @api_router.get(path="/turn_off")
    async def channel_turn_off(channel: int, power_supply_service: PowerSupplyClient=Depends(Container.power_supply_client)) -> StatusOut:
        await asyncio.get_event_loop().run_in_executor(None, power_supply_service.channel_turn_off, channel)
        return StatusOut(status=True)

    @staticmethod
    @api_router.get(path="/state_request")
    async def channels_state_request(power_supply_service: PowerSupplyClient=Depends(Container.power_supply_client)) -> List[ChannelState]:
        channel_states = []
        states = await asyncio.get_event_loop().run_in_executor(None, power_supply_service.get_all_channels_states)
        for channel, state in states.items():
            states = state.split(" ")
            channel_state = {
                'number': channel,
                'measure_time': states[0],
                'voltage': states[1],
                'current': state[2],
            }
            channel_states.append(ChannelState.model_validate(channel_state))
        return channel_states
