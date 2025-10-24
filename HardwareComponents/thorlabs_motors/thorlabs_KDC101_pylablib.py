"""Control of KDC101 using pylablib.

Author
------
    Your Name (October 2025)
"""
import numpy as np
from pylablib.devices import Thorlabs
import ScopeFoundry as SFT


class ThorlabsKDC101(SFT.HardwareModule):
    """Control of KCube DC servo controller (KDC101) using pylablib."""

    serial_number = SFT.ObjectParameter(
        name="Serial number",
        dtype=str,
        doc="Serial number of the KDC101 device"
    )
    
    enabled = SFT.PhysicalParameter(
        name="Enabled",
        dtype=bool,
        initial=False,
        doc="Enable/disable the motor"
    )
    
    angle = SFT.PhysicalParameter(
        name="Angle",
        dtype=float,
        unit='deg',
        range=SFT.MinMaxRangeType(min=0, max=360, decimals=3),
        doc="Current angle position"
    )
    
    velocity = SFT.PhysicalParameter(
        name="Velocity",
        dtype=float,
        initial=10.0,
        unit='deg/s',
        range=SFT.MinMaxRangeType(min=0, max=25, decimals=2),
        doc="Maximum velocity for moves"
    )
    
    acceleration = SFT.PhysicalParameter(
        name="Acceleration",
        dtype=float,
        initial=10.0,
        unit='deg/s2',
        range=SFT.MinMaxRangeType(min=0, max=25, decimals=2),
        doc="Acceleration for moves"
    )
    
    is_moving = SFT.PhysicalParameter(
        name="Is moving",
        dtype=bool,
        readonly=True,
        doc="Whether the motor is currently moving"
    )
    
    home = SFT.ActionParameter(name='Home')
    stop_motion = SFT.ActionParameter(name='Stop')

    def __init__(self, name: str = None):
        SFT.HardwareModule.__init__(self, name=name)
        self.device = None

    def setup(self):
        """Setup method to prevent polling issues."""
        # Connect action buttons
        self.home.sigActivated.connect(self.home_device)
        self.stop_motion.sigActivated.connect(self.stop_device)

    def connect(self):
        """Connect to the KDC101 device."""
        serial_num = self.serial_number.value()
        
        self.log.info(f"Connecting to KDC101 with serial number: {serial_num}")
        
        try:
            # Connect to the device
            self.device = Thorlabs.KinesisMotor(serial_num)
            
            self.log.info(f"Connected to KDC101: {serial_num}")
            
            # Get device info
            device_info = self.device.get_device_info()
            self.log.info(f"Device info: {device_info}")
            
        except Exception as e:
            self.log.error(f"Failed to connect to KDC101: {e}")
            raise
        
        # Connect parameters to hardware
        self.enabled.connect_to_hardware(
            read_func=self.read_enabled,
            write_func=self.write_enabled
        )
        
        self.angle.connect_to_hardware(
            read_func=self.read_angle,
            write_func=self.write_angle
        )
        
        self.velocity.connect_to_hardware(
            read_func=self.read_velocity,
            write_func=self.write_velocity
        )
        
        self.acceleration.connect_to_hardware(
            read_func=self.read_acceleration,
            write_func=self.write_acceleration
        )
        
        self.is_moving.connect_to_hardware(
            read_func=self.read_is_moving
        )
        
        # Read initial values
        self.enabled.trigger_read().wait(1.0)
        self.angle.trigger_read().wait(1.0)
        self.velocity.trigger_read().wait(1.0)
        self.acceleration.trigger_read().wait(1.0)
        
        # Set target values to current values
        self.angle.target_value.setValue(self.angle.value())

    def disconnect(self):
        """Disconnect from the device."""
        if self.device is not None:
            try:
                self.device.close()
                self.log.info("Disconnected from KDC101")
            except Exception as e:
                self.log.error(f"Error disconnecting: {e}")
            finally:
                self.device = None

    def read_enabled(self) -> bool:
        """Check if motor is enabled."""
        if self.device is None:
            return False
        return self.device.is_enabled()

    def write_enabled(self, enable: bool):
        """Enable or disable the motor."""
        if self.device is None:
            return
        if enable:
            self.device.enable()
        else:
            self.device.disable()

    def read_angle(self) -> float:
        """Read current angle position."""
        if self.device is None:
            return 0.0
        return float(self.device.get_position())

    def write_angle(self, angle: float):
        """Move to specified angle."""
        if self.device is None:
            return
        # Normalize angle to 0-360
        angle = float(np.mod(angle, 360))
        self.device.move_to(angle)

    def read_velocity(self) -> float:
        """Read maximum velocity."""
        if self.device is None:
            return 0.0
        params = self.device.get_velocity_parameters()
        return float(params[2])  # max_velocity

    def write_velocity(self, velocity: float):
        """Set maximum velocity."""
        if self.device is None:
            return
        params = self.device.get_velocity_parameters()
        # Keep current min_velocity and acceleration, update max_velocity
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=params[1],
            max_velocity=velocity
        )

    def read_acceleration(self) -> float:
        """Read acceleration."""
        if self.device is None:
            return 0.0
        params = self.device.get_velocity_parameters()
        return float(params[1])  # acceleration

    def write_acceleration(self, acceleration: float):
        """Set acceleration."""
        if self.device is None:
            return
        params = self.device.get_velocity_parameters()
        # Keep current velocities, update acceleration
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=acceleration,
            max_velocity=params[2]
        )

    def read_is_moving(self) -> bool:
        """Check if motor is currently moving."""
        if self.device is None:
            return False
        return self.device.is_moving()

    def home_device(self):
        """Home the device."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        try:
            self.log.info("Homing device...")
            self.device.home(sync=False)  # Non-blocking home
            self.log.info("Homing started")
        except Exception as e:
            self.log.error(f"Error during homing: {e}")

    def stop_device(self):
        """Stop any current motion."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        try:
            self.device.stop()
            self.log.info("Motion stopped")
        except Exception as e:
            self.log.error(f"Error stopping motion: {e}")