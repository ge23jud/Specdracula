from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions
import os


class PowerCalibrationModule(Module):

    # devices
    hwp = SFT.ObjectParameter("HWP", SFT.TurboComponent)

    ps_start = SFT.ObjectParameter("Power HWP Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°" )
    ps_stop = SFT.ObjectParameter("Power HWP Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    ps_step = SFT.ObjectParameter("Power HWP Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    angles_buffer = SFT.ObjectParameters("HWP Angles", dtype=np.ndarray, unit="°", value=None)
    powers_buffer = SFT.ObjectParameter("Powers", dype=np.ndarray, unit="W", value=None)

    interrupt_ActionParam = SFT.ActionParameter('Interrupt Acquire')
    run_ActionParam = SFT.ActionParameter("Run Power Calibration")


    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
   
        self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        self.task_run = SFT.WorkerTask("Run Power Calibration", self.run, default_thread_pool=self.thread_pool)

        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.run_ActionParam.sigActivated.connect(lambda: self.task_run.run_on_pool())
        self._interrupted = False


    @QtCore.Slot()
    def interrupt(self):
        self._interrupted = True


    def run(self):
        start = self.ps_start.value()
        stop = self.ps_stop.value()
        step = self.ps_step.value()
        hwp = self.hwp.value()
        
        hwp.write_angle(start)

        n = self.n_measurements.value()

        datetime = dt.datetime.now()
        temperature = 0 # to implement
        integration_time = 0
        power = 0#
        center_wavelength = 1
        entrance_slit_width = 0
        exit_slit_width = 0
        excitation_power = np.zeros(n)
        filepath = self.update_save_string()


        for i in range(self.n_measurements.value()):    

            hwp.write_angle(start + i*step)

            

        intensity = self.intensity_counts_powerseries_complete.value().T
        wavelength = self.wavelength_nm.value()
        dispersion_window = wavelength[-1] - wavelength[0]

        HelperFunctions().write_origin(datetime, "Powerseries", temperature, integration_time, power, center_wavelength, dispersion_window, 
                                       entrance_slit_width, exit_slit_width, wavelength, excitation_power, intensity, filepath)



    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        n = int((self.ps_stop.value()-self.ps_start.value())/self.ps_step.value()) + 1
        self.n_measurements.setValue(n)


    def update_save_string(self):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        
        helper = HelperFunctions()
        filenumber = helper.get_next_file_number(dir)

        new_save_string =  f"{dir}\\{filenumber}_{file}.origin"
        # self.save_string.setValue(new_save_string)
        return new_save_string
    
    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if os.path.isdir(filepath):
            os.makedirs(filepath)

        