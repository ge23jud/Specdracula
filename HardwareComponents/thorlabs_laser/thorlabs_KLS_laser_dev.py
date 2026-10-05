import sys
import time

_KINESIS_DIR = r"C:\Program Files\Thorlabs\Kinesis"
if _KINESIS_DIR not in sys.path:
    sys.path.insert(0, _KINESIS_DIR)

import clr
import System

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.LaserSourceCLI")

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.LaserSourceCLI import KCubeLaserSource, InputSourceSettings

LaserSourceInputSourceFlags = InputSourceSettings.LaserSourceInputSourceFlags


def _to_float(decimal_value):
    """pythonnet's System.Decimal doesn't support Python's float() directly."""
    return float(str(decimal_value))


class ThorlabsKLSLaser:
    """Thin wrapper around Thorlabs' Kinesis .NET API for a KCube Laser
    Source (KLS635/KLS1550), via pythonnet.

    There is no pylablib support for this device family (only KinesisMotor,
    KinesisPiezoController, etc.) -- this talks directly to the same
    Thorlabs.MotionControl.KCube.LaserSourceCLI.dll the Kinesis GUI uses,
    whose API surface was confirmed via .NET reflection against the real
    installed assembly rather than assumed from documentation.
    """

    def __init__(self, serial_number, polling_interval_ms=250):
        self.serial_number = serial_number
        self._polling_interval_ms = polling_interval_ms
        self._device = None
        self._last_setpoint = 0.0

    def connect(self):
        DeviceManagerCLI.BuildDeviceList()
        device = KCubeLaserSource.CreateKCubeLaserSource(self.serial_number)
        device.Connect(self.serial_number)
        device.WaitForSettingsInitialized(5000)
        device.StartPolling(self._polling_interval_ms)
        device.EnableDevice()
        time.sleep(0.5)  # let the first poll land before reading status
        device.RequestStatus()
        device.RequestReadings()
        # Force deterministic behavior: ignore the front-panel wheel and the
        # EXT IN analog input, respond only to our software setpoints.
        device.SetControlSource(LaserSourceInputSourceFlags.SoftwareOnly)
        time.sleep(0.5)  # let polling pick up the new control source + readings
        self._device = device

        # GetSetPower()'s value is a polled register that lags unpredictably
        # (observed: still stale after 1.5s in some cases) -- only read it
        # once here for the real starting value, then track our own writes
        # from here on (safe since SoftwareOnly means we're the only writer).
        for _ in range(10):
            device.RequestSetPower()
            time.sleep(0.3)
        self._last_setpoint = _to_float(device.GetSetPower())

    def disconnect(self):
        if self._device is None:
            return
        try:
            self._device.SetOff()
            self._wait_while(self._device.IsLaserSetOnOffActive, timeout=5.0)
        except Exception:
            pass
        self._device.StopPolling()
        self._device.DisableDevice()
        self._device.Disconnect(True)
        self._device = None

    def get_output_enabled(self):
        return bool(self._device.Status.LaserEnabled)

    def set_output_enabled(self, on):
        if on:
            self._device.SetOn()
        else:
            self._device.SetOff()
        self._wait_while(self._device.IsLaserSetOnOffActive, timeout=5.0)

    def get_power_setpoint(self):
        return self._last_setpoint

    def set_power_setpoint(self, value):
        self._device.SetPower(System.Decimal(float(value)))
        self._wait_while(self._device.IsSetPowerActive, timeout=5.0)
        self._last_setpoint = float(value)

    def get_power_reading(self):
        return _to_float(self._device.GetPowerReading())

    def get_power_limits(self):
        limits = self._device.GetLimits()
        return 0.0, _to_float(limits.MaxPower)

    def get_interlock_ok(self):
        status = self._device.Status
        return bool(status.SafetyInterlockEnabled and status.KeyEnabled)

    def get_wavelength_nm(self):
        return _to_float(self._device.GetWavelength())

    def _wait_while(self, is_active_func, timeout):
        deadline = time.monotonic() + timeout
        while is_active_func() and time.monotonic() < deadline:
            time.sleep(0.05)
