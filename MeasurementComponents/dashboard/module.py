from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions

class DashboardModule(Module):

    halfwaveplate = SFT.ObjectParameter("HWP", SFT.TurboComponent)
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    fourier_camera = SFT.ObjectParameter('Fourier Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    piezo = SFT.ObjectParameter('Piezo', SFT.TurboComponent)
    shutter = SFT.ObjectParameter('Shutter', SFT.TurboComponent)
    laser2 = SFT.ObjectParameter('Laser 2', SFT.TurboComponent)

    center_wavelength = SFT.PhysicalParameter("Center Wavelength", dtype=float, value=1e-6, unit="m")

    center_energy = SFT.PhysicalParameter("Center Energy", dtype=float, value=1.2, unit="eV")
    integration_time = SFT.PhysicalParameter("Integration Time", dtype=float, value=1., unit="s")
    cmos_exposure_time = SFT.PhysicalParameter("CMOS Exposure Time", dtype=float, value=10., unit="ms")
    cmos_gain = SFT.PhysicalParameter("CMOS Gain", dtype=float, value=0.)
    piezo_x = SFT.PhysicalParameter("Piezo X", dtype=float, value=0., unit="um")
    piezo_y = SFT.PhysicalParameter("Piezo Y", dtype=float, value=0., unit="um")
    piezo_step = SFT.ObjectParameter("Piezo Step", dtype=float, value=0.1, unit="um")
    hwp_position = SFT.PhysicalParameter("HWP Position", dtype=float, value=45., unit="°")
    selected_grating = SFT.PhysicalParameter('Selected grating', dtype=str, value="150 l/mm", range=SFT.ChoiceRangeType(**{"150 l/mm": 1, "300 l/mm": 2}))
    input_mirror = SFT.PhysicalParameter("Input Mirror", dtype=str, value="Direct", range=SFT.ChoiceRangeType(**{"Direct": 0, "Side": 1}))
    output_mirror = SFT.PhysicalParameter("Output Mirror", dtype=str, value="Side", range=SFT.ChoiceRangeType(**{"Direct": 0, "Side": 1}))
    direct_input_slit_width = SFT.PhysicalParameter("Direct Input Slit Width", dtype=float, value=500e-6, unit="m", range=SFT.MinMaxRangeType(min=10e-6, max=2000e-6))
    side_input_slit_width = SFT.PhysicalParameter("Side Input Slit Width", dtype=float, value=500e-6, unit="m", range=SFT.MinMaxRangeType(min=10e-6, max=2000e-6))
    excitation_shutter = SFT.PhysicalParameter("Excitation Shutter", dtype=bool, value=False)
    laser2_on = SFT.PhysicalParameter("Laser On", dtype=bool, value=False)
    laser2_power = SFT.PhysicalParameter("Laser 2 Power", dtype=float, value=0., unit="mW")
    active_laser = SFT.ObjectParameter(
        "Active Laser", dtype=str, value="Laser 1 (HWP)",
        range=SFT.ChoiceRangeType(**{"Laser 1 (HWP)": 0, "Laser 2 (KLS)": 1})
    )

    step_up_ActionParam = SFT.ActionParameter('Step Up')
    step_down_ActionParam = SFT.ActionParameter('Step Down')
    step_left_ActionParam = SFT.ActionParameter('Step Left')
    step_right_ActionParam = SFT.ActionParameter('Step Right')

    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self.task_step_up    = SFT.WorkerTask("Step Up",    lambda: self._step('y', +1), default_thread_pool=self.thread_pool)
        self.task_step_down  = SFT.WorkerTask("Step Down",  lambda: self._step('y', -1), default_thread_pool=self.thread_pool)
        self.task_step_left  = SFT.WorkerTask("Step Left",  lambda: self._step('x', -1), default_thread_pool=self.thread_pool)
        self.task_step_right = SFT.WorkerTask("Step Right", lambda: self._step('x', +1), default_thread_pool=self.thread_pool)
        self.step_up_ActionParam.sigActivated.connect(lambda: self.task_step_up.run_on_pool())
        self.step_down_ActionParam.sigActivated.connect(lambda: self.task_step_down.run_on_pool())
        self.step_left_ActionParam.sigActivated.connect(lambda: self.task_step_left.run_on_pool())
        self.step_right_ActionParam.sigActivated.connect(lambda: self.task_step_right.run_on_pool())

    def connect(self):

        self.spec = self.spectrograph.value()
        self.dev_id = self.spec.device_id.value()
        self.cam = self.camera.value()

        self.Helper = HelperFunctions()

        self.hwp_position.connect_to_hardware(
            read_func=self.get_HWP_position,
            write_func=self.set_HWP_position
        )     

        self.integration_time.connect_to_hardware(
            read_func=self.get_integration_time,
            write_func=self.set_integration_time
        )

        self.fourier_cam = self.fourier_camera.value()

        self.cmos_exposure_time.connect_to_hardware(
            read_func=self.get_cmos_exposure_time,
            write_func=self.set_cmos_exposure_time
        )
        self.cmos_exposure_time.set_range(self.fourier_cam.exposure_time.range)

        self.cmos_gain.connect_to_hardware(
            read_func=self.get_cmos_gain,
            write_func=self.set_cmos_gain
        )
        self.cmos_gain.set_range(self.fourier_cam.gain.range)

        self.center_wavelength.connect_to_hardware(
            read_func=self.get_center_wavelength,
            write_func=self.set_center_wavelength
        )

        self.center_energy.connect_to_hardware(
            read_func=self.get_center_energy,
            write_func=self.set_center_energy
        )

        self.selected_grating.connect_to_hardware(
            read_func=self.get_selected_grating,
            write_func=self.set_selected_grating
        )

        self.direct_input_slit_width.connect_to_hardware(
            read_func=self.get_direct_input_slit_width,
            write_func=self.set_direct_input_slit_width
        )
        self.direct_input_slit_width.write_to_device(500e-6).wait(5.0)

        self.side_input_slit_width.connect_to_hardware(
            read_func=self.get_side_input_slit_width,
            write_func=self.set_side_input_slit_width
        )
        self.side_input_slit_width.write_to_device(500e-6).wait(5.0)

        self.input_mirror.connect_to_hardware(
            read_func=self.get_input_mirror,
            write_func=self.set_input_mirror
        )

        self.output_mirror.connect_to_hardware(
            read_func=self.get_output_mirror,
            write_func=self.set_output_mirror
        )

        self.piezo_x.connect_to_hardware(
            read_func=self.get_piezo_x,
            write_func=self.set_piezo_x
        )

        self.piezo_y.connect_to_hardware(
            read_func=self.get_piezo_y,
            write_func=self.set_piezo_y
        )

        self.excitation_shutter.connect_to_hardware(
            read_func=self.get_excitation_shutter,
            write_func=self.set_excitation_shutter
        )

        self.laser2_on.connect_to_hardware(
            read_func=self.get_laser2_on,
            write_func=self.set_laser2_on
        )

        self.laser2_power.connect_to_hardware(
            read_func=self.get_laser2_power,
            write_func=self.set_laser2_power
        )
        laser2 = self.laser2.value()
        self.laser2_power.set_range(laser2.power_setpoint.range)
        self.laser2_power.set_unit(laser2.power_setpoint.unit)

        # Integration time, HWP position, and laser 2 on/power can all change
        # from elsewhere (e.g. a PL powerseries sweep moves the HWP or laser 2
        # directly). Rather than polling the hardware on a timer -- which raced
        # with Live PL acquisition and HWP moves and made both unresponsive --
        # mirror the driver's own parameters, which are kept current after
        # every move/change regardless of who made it.
        hwp = self.halfwaveplate.value()
        hwp.angle.sigValueChanged.connect(self._on_hwp_angle_changed)
        self._on_hwp_angle_changed()  # seed with the already-current value

        self.cam.exposure.sigValueChanged.connect(self._on_exposure_changed)
        self._on_exposure_changed()  # seed with the already-current value

        self.fourier_cam.exposure_time.sigValueChanged.connect(self._on_cmos_exposure_changed)
        self._on_cmos_exposure_changed()  # seed with the already-current value

        self.fourier_cam.gain.sigValueChanged.connect(self._on_cmos_gain_changed)
        self._on_cmos_gain_changed()  # seed with the already-current value

        laser2.is_on.sigValueChanged.connect(self._on_laser2_on_changed)
        self._on_laser2_on_changed()  # seed with the already-current value

        laser2.power_setpoint.sigValueChanged.connect(self._on_laser2_power_changed)
        self._on_laser2_power_changed()  # seed with the already-current value

    @QtCore.Slot()
    def _on_hwp_angle_changed(self):
        self.hwp_position.setValue(self.halfwaveplate.value().angle.value())

    @QtCore.Slot()
    def _on_exposure_changed(self):
        self.integration_time.setValue(self.cam.exposure.value())

    @QtCore.Slot()
    def _on_cmos_exposure_changed(self):
        self.cmos_exposure_time.setValue(self.fourier_cam.exposure_time.value())

    @QtCore.Slot()
    def _on_cmos_gain_changed(self):
        self.cmos_gain.setValue(self.fourier_cam.gain.value())

    @QtCore.Slot()
    def _on_laser2_on_changed(self):
        self.laser2_on.setValue(self.laser2.value().is_on.value())

    @QtCore.Slot()
    def _on_laser2_power_changed(self):
        self.laser2_power.setValue(self.laser2.value().power_setpoint.value())

    def set_output_mirror(self, mirror):
        self.spec.host.SetFlipperMirror(int(self.dev_id), 2, int(self.output_mirror.range[mirror]))

    def get_output_mirror(self):
        return self.spec.host.GetFlipperMirror(int(self.dev_id), 2)
    
    def set_input_mirror(self, mirror):
        self.spec.host.SetFlipperMirror(int(self.dev_id), 1, int(self.input_mirror.range[mirror]))

    def get_input_mirror(self):
        return self.spec.host.GetFlipperMirror(int(self.dev_id), 1)
    
    def set_direct_input_slit_width(self, width):
        self.spec.host.SetSlitWidth(int(self.dev_id), int(2), width=float(width * 1e6))

    def get_direct_input_slit_width(self):
        return float(self.spec.host.GetSlitWidth(int(self.dev_id), int(2)) / 1e6)
    
    def set_side_input_slit_width(self, width):
        self.spec.host.SetSlitWidth(int(self.dev_id), int(1), width=float(width * 1e6))

    def get_side_input_slit_width(self):
        return float(self.spec.host.GetSlitWidth(int(self.dev_id), int(1)) / 1e6)

    def set_selected_grating(self, grating):
        self.spec.host.SetGrating(int(self.dev_id), self.selected_grating.range[grating])

    def get_selected_grating(self):
        return self.spec.host.GetGrating(int(self.dev_id))

    def set_HWP_position(self, angle):
        hwp = self.halfwaveplate.value()
        hwp.write_angle(angle)

    def get_HWP_position(self):
         hwp = self.halfwaveplate.value()
         return hwp.read_angle()
    
    def set_integration_time(self, time):
        self.cam.host.SetExposureTime(time)

    def get_integration_time(self):
        return self.cam._get_acquisition_timings()[0]

    def set_cmos_exposure_time(self, value_ms):
        exposure = self.fourier_cam.exposure_time
        exposure.write_to_device(value_ms)
        # write_to_device alone doesn't refresh exposure.value() -- without this
        # read-back, _on_cmos_exposure_changed never fires and the dashboard
        # spinbox would silently keep showing the old value after a write.
        exposure.trigger_read().wait(2.0)

    def get_cmos_exposure_time(self):
        return self.fourier_cam.exposure_time.value()

    def set_cmos_gain(self, value):
        # gain.range.max == gain.range.min means this camera doesn't support
        # adjustable gain (see ThorlabsCS165HW.connect) -- its write_func was
        # never wired to hardware, so writing would be a no-op at best.
        gain = self.fourier_cam.gain
        if gain.range.max > gain.range.min:
            gain.write_to_device(value)
            gain.trigger_read().wait(2.0)

    def get_cmos_gain(self):
        return self.fourier_cam.gain.value()

    def set_center_wavelength(self, wavelength):
        self.spec.host.SetWavelength(int(self.dev_id), float(wavelength / 1e-9))
        self.center_energy.trigger_read()

    def get_center_wavelength(self):
        return float(self.spec.host.GetWavelength(int(self.dev_id))) * 1e-9
    
    def set_center_energy(self, energy):
        self.spec.host.SetWavelength(int(self.dev_id), float(self.Helper.wavelength_energy_converter(energy)))
        self.center_wavelength.trigger_read()


    def get_center_energy(self):
        return float(self.Helper.wavelength_energy_converter(self.spec.host.GetWavelength(int(self.dev_id))))

    def set_piezo_x(self, x_um):
        self.piezo.value().set_position_SI('x', x_um * 1e-6)

    def get_piezo_x(self):
        return self.piezo.value().get_single_position_SI('x') * 1e6

    def set_piezo_y(self, y_um):
        self.piezo.value().set_position_SI('y', y_um * 1e-6)

    def get_piezo_y(self):
        return self.piezo.value().get_single_position_SI('y') * 1e6

    def set_excitation_shutter(self, is_open):
        # Checkbox "Shutter open": checked -> shutter open. The mapping to the
        # driver is inverted relative to set_shutter_state's open/closed flag.
        shutter = self.shutter.value()
        shutter.device.set_shutter_state(shutter.shutter_id.value(), not bool(is_open))

    def get_excitation_shutter(self):
        shutter = self.shutter.value()
        return not shutter.device.get_shutter_state(shutter.shutter_id.value())

    def set_laser2_on(self, on):
        laser2 = self.laser2.value()
        laser2.device.set_output_enabled(bool(on))
        laser2.is_on.setValue(bool(on))

    def get_laser2_on(self):
        return self.laser2.value().device.get_output_enabled()

    def set_laser2_power(self, value):
        laser2 = self.laser2.value()
        laser2.device.set_power_setpoint(value)
        laser2.power_setpoint.setValue(value)

    def get_laser2_power(self):
        return self.laser2.value().device.get_power_setpoint()

    def _step(self, axis, direction):
        piezo = self.piezo.value()
        current_m = piezo.get_single_position_SI(axis)
        piezo.set_position_SI(axis, current_m + direction * self.piezo_step.value() * 1e-6)
        if axis == 'x':
            self.piezo_x.trigger_read()
        else:
            self.piezo_y.trigger_read()