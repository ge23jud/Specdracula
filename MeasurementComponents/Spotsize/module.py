from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from time import sleep
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions
import os


class SpotsizeModule(Module):

    # devices
    powermeter = SFT.ObjectParameter("Powermeter", SFT.TurboComponent)
    piezo = SFT.ObjectParameter("Piezo", SFT.TurboComponent)

    #y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    #x_label = SFT.ObjectParameter("X Label", dtype=str, value="Wavelength", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")
    start = SFT.ObjectParameter("Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="m" )
    stop = SFT.ObjectParameter("Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="m")
    #n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    #extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    #position_um = SFT.ObjectParameter('Wavelength', dtype=np.ndarray, unit='nm', value=None, readonly=True)
    #power = SFT.ObjectParameter('Power', dtype=np.ndarray, value=None, readonly=True)

    #save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    #save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    # save_string = SFT.ObjectParameter("Save String", dtype=str, value="", readonly=True) 

    run_ActionParam = SFT.ActionParameter('Run Spotsize Calibration')




    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
   
        # self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        # '''Connect action parameters to ui buttons'''
        self.task_run = SFT.WorkerTask("Run Spotsize Calibration", self.run_spotsize, default_thread_pool=self.thread_pool)
        # self.task_single = SFT.WorkerTask("Acquire single", self.acquire_single, default_thread_pool=self.thread_pool)
        # self.task_save_single = SFT.WorkerTask("Save PL Snapshot", self.save_single, default_thread_pool=self.thread_pool)
        # self.task_continuous = SFT.WorkerTask("Acquire continuous", self.acquire_continuous, default_thread_pool=self.thread_pool)
        # self.task_powerseries = SFT.WorkerTask("Run Powerseries", self.powerseries, default_thread_pool=self.thread_pool)

        self.run_ActionParam.sigActivated.connect(lambda: self.task_run.run_on_pool())
        # self.single_ActionParam.sigActivated.connect(lambda: self.task_single.run_on_pool())
        # self.save_single_ActionParam.sigActivated.connect(lambda: self.task_save_single.run_on_pool())
        # self.continuous_ActionParam.sigActivated.connect(lambda: self.task_continuous.run_on_pool())
        # self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        # self.powerseries_ActionParam.sigActivated.connect(lambda: self.task_powerseries.run_on_pool())
        # self._interrupted = False
        # #self.file_exporters["HDF files (*.h5)"] = AndorCCDReadoutMeasure.to_hdf

        # self.wavelength_nm.sigValueChanged.connect(self._update_energy_array)


    def run_spotsize(self):
        piezo = self.piezo.value()
        pm = self.powermeter.value()
        positions = np.linspace(self.start.value(), self.stop.value(), 75)
        with open("C:\WSI\specdracula\spotsize.txt", "w") as f:
            for pos in positions:
                piezo.set_position("y", pos)
                sleep(0.5)
                x = piezo.get_single_position("y")
                pm.reading.trigger_read()
                p = pm.reading.value()
                f.write(f"{x}\t{p}\n")




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

        