"""Control of a Picomotor-driven motorized mirror mount through a Newport
(New Focus) 8742 Picomotor controller, using pylablib.

The mirror's horizontal and vertical actuators are plugged into two of the
controller's four motor outputs, chosen via the 'Horizontal axis' / 'Vertical
axis' parameters. Picomotors are open loop: positions are step counts relative
to the last zero reference, not calibrated angles.
"""
import ScopeFoundry as SFT

from .picomotor_8742_dev import Picomotor8742Device

_STEP_RANGE = SFT.MinMaxRangeType(min=-2147483648, max=2147483647, decimals=0)
_SPEED_RANGE = SFT.MinMaxRangeType(min=1, max=2000, decimals=0)  # steps/s, per 8742 manual
_ACCEL_RANGE = SFT.MinMaxRangeType(min=1, max=200000, decimals=0)  # steps/s^2, per 8742 manual
_AXIS_RANGE = SFT.MinMaxRangeType(min=1, max=4, decimals=0)


class Picomotor8742HW(SFT.HardwareModule):
    """Two-axis motorized mirror on a Newport 8742 Picomotor controller."""

    connection = SFT.ObjectParameter(
        name="Connection",
        dtype=str,
        value='0',
        doc="USB device index ('0' = first controller) or IP address / hostname for Ethernet"
    )
    identification = SFT.ObjectParameter(name="Identification", dtype=str, readonly=True)
    move_timeout = SFT.ObjectParameter(
        name="Move timeout",
        dtype=float,
        value=60.0,
        unit='s',
        doc="Stop the axis if a single move takes longer than this"
    )

    horizontal = SFT.ParameterGroup('Horizontal')
    axis_h = SFT.ObjectParameter('Horizontal axis', dtype=int, value=1, range=_AXIS_RANGE, parent=horizontal)
    position_h = SFT.PhysicalParameter('Position', dtype=int, unit='steps', range=_STEP_RANGE, parent=horizontal)
    step_size_h = SFT.ObjectParameter('Step size', dtype=int, value=100, unit='steps',
                                      range=SFT.MinMaxRangeType(min=1, max=100000, decimals=0), parent=horizontal)
    speed_h = SFT.PhysicalParameter('Speed', dtype=int, unit='steps/s', range=_SPEED_RANGE, parent=horizontal)
    acceleration_h = SFT.PhysicalParameter('Acceleration', dtype=int, unit='steps/s2', range=_ACCEL_RANGE,
                                           parent=horizontal)
    motor_type_h = SFT.PhysicalParameter('Motor type', dtype=str, parent=horizontal)
    step_plus_h = SFT.ActionParameter('Step +', parent=horizontal)
    step_minus_h = SFT.ActionParameter('Step -', parent=horizontal)
    zero_h = SFT.ActionParameter('Set zero here', parent=horizontal)

    vertical = SFT.ParameterGroup('Vertical')
    axis_v = SFT.ObjectParameter('Vertical axis', dtype=int, value=2, range=_AXIS_RANGE, parent=vertical)
    position_v = SFT.PhysicalParameter('Position', dtype=int, unit='steps', range=_STEP_RANGE, parent=vertical)
    step_size_v = SFT.ObjectParameter('Step size', dtype=int, value=100, unit='steps',
                                      range=SFT.MinMaxRangeType(min=1, max=100000, decimals=0), parent=vertical)
    speed_v = SFT.PhysicalParameter('Speed', dtype=int, unit='steps/s', range=_SPEED_RANGE, parent=vertical)
    acceleration_v = SFT.PhysicalParameter('Acceleration', dtype=int, unit='steps/s2', range=_ACCEL_RANGE,
                                           parent=vertical)
    motor_type_v = SFT.PhysicalParameter('Motor type', dtype=str, parent=vertical)
    step_plus_v = SFT.ActionParameter('Step +', parent=vertical)
    step_minus_v = SFT.ActionParameter('Step -', parent=vertical)
    zero_v = SFT.ActionParameter('Set zero here', parent=vertical)

    is_moving = SFT.PhysicalParameter('Is moving', dtype=bool, value=False)
    stop_motion = SFT.ActionParameter(name='Stop')

    def __init__(self, name: str = None):
        SFT.HardwareModule.__init__(self, name=name)
        self.device = None

        # Connect action buttons here, not in connect(): making connections to
        # objects created in different threads can fail silently later on.
        self.step_plus_h.sigActivated.connect(lambda: self.step('h', +1))
        self.step_minus_h.sigActivated.connect(lambda: self.step('h', -1))
        self.step_plus_v.sigActivated.connect(lambda: self.step('v', +1))
        self.step_minus_v.sigActivated.connect(lambda: self.step('v', -1))
        self.zero_h.sigActivated.connect(lambda: self.set_zero('h'))
        self.zero_v.sigActivated.connect(lambda: self.set_zero('v'))
        self.stop_motion.sigActivated.connect(self.stop_device)

    def _axis(self, which: str) -> int:
        return {'h': self.axis_h, 'v': self.axis_v}[which].value()

    def _position_param(self, which: str):
        return {'h': self.position_h, 'v': self.position_v}[which]

    def connect(self):
        """Connect to the 8742 controller."""
        conn = self.connection.value()
        self.log.info(f"Connecting to Picomotor 8742 at '{conn}'")
        try:
            self.device = Picomotor8742Device(conn)
            self.device.connect()
            self.identification.setValue(self.device.get_id())
            self.log.info(f"Connected to Picomotor 8742: {self.identification.value()}")
        except Exception as e:
            self.device = None
            self.log.error(f"Failed to connect to Picomotor 8742: {e}")
            raise

        for which, position, speed, accel, motor_type in (
                ('h', self.position_h, self.speed_h, self.acceleration_h, self.motor_type_h),
                ('v', self.position_v, self.speed_v, self.acceleration_v, self.motor_type_v)):
            position.connect_to_hardware(
                read_func=lambda w=which: self.read_position(w),
                write_func=lambda pos, w=which: self.write_position(w, pos)
            )
            speed.connect_to_hardware(
                read_func=lambda w=which: self.read_speed(w),
                write_func=lambda val, w=which: self.write_speed(w, val)
            )
            accel.connect_to_hardware(
                read_func=lambda w=which: self.read_acceleration(w),
                write_func=lambda val, w=which: self.write_acceleration(w, val)
            )
            motor_type.connect_to_hardware(
                read_func=lambda w=which: self.read_motor_type(w)
            )
        self.is_moving.connect_to_hardware(read_func=self.read_is_moving)

        for param in (self.position_h, self.speed_h, self.acceleration_h, self.motor_type_h,
                      self.position_v, self.speed_v, self.acceleration_v, self.motor_type_v,
                      self.is_moving):
            param.trigger_read().wait(1.0)

        # Set target to current so the UI doesn't show a pending move on connect.
        self.position_h.target_value.setValue(self.position_h.value())
        self.position_v.target_value.setValue(self.position_v.value())

        for which, motor_type in (('h', self.motor_type_h), ('v', self.motor_type_v)):
            if motor_type.value() == 'none':
                self.log.warning(f"No motor detected on axis {self._axis(which)} ({which}); check cabling/axis setting")

        self.log.info("Picomotor 8742 ready!")

    def disconnect(self):
        """Disconnect from the controller."""
        if self.device is not None:
            try:
                self.device.close()
                self.log.info("Disconnected from Picomotor 8742")
            except Exception as e:
                self.log.error(f"Error disconnecting: {e}")
            finally:
                self.device = None

    def read_position(self, which: str) -> int:
        if self.device is None:
            return 0
        return self.device.get_position(self._axis(which))

    def write_position(self, which: str, position: int):
        """Absolute move in steps; blocks (on the worker thread) until the axis stops."""
        if self.device is None:
            self.log.error("Device is None!")
            return
        axis = self._axis(which)
        try:
            self.device.move_to(axis, position)
            if not self.device.wait_move(axis, timeout=self.move_timeout.value()):
                self.log.warning(f"Move on axis {axis} timed out after {self.move_timeout.value()} s, stopping")
                self.device.stop(axis)
        except Exception as e:
            self.log.error(f"Error moving Picomotor axis {axis}: {e}")

    def read_speed(self, which: str) -> int:
        if self.device is None:
            return 0
        return self.device.get_velocity_parameters(self._axis(which))[0]

    def write_speed(self, which: str, speed: int):
        if self.device is None:
            return
        self.device.set_speed(self._axis(which), speed)

    def read_acceleration(self, which: str) -> int:
        if self.device is None:
            return 0
        return self.device.get_velocity_parameters(self._axis(which))[1]

    def write_acceleration(self, which: str, accel: int):
        if self.device is None:
            return
        self.device.set_acceleration(self._axis(which), accel)

    def read_motor_type(self, which: str) -> str:
        if self.device is None:
            return ''
        return self.device.get_motor_type(self._axis(which))

    def read_is_moving(self) -> bool:
        if self.device is None:
            return False
        return self.device.is_moving(self.axis_h.value()) or self.device.is_moving(self.axis_v.value())

    def step(self, which: str, direction: int):
        """Move one step size in `direction` (+1/-1) relative to the current target."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        position = self._position_param(which)
        step_size = {'h': self.step_size_h, 'v': self.step_size_v}[which].value()
        # Build on the target, not the last read, so rapid clicks accumulate.
        position.write_to_device(position.target_value.value() + direction * step_size)

    def set_zero(self, which: str):
        """Define the current position of the axis as 0 steps (no motion)."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        try:
            self.device.set_zero(self._axis(which))
            position = self._position_param(which)
            position.trigger_read().wait(1.0)
            position.target_value.setValue(position.value())
        except Exception as e:
            self.log.error(f"Error setting zero: {e}")

    def stop_device(self):
        """Stop both mirror axes."""
        if self.device is None:
            self.log.error('Device not connected')
            return
        try:
            for axis in {self.axis_h.value(), self.axis_v.value()}:
                self.device.stop(axis)
            self.position_h.trigger_read()
            self.position_v.trigger_read()
            self.log.info("Motion stopped")
        except Exception as e:
            self.log.error(f"Error stopping motion: {e}")
