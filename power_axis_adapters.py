import ScopeFoundry as SFT


class PowerAxisAdapter:
    """Uniform interface so power-sweep loops don't need to branch on which
    laser (and which physical power-control mechanism) is currently active."""

    unit = ""
    range = SFT.MinMaxRangeType()

    def set_setpoint(self, value):
        raise NotImplementedError

    def to_min(self):
        """Push the axis to its safe/minimum-power state, used when switching
        away from this laser."""
        raise NotImplementedError

    def supports_log_calibration(self):
        """Whether a separate angle<->power calibration curve is needed to
        place log-spaced sweep points (true for the HWP, false for a laser
        with its own closed-loop power setpoint)."""
        return False


class HWPPowerAxisAdapter(PowerAxisAdapter):
    unit = "°"
    range = SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2)

    def __init__(self, hwp):
        self._hwp = hwp

    def set_setpoint(self, value):
        self._hwp.write_angle(value)

    def to_min(self):
        self._hwp.write_angle(0.0)

    def supports_log_calibration(self):
        return True


class LaserPowerAxisAdapter(PowerAxisAdapter):
    def __init__(self, laser):
        self._laser = laser
        self.unit = laser.power_setpoint.unit
        self.range = laser.power_setpoint.range

    def set_setpoint(self, value):
        self._laser.device.set_power_setpoint(value)
        self._laser.power_setpoint.setValue(value)

    def to_min(self):
        self._laser.device.set_power_setpoint(self.range.min)
        self._laser.device.set_output_enabled(False)
        self._laser.power_setpoint.setValue(self.range.min)
        self._laser.is_on.setValue(False)

    def supports_log_calibration(self):
        return False
