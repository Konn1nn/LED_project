#
#
#

"""
ads1015/1115 driver for Raspberry Pi
"""

import time
from smbus import SMBus
import explorerhat


def i2c_bus_id():
    """Find the SMBUS"""
    revision = None
    with open('/proc/cpuinfo', 'r') as cpuinfo:
        revision = ([l[12:-1] for l in cpuinfo.readlines() if l[:8] == "Revision"] + ['0000'])[0]
    return 1 if int(revision, 16) >= 4 else 0

i2c = SMBus(i2c_bus_id())

REG_CONV = 0x00
REG_CFG = 0x01



channel_map = {
        0: 0x4000,
        1: 0x5000,
        2: 0x6000,
        3: 0x7000
}

programmable_gain_map = {
        6144: 0x0000,  # 2/3
        4096: 0x0200,  # 1
        2048: 0x0400,  # 2
        1024: 0x0600,  # 4
        512: 0x0800,   # 8
        256: 0x0A00    # 16
}

# These names represent the full range (cf Table 1, page 13)
PGA_6_144V = 6144
PGA_4_096V = 4096
PGA_2_048V = 2048
PGA_1_024V = 1024
PGA_0_512V = 512
PGA_0_256V = 256



class ADS1x15:
    """Base class to ADS1x15 family of ADC."""
    def __init__(self, channel):
        assert channel in [0,1,2,3]

        self.address = 0x48
        self._sample_rate = 250 # common rate between both chips.
        self._programmable_gain = 6144
        self._channel = channel

    def __busy(self):
        """See if the line is busy"""
        data = i2c.read_i2c_block_data(self.address, REG_CFG)
        status = (data[0] << 8) | data[1]
        return (status & (1 << 15)) == 0

    @property
    def channel(self):
        """The channel of the controlled ADC"""
        return self._channel

    @property
    def sample_rate(self):
        """The sample rate in samples per second"""
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, rate):
        """Set the sample rate."""
        if rate not in self.sample_rates:
            raise AttributeError
        self._sample_rate = rate

    def samples_per_second_map(self, sample_rate):
        """Map the sample rate to its bit mask"""
        raise NotImplementedError

    @property
    def sample_rates(self):
        """Get a list of all supported sample rates."""
        raise NotImplementedError

    @property
    def programmable_gain(self):
        """The current rogrammable gain"""
        return self._programmable_gain

    @programmable_gain.setter
    def programmable_gain(self, gain):
        """Set the programmable gain."""
        if gain not in programmable_gain_map.keys():
            raise AttributeError
        self._programmable_gain = gain

    def read_se_adc(self):
        """Read data from the ADS1x15 using i2c in one-shot mode"""
        # Sane defaults:
        # Disable comparator and set ALERT/RDY pin to high-impedance
        config = 0x0003
        # Single-shot mode or power-down state
        config |= 0x0100
        config |= self.samples_per_second_map(self._sample_rate)
        config |= channel_map[self._channel]
        config |= programmable_gain_map[self._programmable_gain]
        #  Start a single conversion (when in power-down state)
        config |= 0x8000

        i2c.write_i2c_block_data(self.address, REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])

        while self.__busy():
            time.sleep(1.0 / self._sample_rate)

        data = i2c.read_i2c_block_data(self.address, REG_CONV)
        return data


class ADS1015(ADS1x15):
    """This class defines the ADS1015 specific code, among others,
    the conversion from 12bit to float."""

    _SAMPLE_RATE_MAP = {
        128: 0x0000,
        250: 0x0020,
        490: 0x0040,
        920: 0x0060,
        1600: 0x0080,
        2400: 0x00A0,
        3300: 0x00C0
    }

    def __init__(self, channel):
        super().__init__(channel)

    def samples_per_second_map(self, sample_rate):
        """Get the configuration for the samples per second."""
        return ADS1015._SAMPLE_RATE_MAP[sample_rate]

    @property
    def sample_rates(self):
        return ADS1015._SAMPLE_RATE_MAP.keys()

    def read(self):
        """Read a value of the ADS1015."""
        data = self.read_se_adc()
        value = (data[0] << 4) | (data[1] >> 4)
        if value & 0x0800:  # Check and apply sign bit
            value -= 1 << 12
        value /= 2047.0
        value *= float(self._programmable_gain)
        value /= 1000.0
        return max(0, value)



class ADS1115(ADS1x15):
    """This class defines the ADS1115 specific code, among others,
    the conversion from 16bit to float."""
    _SAMPLE_RATE_MAP = {
        8: 0x0000,
        16: 0x0020,
        32: 0x0040,
        64: 0x0060,
        128: 0x0080,
        250: 0x00A0,
        475: 0x00C0,
        860: 0x00E0,
    }

    def __init__(self, channel):
        super().__init__(channel)

    def samples_per_second_map(self, sample_rate):
        """Get the configuration for the samples per second."""
        return ADS1115._SAMPLE_RATE_MAP[sample_rate]

    @property
    def sample_rates(self):
        return ADS1115._SAMPLE_RATE_MAP.keys()

    def read(self):
        """Read a value of the ADS1115."""
        data = self.read_se_adc()
        value = (data[0] << 8) | data[1]
        if value & 0x8000:  # Check and apply sign bit
            value -= 1 << 16
        value /= 32767.0
        value *= float(self._programmable_gain)
        value /= 1000.0
        return max(0, value)


class TunableAnalogInput(explorerhat.AnalogInput):
    """A reimplementation of the AnalogInput for the explorer hat.
    To use it, owerwrite the AnalogInput variable by an instance
    of TunableAAnologInput, e.g.

    explorterhat.analog.one = TunableAnalogInput(3, 250, PGA_4_096V)
    """
    def __init__(self, channel, sample_rate, programmable_gain):
        super().__init__(channel)
        self.pin = ADS1015(channel)
        self.pin.sample_rate = sample_rate
        self.pin.programmable_gain = programmable_gain

    def read(self):
        """Read from the pin at a specified sample rate and a specific gain"""
        return self.pin.read()
