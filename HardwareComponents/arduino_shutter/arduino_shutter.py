# -*- coding: utf-8 -*-
"""Low-level control for Arduino-based shutter system.

This controls servo-actuated shutters via an Arduino.
"""

import logging
import pyvisa

logger = logging.getLogger(__name__)


class ArduinoShutter(pyvisa.resources.MessageBasedResource):
    """Driver for Arduino-controlled servo shutters.
    
    Supports two independent shutters on pins 10 and 11.
    """
    
    def open_shutter(self, shutter_id: int = 10):
        """Open the specified shutter.
        
        Args:
            shutter_id: Shutter number (10 or 11)
        """
        if shutter_id not in [10, 11]:
            raise ValueError("shutter_id must be 10 or 11")
        cmd = f"!openshutter={shutter_id}"
        self.write(cmd)
        logger.info(f"Opened shutter {shutter_id}")
    
    def close_shutter(self, shutter_id: int = 10):
        """Close the specified shutter.
        
        Args:
            shutter_id: Shutter number (10 or 11)
        """
        if shutter_id not in [10, 11]:
            raise ValueError("shutter_id must be 10 or 11")
        cmd = f"!closeshutter={shutter_id}"
        self.write(cmd)
        logger.info(f"Closed shutter {shutter_id}")
    
    def get_shutter_state(self, shutter_id: int = 10) -> bool:
        """Get the current state of the shutter."""
        if shutter_id not in [10, 11]:
            raise ValueError("shutter_id must be 10 or 11")
        
        # Clear any pending input before querying
        try:
            # Flush the input buffer
            while True:
                try:
                    self.read_bytes(1, break_on_termchar=False)
                except:
                    break
        except:
            pass
        
        # Send query
        cmd = f"?readshutter={shutter_id}"
        self.write(cmd)
        
        # Read response with explicit timeout handling
        try:
            response = self.read().strip()
            state = int(response)
            return bool(state)
        except Exception as e:
            logger.error(f"Error reading shutter state: {e}")
            return False  # Default to closed on error
    
    def set_shutter_state(self, shutter_id: int, state: bool):
        """Set the shutter to open (True) or closed (False).
        
        Args:
            shutter_id: Shutter number (10 or 11)
            state: True to open, False to close
        """
        if state:
            self.open_shutter(shutter_id)
        else:
            self.close_shutter(shutter_id)


if __name__ == "__main__":
    # Test code
    # import pyvisa
    # rm = pyvisa.ResourceManager()
    
    # # Replace with your Arduino's COM port
    # shutter = rm.open_resource('COM11', resource_pyclass=ArduinoShutter)
    
    # print("Testing shutter 10...")
    # print(f"Current state: {shutter.get_shutter_state(10)}")
    
    # shutter.open_shutter(10)
    # print(f"After open: {shutter.get_shutter_state(10)}")
    
    # shutter.close_shutter(10)
    # print(f"After close: {shutter.get_shutter_state(10)}")
    
    # shutter.close()
    pass