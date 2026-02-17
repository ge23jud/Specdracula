from PySide6 import QtCore
import datetime as dt

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter

class XYMeasurementModule(Module):
    
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    save_filenumber = SFT.ObjectParameter("Save Filenumber", dtype=int, value=0)
    save_string = SFT.ObjectParameter("Save String", dtype=str, value="", readonly=True)
    sweep_start = SFT.ObjectParameter("Sweep Start", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°" )
    sweep_stop = SFT.ObjectParameter("Sweep Stop", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    sweep_step = SFT.ObjectParameter("Sweep Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    sweep_parameter = SFT.ObjectParameter("Sweep Parameter", dtype=str, value="Power HWP Position", range=SFT.ChoiceRangeType(**{"Power HWP Position": 0, "Piezo X": 1, "Piezo Y": 2}))
    measured_parameter = SFT.ObjectParameter("Measurement Parameter", dtype=str, value="Photoluminescence", range=SFT.ChoiceRangeType(**{"Photoluminescence": 0, "Power": 1}))
    #todo plot_xaxis = SFT.ObjectParameter("Plot X Axis", dtype=str, value="Energy", range=SFT.ChoiceRangeType(*{"Energy"}))


    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.sweep_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.sweep_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.sweep_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
   

    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        n = int((self.sweep_stop.value()-self.sweep_start.value())/self.sweep_step.value()) + 1
        self.n_measurements.setValue(n)