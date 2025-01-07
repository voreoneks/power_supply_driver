import logging

from pyvisa import ResourceManager
import asyncio
from app.config import settings
from typing import List
from tenacity import retry, wait_random


class PowerSupplyClient:
    """
    :SOURce[1|2|3|4]:CURRent <NRf>
    Sets the current level. Example :SOURce2:CURRent 1.0005

    :SOURce[1|2|3|4]:VOLTage < NRf >
    Sets the output voltage amplitude. Example :SOURce2:VOLTage 5.321

    :OUTPut[1|2|3|4][:STATe] <b>
    Turns the output on or off. Example :OUTPut:STATe ON

    :MEASure[1|2|3|4]:ALL?
    Query the all measurement functions. Example :MEASure2:ALL?

    """

    def __init__(self, telemetry_poll_delay: int = 1, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> None:
        self.file_logger = logging.getLogger(name='file_logger')
        self.telemetry_poll_delay = telemetry_poll_delay
        self.loop = loop
        self.rm = ResourceManager("")
        connection_address = self.check_connection()
        self.instrument = self.rm.open_resource(connection_address)
        healthcheck = self.instrument.query("*IDN?")
        if healthcheck:
            logging.info("Устройство подключено и готово к работе")

    @retry(wait=wait_random(min=1, max=10), reraise=True)
    def check_connection(self) -> str:
        resources = self.rm.list_resources()
        if not resources:
            raise ConnectionError("Отсутствуют подключения")
        return resources[0]

    def channel_turn_on(self, channel_number: int, voltage_level: float, current_level: float) -> None:
        self.instrument.query(settings.COMMANDS.set_current_level.format(channel_number=channel_number, value=current_level))
        self.instrument.query(settings.COMMANDS.set_voltage_level.format(channel_number=channel_number, value=voltage_level))
        self.instrument.query(settings.COMMANDS.channel_switch.format(channel_number=channel_number, value="ON"))
        logging.info(f"Выходной канал {channel_number} включен")

    def channel_turn_off(self, channel_number) -> None:
        self.instrument.query(settings.COMMANDS.channel_switch.format(channel_number=channel_number, value="OFF"))
        logging.info(f"Выходной канал {channel_number} отключен")

    def channel_state_request(self, channel_number) -> str:
        state = self.instrument.query(settings.COMMANDS.channel_states.format(channel_number=channel_number))
        logging.info(f"Показатели канала {channel_number}: {state}")
        return state
    
    def get_all_channels_states(self) -> dict:
        channels_states = {}
        for channel_number in range(settings.NUM_CHANNELS):
            state = self.channel_states_request(channel_number=channel_number)
            channels_states[channel_number] = state
        return channels_states

    def telemetry_poll(self):
        channels_states = self.get_all_channels_states()
        log = "\n"
        for channel, state in channels_states.items():
            log += f"State of checnnel {channel}: {state}\n"
        self.file_logger.info(log)

    async def telemetry_poll_task(self):
        while True:
            await self.loop.run_in_executor(executor=None, func=self.telemetry_poll)
            await asyncio.sleep(self.telemetry_poll_delay)

    def close_connection(self):
        self.rm.close()
