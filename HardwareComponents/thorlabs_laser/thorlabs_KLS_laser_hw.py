import ScopeFoundry as SFT
from .thorlabs_KLS_laser_dev import ThorlabsKLSLaser


class ThorlabsKLSLaserHW(SFT.HardwareModule):

    serial_number = SFT.ObjectParameter("Serial number", dtype=str, value="")

    is_on = SFT.PhysicalParameter("Laser On", dtype=bool, value=False)
    power_setpoint = SFT.PhysicalParameter(
        "Power Setpoint", dtype=float, value=0.0, unit="mW",
        range=SFT.MinMaxRangeType(min=0.0, max=8.0, decimals=3)
    )
    power_reading = SFT.PhysicalParameter(
        "Power Reading", dtype=float, value=0.0, unit="mW", readonly=True
    )
    interlock_ok = SFT.PhysicalParameter(
        "Interlock/Key OK", dtype=bool, value=False, readonly=True
    )

    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self.device = None

    def connect(self):
        self.device = ThorlabsKLSLaser(self.serial_number.value())
        self.device.connect()

        min_power, max_power = self.device.get_power_limits()
        self.power_setpoint.set_range(SFT.MinMaxRangeType(min=min_power, max=max_power, decimals=3))

        self.is_on.connect_to_hardware(read_func=self._read_is_on, write_func=self._write_is_on)
        self.power_setpoint.connect_to_hardware(read_func=self._read_power_setpoint, write_func=self._write_power_setpoint)
        self.power_reading.connect_to_hardware(read_func=self._read_power_reading)
        self.interlock_ok.connect_to_hardware(read_func=self._read_interlock_ok)

        self.is_on.trigger_read().wait(2.0)
        self.power_setpoint.trigger_read().wait(2.0)
        self.power_setpoint.target_value.setValue(self.power_setpoint.value())
        self.power_reading.trigger_read().wait(2.0)
        self.interlock_ok.trigger_read().wait(2.0)

    def disconnect(self):
        if self.device is not None:
            try:
                self.device.set_output_enabled(False)
            except Exception:
                pass
            self.device.disconnect()
            self.device = None

    def _read_is_on(self):
        return self.device.get_output_enabled()

    def _write_is_on(self, on):
        self.device.set_output_enabled(on)

    def _read_power_setpoint(self):
        return self.device.get_power_setpoint()

    def _write_power_setpoint(self, value):
        self.device.set_power_setpoint(value)

    def _read_power_reading(self):
        return self.device.get_power_reading()

    def _read_interlock_ok(self):
        return self.device.get_interlock_ok()
