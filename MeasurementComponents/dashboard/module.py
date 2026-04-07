from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions

class DashboardModule(Module):

    halfwaveplate = SFT.ObjectParameter("HWP", SFT.TurboComponent)
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)

    center_wavelength = SFT.PhysicalParameter("Center Wavelength", dtype=float, value=1e-6, unit="m")
    center_energy = SFT.PhysicalParameter("Center Energy", dtype=float, value=1.2, unit="eV")
    integration_time = SFT.PhysicalParameter("Integration Time", dtype=float, value=1., unit="s")
    piezo_x = SFT.PhysicalParameter("Piezo X", dtype=float, value=0., unit="um")
    piezo_y = SFT.PhysicalParameter("Piezo Y", dtype=float, value=0., unit="um")
    piezo_step = SFT.PhysicalParameter("Piezo Step", dtype=float, value=0.1, unit="um")
    hwp_position = SFT.PhysicalParameter("HWP Position", dtype=float, value=45., unit="°")
    grating = SFT.PhysicalParameter("Grating", dtype=str, )


    def connect(self):

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
        

    def set_HWP_position(self, angle):
        hwp = self.halfwaveplate.value()
        hwp.write_angle(angle)

    def get_HWP_position(self):
         hwp = self.halfwaveplate.value()
         return hwp.read_angle()
    
    def set_integration_time(self, time):
        cam = self.camera.value()
        cam.host.SetExposureTime(time)

    def get_integration_time(self):
        cam = self.camera.value()
        return cam._get_acquisition_timings()[0]
    
    def set_center_wavelength(self, wavelength):
        spec = self.spectrograph.value()
        dev_id = spec.device_id.value()
        spec.host.SetWavelength(int(dev_id), float(wavelength / 1e-9))
        self.center_energy.trigger_read()

    def get_center_wavelength(self):
        spec = self.spectrograph.value()
        dev_id = spec.device_id.value()
        return float(spec.host.GetWavelength(int(dev_id))) * 1e-9
    
    def set_center_energy(self, energy):
        spec = self.spectrograph.value()
        dev_id = spec.device_id.value()
        Helper = HelperFunctions()
        spec.host.SetWavelength(int(dev_id), float(Helper.wavelength_energy_converter(energy)))
        self.center_wavelength.trigger_read()


    def get_center_energy(self):
        spec = self.spectrograph.value()
        dev_id = spec.device_id.value()
        Helper = HelperFunctions()
        return float(Helper.wavelength_energy_converter(spec.host.GetWavelength(int(dev_id))))