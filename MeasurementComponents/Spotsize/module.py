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
    status = SFT.ObjectParameter("Status", SFT.TurboComponent)

    #y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    #x_label = SFT.ObjectParameter("X Label", dtype=str, value="Wavelength", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")
    start = SFT.ObjectParameter("Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="m")
    stop = SFT.ObjectParameter("Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="m")
    step = SFT.ObjectParameter("Step Size", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.01, max=360.0, decimals=4), unit="m")
    axis = SFT.ObjectParameter("Axis", dtype=str, value="x", range=SFT.ChoiceRangeType(**{"x": 0, "y": 1}))
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0, readonly=True)
    positions_buffer = SFT.ObjectParameter("Positions", dtype=np.ndarray, unit="m", value=np.array([]), readonly=True)
    powers_buffer = SFT.ObjectParameter("Powers", dtype=np.ndarray, unit="W", value=np.array([]), readonly=True)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\\Measurements\\{dt.date.today().__str__().replace('-', '')}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")

    run_ActionParam = SFT.ActionParameter('Run Spotsize Calibration')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt')




    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
   
        # self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        # self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        # '''Connect action parameters to ui buttons'''
        self.task_run = SFT.WorkerTask("Run Spotsize Calibration", self.run_spotsize, default_thread_pool=self.thread_pool)
        self._interrupted = False

        self.run_ActionParam.sigActivated.connect(lambda: self.task_run.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)
        self.start.sigValueChanged.connect(self._update_n_measurements)
        self.stop.sigValueChanged.connect(self._update_n_measurements)
        self.step.sigValueChanged.connect(self._update_n_measurements)
        self._update_n_measurements()


    def run_spotsize(self):
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._run_spotsize()
        finally:
            if status is not None:
                status.resume()

    def _run_spotsize(self):
        self._interrupted = False
        piezo = self.piezo.value()
        pm = self.powermeter.value()
        axis = self.axis.value()
        positions = np.arange(self.start.value(), self.stop.value() + self.step.value() * 0.5, self.step.value())
        self.positions_buffer.setValue(np.array([]))
        self.powers_buffer.setValue(np.array([]))
        pos_list = []
        pow_list = []
        filepath = self.update_save_string()
        with open(filepath, "w") as f:
            for pos in positions:
                if self._interrupted:
                    break
                piezo.set_position(axis, pos)
                sleep(0.5)
                x = piezo.get_single_position(axis)
                pm.reading.trigger_read().wait(2.0)
                p = pm.reading.value()
                pos_list.append(x)
                pow_list.append(p)
                self.positions_buffer.setValue(np.array(pos_list))
                self.powers_buffer.setValue(np.array(pow_list))
                f.write(f"{x}\t{p}\n")

    @QtCore.Slot()
    def interrupt(self):
        self._interrupted = True

    @QtCore.Slot()
    def _update_n_measurements(self):
        step = self.step.value()
        if step <= 0:
            return
        n = int((self.stop.value() - self.start.value()) / step) + 1
        self.n_measurements.setValue(n)

    def update_save_string(self):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        
        helper = HelperFunctions()
        filenumber = helper.get_next_file_number(dir)

        new_save_string = f"{dir}\\{filenumber}_{file}_spotsize.txt"
        # self.save_string.setValue(new_save_string)
        return new_save_string
    
    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)

        