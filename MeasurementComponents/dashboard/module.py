from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions

class DashboardModule(Module):

    halfwaveplate = SFT.ObjectParameter("HWP", SFT.TurboComponent)
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    piezo = SFT.ObjectParameter('Piezo', SFT.TurboComponent)

    center_wavelength = SFT.PhysicalParameter("Center Wavelength", dtype=float, value=1e-6, unit="m")

    center_energy = SFT.PhysicalParameter("Center Energy", dtype=float, value=1.2, unit="eV")
    integration_time = SFT.PhysicalParameter("Integration Time", dtype=float, value=1., unit="s")
    piezo_x = SFT.PhysicalParameter("Piezo X", dtype=float, value=0., unit="um")
    piezo_y = SFT.PhysicalParameter("Piezo Y", dtype=float, value=0., unit="um")
    piezo_step = SFT.ObjectParameter("Piezo Step", dtype=float, value=0.1, unit="um")
    hwp_position = SFT.PhysicalParameter("HWP Position", dtype=float, value=45., unit="°")
    selected_grating = SFT.PhysicalParameter('Selected grating', dtype=str, value="150 l/mm", range=SFT.ChoiceRangeType(**{"150 l/mm": 1, "300 l/mm": 2}))
    input_mirror = SFT.PhysicalParameter("Input Mirror", dtype=str, value="Direct", range=SFT.ChoiceRangeType(**{"Direct": 0, "Side": 1}))
    output_mirror = SFT.PhysicalParameter("Output Mirror", dtype=str, value="Side", range=SFT.ChoiceRangeType(**{"Direct": 0, "Side": 1}))
    direct_input_slit_width = SFT.PhysicalParameter("Direct Input Slit Width", dtype=float, value=100e-6, unit="m", range=SFT.MinMaxRangeType(min=10e-6, max=2000e-6))
    side_input_slit_width = SFT.PhysicalParameter("Side Input Slit Width", dtype=float, value=100e-6, unit="m", range=SFT.MinMaxRangeType(min=10e-6, max=2000e-6))

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

        self.side_input_slit_width.connect_to_hardware(
            read_func=self.get_side_input_slit_width,
            write_func=self.set_side_input_slit_width
        )

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

    def _step(self, axis, direction):
        piezo = self.piezo.value()
        current_m = piezo.get_single_position_SI(axis)
        piezo.set_position_SI(axis, current_m + direction * self.piezo_step.value() * 1e-6)
        if axis == 'x':
            self.piezo_x.trigger_read()
        else:
            self.piezo_y.trigger_read()