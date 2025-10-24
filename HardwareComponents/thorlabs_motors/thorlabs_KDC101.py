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
        
        try:
            # Connect to the device
            self.device = Thorlabs.KinesisMotor(serial_num)
            
            self.log.info(f"Connected to KDC101: {serial_num}")
            
            # Get device info
            device_info = self.device.get_device_info()
            self.log.info(f"Device info: {device_info}")
            
            # Set to use channel 1
            self.device.set_default_channel(1)
            
            # Get scale info
            scale = self.device.get_scale()
            self.log.info(f"Scale factors: {scale}")
            
            stage_name = self.device.get_stage()
            self.log.info(f"Stage: {stage_name}")
            
            # Check velocity parameters
            vel_params = self.device.get_velocity_parameters()
            self.log.info(f"Velocity params: {vel_params}")
            
            # HOME THE DEVICE
            self.log.info("Homing device (this may take a moment)...")
            self.device.home(sync=True, channel=1)
            pos_after_home = self.device.get_position()
            self.log.info(f"Homing complete! Position: {pos_after_home}")
            
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
        return float(self.device.get_position())

    def write_angle(self, angle: float):
        """Move to specified angle."""
        if self.device is None:
            self.log.error("Device is None!")
            return
        
        try:
            current_pos = self.device.get_position()
            angle = float(np.mod(angle, 360))
            distance = angle - current_pos
            
            self.log.info("=" * 60)
            self.log.info(f"MOVE TEST")
            self.log.info(f"Current position: {current_pos:.2f}°")
            self.log.info(f"Target position: {angle:.2f}°")
            self.log.info(f"Distance to travel: {distance:.2f}°")
            self.log.info(f"Direction: {'FORWARD (+)' if distance > 0 else 'BACKWARD (-)'}")
            
            # Check velocity params
            vel_params = self.device.get_velocity_parameters()
            scale = self.device.get_scale()
            vel_deg = vel_params[2] * scale[2]
            accel_deg = vel_params[1] * scale[2]
            self.log.info(f"Velocity: {vel_deg:.2f} deg/s, Accel: {accel_deg:.2f} deg/s²")
            
            if vel_params[1] == 0:
                self.log.error("ACCELERATION IS ZERO - CANNOT MOVE!")
                return
            
            # Send move command
            self.log.info(f"Sending move command...")
            self.device.move_to(angle, channel=1)
            
            # Monitor progress
            import time
            for i in range(20):  # Check for up to 10 seconds
                time.sleep(0.5)
                new_pos = self.device.get_position()
                is_moving = self.device.is_moving()
                moved_distance = new_pos - current_pos
                
                if i == 0 or i % 4 == 0 or not is_moving:  # Log every 2 seconds
                    self.log.info(f"[{i*0.5:.1f}s] Moving: {is_moving}, Pos: {new_pos:.2f}°, Moved: {moved_distance:.2f}°")
                
                if not is_moving and abs(new_pos - angle) < 1.0:
                    self.log.info(f"✓ MOVE COMPLETE!")
                    self.log.info(f"Final position: {new_pos:.2f}°")
                    break
            else:
                self.log.warning(f"Move timed out or did not reach target")
                self.log.warning(f"Final position: {self.device.get_position():.2f}°")
            
            self.log.info("=" * 60)
            
        except Exception as e:
            self.log.error(f"Error: {e}")
            import traceback
            self.log.error(traceback.format_exc())

    def read_velocity(self) -> float:
        """Read maximum velocity."""
        if self.device is None:
            return 0.0
        params = self.device.get_velocity_parameters()
        scale = self.device.get_scale()
        # scale[2] converts device units to deg/s
        velocity_deg_s = params[2] * scale[2]
        self.log.debug(f"Read velocity: {params[2]} DU = {velocity_deg_s} deg/s")
        return float(velocity_deg_s)

    def read_acceleration(self) -> float:
        """Read acceleration."""
        if self.device is None:
            return 0.0
        params = self.device.get_velocity_parameters()
        scale = self.device.get_scale()
        # scale[2] converts device units to deg/s (same for acceleration)
        accel_deg_s2 = params[1] * scale[2]
        self.log.debug(f"Read acceleration: {params[1]} DU = {accel_deg_s2} deg/s²")
        return float(accel_deg_s2)

    def write_velocity(self, velocity: float):
        """Set maximum velocity."""
        if self.device is None:
            return
        scale = self.device.get_scale()
        params = self.device.get_velocity_parameters()
        
        # Convert deg/s to device units
        velocity_du = velocity / scale[2]
        
        self.log.info(f"Setting velocity: {velocity} deg/s = {velocity_du} DU")
        
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=params[1],  # Keep current acceleration
            max_velocity=velocity_du
        )

    def write_acceleration(self, acceleration: float):
        """Set acceleration."""
        if self.device is None:
            return
        
        # Don't allow zero acceleration!
        if acceleration <= 0:
            self.log.warning("Cannot set acceleration to zero or negative, using 1.0 deg/s²")
            acceleration = 1.0
        
        scale = self.device.get_scale()
        params = self.device.get_velocity_parameters()
        
        # Convert deg/s² to device units
        acceleration_du = acceleration / scale[2]
        
        self.log.info(f"Setting acceleration: {acceleration} deg/s² = {acceleration_du} DU")
        
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=acceleration_du,
            max_velocity=params[2]  # Keep current velocity
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
            self.log.info("=" * 50)
            self.log.info("HOMING DEVICE - Please wait...")
            self.log.info("=" * 50)
            self.device.home(sync=True)  # Wait for homing to complete
            self.log.info("=" * 50)
            self.log.info("HOMING COMPLETE!")
            self.log.info("=" * 50)
            # Update position after homing
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