import asyncio
import logging

from pyvisa import ResourceManager
from tenacity import retry, wait_random

from app.config import settings


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

    def __init__(
        self,
        telemetry_poll_delay: int = 1,
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
    ) -> None:
        self.file_logger = logging.getLogger(name="file_logger")
        self.telemetry_poll_delay = telemetry_poll_delay
        self.loop = loop

    def init_connection(self):
        self.rm = ResourceManager("")
        connection_address = self.check_connection()
        self.instrument = self.rm.open_resource(connection_address)
        healthcheck = self.instrument.query("*IDN?")
        if healthcheck:
            logging.info("Устройство подключено и готово к работе")

    def check_connection(self) -> str:
        resources = self.rm.list_resources()
        if not resources:
            raise ConnectionError("Отсутствуют подключения")
        return resources[0]

    def channel_turn_on(self, channel_number: int, voltage_level: float, current_level: float) -> None:
        self.instrument.query(
            settings.COMMANDS.set_current_level.format(channel_number=channel_number, value=current_level),
        )
        self.instrument.query(
            settings.COMMANDS.set_voltage_level.format(channel_number=channel_number, value=voltage_level),
        )
        self.instrument.query(settings.COMMANDS.channel_switch.format(channel_number=channel_number, value="ON"))
        logging.info(f"Выходной канал {channel_number} включен")

    def channel_turn_off(self, channel_number) -> None:
        self.instrument.query(settings.COMMANDS.channel_switch.format(channel_number=channel_number, value="OFF"))
        logging.info(f"Выходной канал {channel_number} отключен")

    def channel_state_request(self, channel_number) -> str:
        states = self.instrument.query(settings.COMMANDS.channel_states.format(channel_number=channel_number))
        logging.info(f"Показатели канала {channel_number}: {states}")
        return self.validate_data(states)

    @staticmethod
    def validate_data(data) -> dict:
        data = data.split(" ")
        states = {
            "measure_time": data[0],
            "voltage": data[1],
            "current": data[2],
        }
        return states

    def get_all_channels_states(self) -> dict:
        channels_states = {}
        for channel_number in range(1, settings.NUM_CHANNELS + 1):
            states = self.channel_state_request(channel_number=channel_number)
            channels_states[channel_number] = states
        return channels_states

    def telemetry_poll(self):
        channels_states = self.get_all_channels_states()
        log = "\n"
        for channel, states in channels_states.items():
            log += (
                f"State of checnnel {channel}: "
                + f"Measure time - {states.get('measure_time')}. "
                + f"Voltage: {states.get('voltage')}. Current: {states.get('current')}\n"
            )
        self.file_logger.info(log)

    async def telemetry_poll_task(self):
        while True:
            await self.loop.run_in_executor(executor=None, func=self.telemetry_poll)
            await asyncio.sleep(self.telemetry_poll_delay)

    def close_connection(self):
        self.rm.close()
