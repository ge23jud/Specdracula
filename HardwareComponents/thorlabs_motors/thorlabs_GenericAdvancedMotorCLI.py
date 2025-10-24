"""Control of devices inheriting from GenericAdvancedMotorCLI in Thorlabs Kinesis software.

Author
------
    Nick Metelski (August 2022)
"""
import clr
import numpy as np

from System import Decimal

try:
    clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
    clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
    from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
    from Thorlabs.MotionControl.GenericMotorCLI.Settings import RotationSettings
except Exception as e:
    print('Thorlabs motion control could not be imported')
    print(e)
import ScopeFoundry as SFT
from ScopeFoundry import HardwareModule, PhysicalParameter, ObjectParameter, ActionParameter, WorkerTask


class ThorlabsGenericAdvancedMotorCLI(HardwareModule):
    """Control of Thorlabs controlled inheriting from GenericAdvancedMotorCLI.
    """

    serial_number = ObjectParameter(
        name="Serial number",
        dtype=str,
        readonly=True,
        value=""
    )
    actuator = PhysicalParameter(
        name="Actuator",
        value="",
        dtype=str,
        # readonly=True
    )
    polling_time = PhysicalParameter(
        "Polling time",
        dtype=int,
        value=100,
        unit='ms',
        doc="In miliseconds. The polling loop requests regular status requests to the motor to ensure "
            "the program keeps track of the device."
    )
    enabled = PhysicalParameter(
        "Enabled",
        dtype=bool,
        # readonly=False,
        value=False
    )
    motor_state = PhysicalParameter(
        "Motor state",
        dtype=str
    )
    angle = PhysicalParameter(
        "Angle",
        dtype=float,
        unit='deg',
        range=SFT.MinMaxRangeType(decimals=5)
        # readonly=False
    )
    velocity = PhysicalParameter(
        "Velocity",
        value=200.0,
        dtype=float,
        unit='deg/s',
        # readonly=False,
        range=SFT.MinMaxRangeType(min=0, max=1000)
    )
    acceleration = PhysicalParameter(
        "Acceleration",
        value=200.0,
        dtype=float,
        unit='deg/s2',
        # readonly=False,
        range=SFT.MinMaxRangeType(min=0, max=1000)
    )
    rotation_mode = PhysicalParameter(
        "Rotation mode",
        dtype=str,
        value='Total angle',
        range=SFT.ChoiceRangeType(**{'Fixed range': 0, 'Total angle': 1, 'Equivalent angle': 2})
    )
    rotation_direction = PhysicalParameter(
        "Rotation direction",
        dtype=str,
        value='Quickest',
        range=SFT.ChoiceRangeType(**{'Quickest': 0, 'Forwards': 1, 'Reverse': 2}),
    )
    move_timeout = ObjectParameter(
        "Move timeout",
        doc="This applies to both homing and moving. In ms.",
        dtype=int,
        value=30000,
        range=SFT.MinMaxRangeType(min=1000, max=120000)
    )

    home = ActionParameter(name='Home')
    interrupt = ActionParameter(name='Interrupt movement')

    def __init__(self, *args, **kwargs):
        HardwareModule.__init__(self, *args, **kwargs)
        self._aborted = False
        self.task_home = WorkerTask("Home", self.home_device, default_thread_pool=self.thread_pool)
        self.task_interrupt = WorkerTask("Interrupt move", self.interrupt_move, default_thread_pool=self.thread_pool)
        self.home.sigActivated.connect(lambda: self.thread_pool.start(self.task_home))
        self.interrupt.sigActivated.connect(lambda: self.thread_pool.start(self.task_interrupt))

    def connect(self):
        self.enabled.connect_to_hardware(
            write_func=self.toggle_enable,
            read_func=lambda: self.device.IsEnabled
        )
        self.actuator.connect_to_hardware(
            read_func=lambda: self.device.LoadMotorConfiguration(self.serial_number.value())
        )
        self.motor_state.connect_to_hardware(
            read_func=lambda: self.device.State
        )
        self.angle.connect_to_hardware(
            read_func=lambda: float(Decimal.ToSingle(self.device.Position)),
            write_func=lambda x: self.device.MoveTo(Decimal(float(np.mod(x, 360))), self.move_timeout.value())
        )
        self.velocity.connect_to_hardware(
            read_func=lambda: float(Decimal.ToSingle(
                self.device.GetVelocityParams().MaxVelocity)),
            write_func=lambda x: self.device.SetVelocityParams(
                Decimal(x),
                Decimal(self.acceleration.value())
            )
        )
        self.acceleration.connect_to_hardware(
            read_func=lambda: float(Decimal.ToSingle(
                self.device.GetVelocityParams().Acceleration)),
            write_func=lambda x: self.device.SetVelocityParams(
                Decimal(self.velocity.value()),
                Decimal(x)
            )
        )
        self.rotation_mode.connect_to_hardware(
            write_func=lambda x: self.set_rotation_direction(x, self.rotation_direction.value())
        )
        self.rotation_direction.connect_to_hardware(
            write_func=lambda x: self.set_rotation_direction(self.rotation_mode.value(), x)
        )

        DeviceManagerCLI.BuildDeviceList()
        for item in DeviceManagerCLI.GetDeviceList():
            self.log.info(f"Detected device: {item}")

    def _manual_adjustments(self):
        self.enabled.read_task.run()
        self.actuator.read_task.run()
        self.motor_state.read_task.run()
        self.angle.read_task.run()
        self.velocity.read_task.run()
        self.acceleration.read_task.run()
        range = 360.0
        max_movetime = 1000 * 2.0 * range / self.velocity.value()  # in ms
        self.move_timeout.setValue(int(max_movetime))
        # TODO: write_to_device for mode and direction rely that mode/direction are not None!
        # (as they use each other in write_func)
        self.rotation_mode.setValue("Total angle")
        self.rotation_direction.setValue("Forwards")
        self.rotation_mode.write_to_device("Total angle")
        self.rotation_direction.write_to_device("Forwards")

    def interrupt_move(self):
        if self.host is None:
            raise Exception('not connected')
        # TODO send a stop moving command to the device
        self._aborted = True

    def home_device(self) -> None:
        """Takes care of homing in case device is not connected.
        """
        # TODO this should be part of the device, not hardware controller.
        if self.device is None:
            self.log.error('device not connected')
            raise Exception('device not connected')
        if self.device.CanHome:
            self.device.Home(30000)

    def toggle_enable(self, enable: bool) -> None:
        # TODO this should be part of the device, not hardware controller.
        if self.device is None:
            self.log.error('device not connected')
            return
        if enable:
            toggle = self.device.EnableDevice
        else:
            toggle = self.device.DisableDevice
        toggle()

    def set_rotation_direction(self, rotation_mode: str, rot_direction: str):
        if self.device is None:
            raise Exception("device not connected")
        map_mode = {
            "Fixed range": RotationSettings.RotationModes.LinearRange,
            "Total angle": RotationSettings.RotationModes.RotationalUnlimited,
            "Equivalent angle": RotationSettings.RotationModes.RotationalRange
        }
        map_direction = {
            "Quickest": RotationSettings.RotationDirections.Quickest,
            "Forwards": RotationSettings.RotationDirections.Forwards,
            "Reverse": RotationSettings.RotationDirections.Reverse
        }
        mode = map_mode.get(rotation_mode, None)
        direction = map_direction.get(rot_direction, None)

        if direction is None:
            raise ValueError(f"unrecognized direction {rot_direction}")
        if mode is None:
            raise ValueError(f"unrecognized mode {rotation_mode}")
        self.device.SetRotationModes(
            mode,
            direction
        )
        self.rotation_mode.setValue(rotation_mode)
        self.rotation_direction.setValue(rot_direction)

    def disconnect(self):
        if self.device is not None:
            self.device.StopPolling()
            self.device.DisconnectTidyUp()
            self.device.Disconnect()
            self.device = None
