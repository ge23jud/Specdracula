from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from time import sleep
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions
import os


class PowerCalibrationModule(Module):

    hwp = SFT.ObjectParameter("HWP", SFT.TurboComponent)
    powermeter = SFT.ObjectParameter("Powermeter", SFT.TurboComponent)
    status = SFT.ObjectParameter("Status", SFT.TurboComponent)

    ps_start = SFT.ObjectParameter("Power HWP Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°")
    ps_stop = SFT.ObjectParameter("Power HWP Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    ps_step = SFT.ObjectParameter("Power HWP Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.1, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=46)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\\Measurements\\{dt.date.today().__str__().replace('-', '')}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    angles_buffer = SFT.ObjectParameter("HWP Angles", dtype=np.ndarray, unit="°", value=np.array([]))
    powers_buffer = SFT.ObjectParameter("Powers", dtype=np.ndarray, unit="W", value=np.array([]))

    interrupt_ActionParam = SFT.ActionParameter('Interrupt')
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
        self._interrupted = False
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._run()
        finally:
            if status is not None:
                status.resume()

    def _run(self):
        start = self.ps_start.value()
        stop = self.ps_stop.value()
        step = self.ps_step.value()
        hwp = self.hwp.value()
        pm = self.powermeter.value()

        datetime = dt.datetime.now()
        positions = np.arange(start, stop + step * 0.5, step)
        angles = []
        powers = []

        for pos in positions:
            if self._interrupted:
                break
            hwp.write_angle(pos)
            sleep(0.2)
            pm.reading.trigger_read().wait(2.0)
            p = pm.reading.value()
            angles.append(pos)
            powers.append(p)
            self.angles_buffer.setValue(np.array(angles))
            self.powers_buffer.setValue(np.array(powers))

        excitation_power_uw = float(np.max(powers)) * 1e6 if powers else 0.0
        filepath = self.update_save_string()
        HelperFunctions().write_powercal_origin(
            date=datetime,
            temperature=0.0,
            integration_time=0.0,
            excitation_power_uw=excitation_power_uw,
            center_wavelength=0.0,
            dispersion_window=0.0,
            entrance_slit_width=0.0,
            exit_slit_width=0.0,
            angles=np.array(angles),
            powers=np.array(powers),
            filepath=filepath,
        )

    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        step = self.ps_step.value()
        if step <= 0:
            return
        n = int((self.ps_stop.value() - self.ps_start.value()) / step) + 1
        self.n_measurements.setValue(n)

    def update_save_string(self):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        helper = HelperFunctions()
        filenumber = helper.get_next_file_number(dir)
        return f"{dir}\\{filenumber}_{file}_powercalibration.origin"

    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
