"""Control of Thorlabs K10CR1 motorized rotation stage using pylablib.

Unlike the KDC101, the K10CR1 is an integrated stepper motor stage (no
separate K-Cube controller) but is addressed through the same pylablib
KinesisMotor class.
"""
import numpy as np
from pylablib.devices import Thorlabs
import ScopeFoundry as SFT


class ThorlabsK10CR1(SFT.HardwareModule):
    """Control of K10CR1 motorized rotation stage using pylablib."""

    serial_number = SFT.ObjectParameter(
        name="Serial number",
        dtype=str,
        doc="Serial number of the K10CR1 device"
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

        # Connect action buttons here, not in connect(): making connections to
        # objects created in different threads can fail silently later on.
        self.home.sigActivated.connect(self.home_device)
        self.stop_motion.sigActivated.connect(self.stop_device)

    def connect(self):
        """Connect to the K10CR1 device."""
        serial_num = self.serial_number.value()
        self.log.info(f"Connecting to K10CR1 with serial number: {serial_num}")

        try:
            # scale="stage" lets pylablib autodetect the K10CR1 model and
            # report position/velocity/acceleration directly in degrees,
            # degrees/s and degrees/s^2.
            self.device = Thorlabs.KinesisMotor(serial_num, scale="stage")
            device_info = self.device.get_device_info()
            self.log.info(f"Connected to K10CR1: {serial_num}, device info: {device_info}")
        except Exception as e:
            self.log.error(f"Failed to connect to K10CR1: {e}")
            raise

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

        self.enabled.trigger_read().wait(1.0)
        self.angle.trigger_read().wait(1.0)
        self.velocity.trigger_read().wait(1.0)
        self.acceleration.trigger_read().wait(1.0)

        # Set target to current so the UI doesn't show a pending move on connect.
        self.angle.target_value.setValue(self.angle.value())

        self.log.info("K10CR1 ready!")

    def disconnect(self):
        """Disconnect from the device."""
        if self.device is not None:
            try:
                self.device.close()
                self.log.info("Disconnected from K10CR1")
            except Exception as e:
                self.log.error(f"Error disconnecting: {e}")
            finally:
                self.device = None

    def read_enabled(self) -> bool:
        """K10CR1/pylablib has no explicit enable/disable; it is active whenever connected."""
        return self.device is not None

    def write_enabled(self, enable: bool):
        if self.device is None:
            return
        if not enable:
            self.log.warning("Cannot disable motor via pylablib. Disconnect to disable.")

    def read_angle(self) -> float:
        if self.device is None:
            return 0.0
        return float(np.mod(self.device.get_position(), 360))

    def write_angle(self, angle: float):
        if self.device is None:
            self.log.error("Device is None!")
            return
        try:
            angle = float(np.mod(angle, 360))
            self.device.move_to(angle)
            self.device.wait_for_stop()
            self.angle.trigger_read().wait(timeout=0.2)
        except Exception as e:
            self.log.error(f"Error moving K10CR1: {e}")

    def read_velocity(self) -> float:
        if self.device is None:
            return 0.0
        return float(self.device.get_velocity_parameters()[2])  # max_velocity

    def write_velocity(self, velocity: float):
        if self.device is None:
            return
        params = self.device.get_velocity_parameters()
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=params[1],
            max_velocity=velocity
        )

    def read_acceleration(self) -> float:
        if self.device is None:
            return 0.0
        return float(self.device.get_velocity_parameters()[1])  # acceleration

    def write_acceleration(self, acceleration: float):
        if self.device is None:
            return
        if acceleration <= 0:
            self.log.warning("Cannot set acceleration to zero or negative, using 1.0 deg/s^2")
            acceleration = 1.0
        params = self.device.get_velocity_parameters()
        self.device.setup_velocity(
            min_velocity=params[0],
            acceleration=acceleration,
            max_velocity=params[2]
        )

    def read_is_moving(self) -> bool:
        if self.device is None:
            return False
        return self.device.is_moving()

    def home_device(self):
        """Home the device."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        try:
            self.device.home(sync=True)
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
