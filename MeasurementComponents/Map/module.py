from PySide6 import QtCore
import datetime as dt

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter


class MapModule(Module):
    
    x_start = SFT.ObjectParameter("X Start", dtype=float, value=0., unit="m")    
    y_start = SFT.ObjectParameter("Y Start", dtype=float, value=0., unit="m")
    x_stop = SFT.ObjectParameter("X Stop", dtype=float, unit="m", value=1e-6)
    y_stop = SFT.ObjectParameter("Y Stop", dtype=float, value=1e-6, unit="m")
    x_step = SFT.ObjectParameter("X Step", dtype=float, value=1e-7, unit="m")
    y_step = SFT.ObjectParameter("Y Step", dtype=float, value=0.1e-6, unit="m")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    save_filenumber = SFT.ObjectParameter("Save Filenumber", dtype=int, value=0)
    save_string = SFT.ObjectParameter("Save String", dtype=str, value="", readonly=True) 


    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.x_start.sigValueChanged.connect(self.update_no_measurements)
        self.x_stop.sigValueChanged.connect(self.update_no_measurements)
        self.x_step.sigValueChanged.connect(self.update_no_measurements)
        self.y_start.sigValueChanged.connect(self.update_no_measurements)
        self.y_stop.sigValueChanged.connect(self.update_no_measurements)
        self.y_step.sigValueChanged.connect(self.update_no_measurements)

        self.update_no_measurements()


    @QtCore.Slot()
    def update_no_measurements(self):

        nx = int((self.x_stop.value() - self.x_start.value()) / self.x_step.value()) + 1
        ny = int((self.y_stop.value() - self.y_start.value()) / self.y_step.value()) + 1
        n = nx * ny

        self.n_measurements.setValue(n)
