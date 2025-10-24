# -*- coding: utf-8 -*-
"""Control of Thorlabs Powermeter.

Authors
-------
    pymucl, Jul 2019
    Nick Metelski, October 2022
"""
from typing import List

import pyvisa

import ScopeFoundry as SFT

try:
    from .thorlabs_PM100 import ThorlabsPM100
except Exception as e:
    print('could not import Thorlabs powermeter device drivers')
    print(e)


class ThorlabsPowerMeterHW(SFT.HardwareModule):
    port = SFT.ObjectParameter(
        name='Port',
        dtype=str
    )
    wavelength = SFT.PhysicalParameter(
        name='Wavelength',
        unit="nm",
        dtype=float,
        range=SFT.MinMaxRangeType(min=400.0, max=1100.0)
    )
    configuration = SFT.PhysicalParameter(
        name='Measurement configuration',
        dtype=str,
        doc="The nature of the reading parameter (power, current, etc).",
        range=SFT.ChoiceRangeType(**{"Power": "POW", "Current": "CURR"})
    )
    reading = SFT.PhysicalParameter(
        name='Reading',
        dtype=float,
        doc='Current reading (power, current, etc, set by configuration)',
        range=SFT.MinMaxRangeType(min=0.0, max=1000.0, decimals=9)
    )
    bandwidth = SFT.PhysicalParameter(
        name='Bandwidth',
        dtype=str,
        doc='Bandwidth setting (low pass filter on photodiode input).',
        range=SFT.ChoiceRangeType(**{"LOW": True, "HIGH": False})
    )
    # power_range = SFT.PhysicalParameter(
    #     name='Power range',
    #     dtype=float,
    #     unit="W",
    #     range=SFT.MinMaxRangeType(decimals=9)
    # )
    # auto_range = SFT.PhysicalParameter(
    #     name='Auto range',
    #     dtype=bool
    # )
    zero_magnitude = SFT.PhysicalParameter(
        name="Zero magnitude",
        dtype=float
    )

    def __init__(self, name: str = None):
        SFT.HardwareModule.__init__(self, name=name)

    def setup(self):
        """Setup method - prevent non-hardware parameters from being polled."""
        pass  # Keep this for now

    def connect(self):
        rm = pyvisa.ResourceManager()
        self.device: ThorlabsPM100 = rm.open_resource(self.port.value(), resource_pyclass=ThorlabsPM100)

        # Add these lines here:
        self.device.baud_rate = 9600
        self.device.data_bits = 8
        self.device.parity = pyvisa.constants.Parity.none
        self.device.stop_bits = pyvisa.constants.StopBits.one
        self.device.flow_control = pyvisa.constants.VI_ASRL_FLOW_NONE
        self.device.timeout = 5000

        self.device.read_termination = '\r\n'
        self.device.write_termination = '\n'
        self.configuration.connect_to_hardware(
            read_func=self.device.get_configuration,
            write_func=lambda x: self.device.set_configuration(self.configuration.range[x])
        )
        self.reading.connect_to_hardware(
            read_func=self.device.measure
        )
        self.wavelength.connect_to_hardware(
        read_func=lambda: self.device.get_wavelength() * 1e9,  # meters → nm
        write_func=lambda wl_nm: self.device.set_wavelength(wl_nm * 1e-9)  # nm → meters
        )   
        self.bandwidth.connect_to_hardware(
            read_func=self.device.get_bandwidth,
            write_func=lambda x: self.device.set_bandwidth(self.bandwidth.range[x.value()])
        )
        # commented out for now, since PM100 does not support power range query
        # Can be reintroduced, if a new powermeter is used
        # self.power_range.connect_to_hardware(
        #     read_func=self.device.get_power_range,
        #     write_func=self.device.set_power_range
        # )
        # self.auto_range.connect_to_hardware(
        #     read_func=self.device.get_auto_range,
        #     write_func=self.device.set_auto_range
        # )
        self.zero_magnitude.connect_to_hardware(
            read_func=self.device.get_zero_magnitude
        )

        if hasattr(self, 'device_mutex'):
            self.device_mutex.hardware_read_func = None
            if hasattr(self.device_mutex, '_read_func'):
                self.device_mutex._read_func = None
            self.device_mutex.reread_from_hardware_after_write = False
        
        # Also handle 'connected' parameter if it exists
        if hasattr(self, 'connected'):
            self.connected.hardware_read_func = None
            if hasattr(self.connected, '_read_func'):
                self.connected._read_func = None
            self.connected.reread_from_hardware_after_write = False

        self.configuration.write_to_device("Power").wait(1.0)
        self.bandwidth.trigger_read().wait(3.0)
        self.wavelength.trigger_read().wait(3.0)
        self.wavelength.target_value.setValue(self.wavelength.value())
        # self.auto_range.trigger_read().wait(3.0)
        # self.power_range.trigger_read().wait(3.0)
        self.zero_magnitude.trigger_read().wait(3.0)
        self.reading.trigger_read().wait(3.0)

    def disconnect(self):
        if self.device is not None:
            self.device.close()
            self.device = None

    def reset_zero(self):
        """Needed when zero has changed.
        Warning: this resets more than just the zero offset and makes an attempt at restoring user settings.
        """
        # save settings
        self.wavelength.trigger_read().wait(1.0)
        self.bandwidth.trigger_read().wait(1.0)
        bandwidth = self.bandwidth.value()
        wavelength = self.wavelength.value()
        self.device.reset()
        # restore settings
        self.wavelength.setValue(wavelength)
        self.bandwidth.setValue(bandwidth)

    def read_series(self, n_samples: int, buffer=None) -> List[float]:
        """Fast reading of many samples.
        If buffer is given, then samples will be written there using `buffer.write`.
        """
        if buffer is None:
            return [self.device.measure() for i in range(n_samples)]
        else:
            for i in range(n_samples):
                buffer.write(self.device.measure())
