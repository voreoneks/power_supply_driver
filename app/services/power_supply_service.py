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
        pass

    async def channel_turn_on():
        pass

    async def channel_turn_off():
        pass

    async def channels_state_request():
        pass
