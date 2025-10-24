# -*- coding: utf-8 -*-
"""Low-level control over Thorlabs PM100D digital power meter console.

Authors
-------
    Nick Metelski, October 2022
"""

import locale
import logging
from collections import namedtuple
from datetime import datetime

import pyvisa

logger = logging.getLogger(__name__)

meter_id = namedtuple(
    "PowermeterIdentification",
    ("manufacturer",
     "model",
     "serial_number",
     "firmware",
     "last_calibration")
)
sensor_id = namedtuple(
    "SensorIdentification",
    ("model",
     "serial_number",
     "last_calibration",
     "sensor_flags")
)
FLAG_POWER_SENSOR = 1
FLAG_ENERGY_SENSOR = 2
FLAG_RESPONSE_SETTABLE = 16
FLAG_WAVELENGTH_SETTABLE = 32
FLAG_TAU_SETTABLE = 64
FLAG_TEMP_SENSOR = 256


class ThorlabsPM100D(pyvisa.resources.MessageBasedResource):
    
    def identify(self) -> "PowermeterIdentification":
        """Identifies the head device.

        Returns:
            PowermeterIdentification: a named tuple with power meter head information
        """
        id = self.query("*IDN?").split(',')
        locale.setlocale(locale.LC_ALL, "en_US")
        calib = datetime.strptime(self.query(":CAL:STR?"), '"%d-%b-%Y"')
        id.append(calib)  # noqa
        return meter_id(*id)

    def identify_sensor(self):
        """Identifies the sensor attached to the head.

        Returns:
            SensorIdentification: a named tuple with sensor information
        """
        query = self.query("SYST:SENS:IDN?").split(',')
        ret = query[:3]  # first three elements are model, S/N, calib date
        sensor_codes = ';'.join(query[3:])
        ret.append(sensor_codes)
        return sensor_id(*ret)

    def reset(self) -> int:
        """Resets the device to defaults.
        """
        return self.write("*RST")

    def get_wavelength(self) -> float:
        return float(self.query(":SENS:CORR:WAV?"))

    def set_wavelength(self, wavelength: float) -> int:
        return self.write(f":SENS:CORR:WAV {wavelength}")

    def get_wavelength_range(self):
        wavelength_min = float(self.query(":SENS:CORR:WAV? MIN"))
        wavelength_max = float(self.query(":SENS:CORR:WAV? MAX"))
        return wavelength_min, wavelength_max

    def get_bandwidth(self) -> bool:
        """If returns true, the bandwidth setting is set to LOW.
        Otherwise it is HIGH.
        """
        return bool(int(self.query(":INP:PDI:FILT:STATE?")))

    def set_bandwidth(self, filter_on: bool) -> int:
        """If filter_on is true, this will set the bandwidth to LOW.
        If false, the bandwidth will be HIGH.
        """
        return self.write(f":INP:PDI:FILT:STATE {int(filter_on)}")

    def get_samples_count(self) -> int:
        """Returns the number of samples taken per measurement.

        Each measurement is approximately 3 ms. The samples are averaged by the hardware.

        Returns
            int: the number of samples the result is averaged over
        """
        return int(self.query(":SENS:AVER:COUNT?"))

    def set_samples_count(self, samples: int) -> int:
        """Sets the number of samples taken per measurement.

        Each measurement is approximately 3 ms. The samples are averaged by the hardware.
        """
        return self.write(f"SENS:AVER:COUNT {str(int(samples))}")

    def set_configuration(self, mode: str):
        return self.write(f":CONF:{mode}")

    def get_configuration(self) -> str:
        return self.query(f":CONF?")

    def measure(self):
        return float(self.query(":READ?"))

    def get_power_range(self):
        resp = self.query("SENS:POW:RANG:UPP?")
        return float(resp)

    def set_power_range(self, range: float):
        # un tested
        self.write(f"SENS:POW:RANG:UPP {range}")

    def get_auto_range(self) -> bool:
        resp = self.query(":SENS:POW:RANG:AUTO?")
        return bool(int(float(resp)))

    def set_auto_range(self, auto=True) -> int:
        return self.write(f":SENS:POW:RANG:AUTO {int(auto)}")

    def get_zero_magnitude(self) -> float:
        """Sets current conditions as zero offset for future readings.
        """
        resp = self.query("SENS:CORR:COLL:ZERO:MAGN?")
        return float(resp)

    def init_zero(self):
        """Sets current conditions as zero offset for future readings.

        Warning
            There is no way of resetting the zero value other that full device reset.
            After such a reset, the wavelength and bandwidth options have to be written in again.
            Software-based offsets may be therefore more favourable.
            You can obtain the current zero from `get_zero_magnitude`.
        """
        resp = self.write(":SENSE:AVER:COUNT 1000;:SENS:CORR:COLL:ZERO:INIT;:SENSE:AVER:COUNT 1;")
        return resp


if __name__ == "__main__":
    pass
