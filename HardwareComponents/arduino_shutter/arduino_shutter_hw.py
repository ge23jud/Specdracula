# -*- coding: utf-8 -*-
"""ScopeFoundry hardware module for Arduino shutter control.

Authors
-------
    Your Name, October 2025
"""

import pyvisa
import ScopeFoundry as SFT

try:
    from .arduino_shutter import ArduinoShutter
except Exception as e:
    print('Could not import Arduino shutter device driver')
    print(e)


class ArduinoShutterHW(SFT.HardwareModule):
    """Hardware module for Arduino-controlled servo shutters."""
    
    port = SFT.ObjectParameter(
        name='Port',
        dtype=str,
        doc='Serial port for Arduino (e.g., COM3, /dev/ttyUSB0)'
    )
    
    shutter_id = SFT.ObjectParameter(
        name='Shutter ID',
        dtype=int,
        doc='Shutter pin number (10 or 11)'
    )
    
    is_open = SFT.PhysicalParameter(
        name='Shutter open',
        dtype=bool,
        doc='True if shutter is open, False if closed'
    )
    
    def __init__(self, name: str = None):
        SFT.HardwareModule.__init__(self, name=name)
    
    def setup(self):
        """Setup method."""
        pass
    
    def connect(self):
        """Connect to the Arduino shutter."""
        rm = pyvisa.ResourceManager()
        self.device: ArduinoShutter = rm.open_resource(
            self.port.value(), 
            resource_pyclass=ArduinoShutter
        )
        
        # Set serial parameters AFTER opening the resource
        self.device.baud_rate = 115200
        self.device.data_bits = 8
        self.device.parity = pyvisa.constants.Parity.none
        self.device.stop_bits = pyvisa.constants.StopBits.one
        self.device.flow_control = pyvisa.constants.VI_ASRL_FLOW_NONE
        self.device.timeout = 100
        self.device.read_termination = '\n'
        self.device.write_termination = '\n'
        
        # Connect the shutter state parameter to hardware
        self.is_open.connect_to_hardware(
            read_func=self._read_shutter_state,
            write_func=self._write_shutter_state
        )
        
        # Read initial state
        self.is_open.trigger_read().wait(1.0)
        self.is_open.target_value.setValue(self.is_open.value())
    
    def disconnect(self):
        """Disconnect from the Arduino."""
        if self.device is not None:
            # Close shutter for safety
            try:
                self.device.close_shutter(self.shutter_id.value())
            except:
                pass
            self.device.close()
            self.device = None
    
    def _read_shutter_state(self) -> bool:
        """Read the current shutter state from hardware."""
        return self.device.get_shutter_state(self.shutter_id.value())
    
    def _write_shutter_state(self, state: bool):
        """Write the shutter state to hardware."""
        self.device.set_shutter_state(self.shutter_id.value(), state)
    
    def open_shutter(self):
        """Convenience method to open the shutter."""
        self.is_open.setValue(True)
    
    def close_shutter(self):
        """Convenience method to close the shutter."""
        self.is_open.setValue(False)