"""Control of KDC101 using pylablib.

Author
------
    Your Name (October 2025)
"""
import numpy as np
from pylablib.devices import Thorlabs
import ScopeFoundry as SFT
import time


class ThorlabsKDC101_PRMTZ8(SFT.HardwareModule):
    """Control of KCube DC servo controller (KDC101) using pylablib."""

    serial_number = SFT.ObjectParameter(
        name="Serial number",
        dtype=str,
        doc="Serial number of the KDC101 device"
    )
    
    enabled = SFT.PhysicalParameter(
        name="Enabled",
        dtype=bool,
        value=False,
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
        value=10.0,
        unit='deg/s',
        range=SFT.MinMaxRangeType(min=0, max=25, decimals=2),
        doc="Maximum velocity for moves"
    )
    
    acceleration = SFT.PhysicalParameter(
        name="Acceleration",
        dtype=float,
        value=10.0,
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
        
        # Connect action buttons HERE instead of in setup()
        self.home.sigActivated.connect(self.home_device)
        self.stop_motion.sigActivated.connect(self.stop_device)
        self.log.info("Action buttons connected in __init__")

    def setup(self):
        """Setup method to prevent polling issues."""
        # Connect action buttons
        self.home.sigActivated.connect(self.home_device)
        self.stop_motion.sigActivated.connect(self.stop_device)
        
        self.log.info("Action buttons connected")

    def connect(self):
        """Connect to the KDC101 device."""
        serial_num = self.serial_number.value()
        
        self.log.info(f"Connecting to KDC101 with serial number: {serial_num}")
        
        vel = self.read_velocity()
        self.log.info(f"Velocity test: {vel}")

        try:
            # Connect to the device
            self.device = Thorlabs.KinesisMotor(serial_num, scale="PRMTZ8")
            
            self.log.info(f"Connected to KDC101: {serial_num}")
            
            # Get device info
            device_info = self.device.get_device_info()
            self.log.info(f"Device info: {device_info}")
            
            # Set to use channel 1
            self.device.set_default_channel(1)
            
            # Set conversion from steps to degrees
            self.step_per_rev = 512 # read from Kinesis GUI
            self.gb_ratio = 67.49016 # read from Kinesis GUI
            self.gear_ratio = 20 # read from Kinesis GUI
            self.pos_conv = 360 / self.step_per_rev / self.gb_ratio / self.gear_ratio    
            
            
            # HOME THE DEVICE
            self.log.info(f"Homing parameters, {self.device.get_homing_parameters(scale=True)}")
            # self.device.setup_homing(velocity=vel_params[2])
                        
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
        
        # Set reasonable defaults
        self.log.info("Setting default velocity and acceleration...")
        print(self.device.get_scale())
        scale = self.device.get_scale()
        self.velocity.setValue(10.0)
        self.velocity.write_to_device(10.0).wait(1.0)
        self.acceleration.setValue(10.0)
        self.acceleration.write_to_device(10.0).wait(1.0)
        
        # Set target to current
        self.angle.target_value.setValue(self.angle.value())
        
        self.log.info("KDC101 ready!")

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
        # Motor is enabled if it's connected and not in an error state
        return True  # Pylablib motors are enabled when connected

    def write_enabled(self, enable: bool):
        """Enable or disable the motor."""
        if self.device is None:
            return
        # Pylablib doesn't have explicit enable/disable
        # The motor is active when connected
        if not enable:
            self.log.warning("Cannot disable motor via pylablib. Disconnect to disable.")
        else:
            self.log.info("Motor is enabled (always enabled when connected)")

    def read_angle(self) -> float:
        """Read current angle position."""
        if self.device is None:
            return 0.0
        
        pos = self.device.get_position()
        angle = np.mod(pos*self.pos_conv, 360)
        return float(angle)

    def write_angle(self, angle: float):
        """Move to specified angle."""
        if self.device is None:
            self.log.error("Device is None!")
            return
        
        try:
            angle = float(np.mod(angle, 360))
            pos = angle/self.pos_conv
            
            self.device.move_to(pos, channel=1)
            self.device.wait_for_stop()
            self.angle.trigger_read()            
            
        except Exception as e:
            self.log.error(f"Error: {e}")
            import traceback
            self.log.error(traceback.format_exc())

    def read_velocity(self) -> float:
        """Read maximum velocity."""
        if self.device is None:
            return 0.0
        maxvel = self.device.get_velocity_parameters()[2] * self.pos_conv
        return float(maxvel)

    def read_acceleration(self) -> float:
        """Read acceleration."""
        if self.device is None:
            return 0.0
        acc = self.device.get_velocity_parameters()[1] * self.pos_conv
        return float(acc)

    def write_velocity(self, velocity: float):
        """Set maximum velocity."""
        if self.device is None:
            return
        params = self.device.get_velocity_parameters()
        
        # Convert deg/s to device units
        maxvel = velocity / self.pos_conv
        
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=params[1],  # Keep current acceleration
            max_velocity=maxvel
        )

    def write_acceleration(self, acceleration: float):
        """Set acceleration."""
        if self.device is None:
            return
        
        # Don't allow zero acceleration!
        if acceleration <= 0:
            self.log.warning("Cannot set acceleration to zero or negative, using 1.0 deg/s²")
            acceleration = 1.0
        
        params = self.device.get_velocity_parameters()
        
        # Convert deg/s² to device units
        acc = acceleration / self.pos_conv
        
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=acc,
            max_velocity=params[2]  # Keep current velocity
        )

    def read_angle_continuous(self, target_angle):
        current_angle = self.read_angle()
        diff = np.abs(target_angle - current_angle)
        acc = self.read_acceleration()
        vel = self.read_velocity()
        if diff <= 10.0:
            time = np.sqrt(2*diff/acc)
        else:
            time = np.sqrt(2*10.0/acc) + (diff - 10.0)/vel
        
        update_interval = 0.5
        for i in range(int(time/update_interval)):
            self.angle.trigger_read()
            time.sleep(update_interval)

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
            self.device.home(sync=True, force=false, channel=1)  # Wait for homing to complete
            self.angle.trigger_read()
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