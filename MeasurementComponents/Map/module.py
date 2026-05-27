from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from time import sleep
from ScopeFoundry import Module
from helperfunctions import HelperFunctions
import os


class MapModule(Module):

    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    piezo = SFT.ObjectParameter('Piezo', SFT.TurboComponent)

    x_start = SFT.ObjectParameter("X Start", dtype=float, value=0., unit="m")
    y_start = SFT.ObjectParameter("Y Start", dtype=float, value=0., unit="m")
    x_stop = SFT.ObjectParameter("X Stop", dtype=float, value=1e-6, unit="m")
    y_stop = SFT.ObjectParameter("Y Stop", dtype=float, value=1e-6, unit="m")
    x_step = SFT.ObjectParameter("X Step", dtype=float, value=1e-7, unit="m")
    y_step = SFT.ObjectParameter("Y Step", dtype=float, value=1e-7, unit="m")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    map_data = SFT.ObjectParameter("Map Data", dtype=np.ndarray, value=None, readonly=True)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\\Measurements\\{dt.date.today().__str__().replace('-', '')}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")

    run_ActionParam = SFT.ActionParameter('Run Map')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt')

    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.x_start.sigValueChanged.connect(self.update_no_measurements)
        self.x_stop.sigValueChanged.connect(self.update_no_measurements)
        self.x_step.sigValueChanged.connect(self.update_no_measurements)
        self.y_start.sigValueChanged.connect(self.update_no_measurements)
        self.y_stop.sigValueChanged.connect(self.update_no_measurements)
        self.y_step.sigValueChanged.connect(self.update_no_measurements)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        self.task_run = SFT.WorkerTask("Run Map", self.run_map, default_thread_pool=self.thread_pool)
        self._interrupted = False
        self._goto_x = 0.0
        self._goto_y = 0.0
        self.task_goto = SFT.WorkerTask("Go to position", self._goto_target, default_thread_pool=self.thread_pool)

        self.run_ActionParam.sigActivated.connect(lambda: self.task_run.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)

        self.update_no_measurements()

    @QtCore.Slot()
    def interrupt(self):
        self._interrupted = True

    def move_to(self, x, y):
        self._goto_x = x
        self._goto_y = y
        self.task_goto.run_on_pool()

    def _goto_target(self):
        piezo = self.piezo.value()
        if piezo is None:
            return
        piezo.set_position_SI('x', self._goto_x)
        piezo.set_position_SI('y', self._goto_y)

    @QtCore.Slot()
    def update_no_measurements(self):
        x_step = self.x_step.value()
        y_step = self.y_step.value()
        if x_step <= 0 or y_step <= 0:
            return
        nx = int((self.x_stop.value() - self.x_start.value()) / x_step) + 1
        ny = int((self.y_stop.value() - self.y_start.value()) / y_step) + 1
        self.n_measurements.setValue(nx * ny)

    def run_map(self):
        self._interrupted = False
        cam = self.camera.value()
        piezo = self.piezo.value()

        x_positions = np.arange(
            self.x_start.value(),
            self.x_stop.value() + self.x_step.value() * 0.5,
            self.x_step.value()
        )
        y_positions = np.arange(
            self.y_start.value(),
            self.y_stop.value() + self.y_step.value() * 0.5,
            self.y_step.value()
        )
        nx, ny = len(x_positions), len(y_positions)

        map_data = np.full((nx, ny), np.nan)
        self.map_data.setValue(map_data.copy())
        filepath = self.update_save_string()

        for iy, y in enumerate(y_positions):
            if self._interrupted:
                break
            piezo.set_position_SI('y', y)
            piezo.get_single_position_SI('y')

            for ix, x in enumerate(x_positions):
                if self._interrupted:
                    break
                piezo.set_position_SI('x', x)
                piezo.get_single_position_SI('x')

                wait_task = cam.trigger_acquisition()
                wait_task.wait(cam.acc_cycle_time.value() + self.extra_timeout.value())
                counts = cam.acquire_wait.result[0].copy()
                map_data[ix, iy] = float(np.sum(counts))
                self.map_data.setValue(map_data.copy())

        self._save_map(x_positions, y_positions, map_data, filepath)

    def _save_map(self, x_positions, y_positions, map_data, filepath):
        with open(filepath, 'w') as f:
            f.write('Y \\ X\t' + '\t'.join(f'{x:.9f}' for x in x_positions) + '\n')
            for iy, y in enumerate(y_positions):
                row = '\t'.join(
                    f'{map_data[ix, iy]:.1f}' if not np.isnan(map_data[ix, iy]) else ''
                    for ix in range(len(x_positions))
                )
                f.write(f'{y:.9f}\t{row}\n')

    def update_save_string(self):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        helper = HelperFunctions()
        filenumber = helper.get_next_file_number(dir)
        return f"{dir}\\{filenumber}_{file}_map.txt"

    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
