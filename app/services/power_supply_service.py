from pyvisa import ResourceManager
import logging


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
    def __init__(self):
        self.rm = ResourceManager('@py')


    def init_device(self):
        connection_address = self.check_connection()
        self.instrument = self.rm.open_resource(connection_address)
        healthcheck = self.instrument.query('*IDN?')
        if healthcheck:
            logging.info('Устройство подключено и готово к работе')

    def check_connection(self):
        resources = self.rm.list_resources()
        if not resources:
            raise ValueError('Отсутствуют подключения')
        return resources[0]

    def channel_turn_on():
        pass

    def channel_turn_off():
        pass

    def channels_state_request():
        pass
