# -*- coding: utf-8 -*-
"""Low-level control over Thorlabs PM100 digital power meter console.

This is for the PM100 (not PM100D). The PM100 uses different RS-232 commands.
"""

import logging
from collections import namedtuple
from datetime import datetime

import pyvisa

logger = logging.getLogger(__name__)

meter_id = namedtuple(
    "PowermeterIdentification",
    ("manufacturer", "model", "serial_number", "firmware")
)

sensor_info = namedtuple(
    "SensorInfo",
    ("serial_number", "name", "description", "max_power")
)


class ThorlabsPM100(pyvisa.resources.MessageBasedResource):
    """Driver for Thorlabs PM100 optical power meter.
    
    Uses RS-232 commands as documented in PM100 manual.
    """
    
    def identify(self) -> "PowermeterIdentification":
        """Identifies the power meter device.

        Returns:
            PowermeterIdentification: named tuple with device information
        """
        id_str = self.query("*IDN?")
        parts = id_str.strip().split(',')
        # PM100 returns: Manufacturer, Model, Serial number, Firmware level
        return meter_id(*parts)

    def identify_sensor(self):
        """Identifies the sensor attached to the head.

        Returns:
            SensorInfo: named tuple with sensor information
        """
        head_info = self.query(":HEAD:INFO?")
        parts = head_info.strip().split(',')
        # Returns: serial number, head name, head description, maximum power
        return sensor_info(*parts)

    def reset(self) -> int:
        """Resets the device to defaults."""
        return self.write("*RST")

    def get_wavelength(self) -> float:
        """Get the current wavelength correction setting in meters."""
        return float(self.query(":WAVELENGTH?"))

    def set_wavelength(self, wavelength: float) -> int:
        """Set the wavelength correction in meters."""
        return self.write(f":WAVELENGTH {wavelength}")

    def get_wavelength_range(self):
        """Get the min and max wavelength range for the sensor."""
        range_str = self.query(":WAVELENGTH:RANGE?")
        parts = range_str.strip().split(',')
        wavelength_min = float(parts[0])
        wavelength_max = float(parts[1])
        return wavelength_min, wavelength_max

    def get_line_filter(self) -> str:
        """Get the line frequency filter setting (50HZ or 60HZ)."""
        return self.query(":FILTER?").strip()

    def set_line_filter(self, frequency: str) -> int:
        """Set the line frequency filter (50HZ or 60HZ)."""
        return self.write(f":FILTER {frequency}")

    def measure(self):
        """Read the current power measurement in Watts."""
        return float(self.query(":POWER?"))

    def get_photocurrent(self) -> float:
        """Get the photodiode current in Amperes (photodiode sensors only)."""
        return float(self.query(":PHOTOCURRENT?"))

    def get_photovoltage(self) -> float:
        """Get the thermal sensor voltage in Volts (thermal sensors only)."""
        return float(self.query(":PHOTOVOLTAGE?"))

    def get_darkcurrent(self) -> float:
        """Get the dark current offset in Amperes (photodiode sensors only)."""
        return float(self.query(":DARKCURRENT?"))

    def set_darkcurrent(self, current: float) -> int:
        """Set the dark current offset in Amperes (photodiode sensors only)."""
        return self.write(f":DARKCURRENT {current}")

    def get_darkvoltage(self) -> float:
        """Get the dark voltage offset in Volts (thermal sensors only)."""
        return float(self.query(":DARKVOLTAGE?"))

    def set_darkvoltage(self, voltage: float) -> int:
        """Set the dark voltage offset in Volts (thermal sensors only)."""
        return self.write(f":DARKVOLTAGE {voltage}")

    def get_attenuation(self) -> float:
        """Get the user attenuation correction in dB."""
        return float(self.query(":ATTENUATION?"))

    def set_attenuation(self, attenuation_db: float) -> int:
        """Set the user attenuation correction in dB."""
        return self.write(f":ATTENUATION {attenuation_db}")

    # Compatibility methods to match PM100D interface
    def get_configuration(self) -> str:
        """Compatibility method - PM100 doesn't have configuration modes."""
        return "POW"  # Always power mode
    
    def set_configuration(self, mode: str):
        """Compatibility method - PM100 doesn't have configuration modes."""
        pass  # PM100 doesn't support this

    def get_bandwidth(self) -> bool:
        """Compatibility method - PM100 uses line filter instead."""
        # Return True for LOW bandwidth (50/60Hz filtering enabled)
        return True
    
    def set_bandwidth(self, filter_on: bool) -> int:
        """Compatibility method - PM100 uses line filter instead."""
        # PM100 doesn't have this setting
        pass

    def get_auto_range(self) -> bool:
        """PM100 doesn't support auto-range query."""
        return False
    
    def set_auto_range(self, auto=True) -> int:
        """PM100 doesn't support auto-range setting."""
        pass

    def get_power_range(self):
        """PM100 doesn't support power range query."""
        return 0.0
    
    def set_power_range(self, range: float):
        """PM100 doesn't support power range setting."""
        pass

    def get_zero_magnitude(self) -> float:
        """Get the current zero offset."""
        try:
            return self.get_darkcurrent()
        except:
            return self.get_darkvoltage()

    def init_zero(self):
        """Zero the sensor - not directly supported by PM100.
        
        Use the menu system on the device instead.
        """
        logger.warning("PM100 doesn't support init_zero via RS-232. Use the device menu.")
        pass


if __name__ == "__main__":
    pass