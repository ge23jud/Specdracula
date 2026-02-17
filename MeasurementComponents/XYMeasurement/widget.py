from PySide6 import QtCore
import ScopeFoundry as SFT

from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .XYMeasurement_ui import Ui_XYMeasurementWidget


class XYMeasurementView(TurboComponentView, Ui_XYMeasurementWidget):


    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)
        self.setup_plot()

        self.sweep_start_map = {"Power HWP Position": {"unit": "°", 
                                                           "range": SFT.MinMaxRangeType(min=0.0, max=360, decimals=1)}, 
                                    "Piezo X": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=-40e-6, max=40e-6, decimals=9)},
                                    "Piezo Y": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=-40e-6, max=40e-6, decimals=9)}}
        
        self.sweep_stop_map = {"Power HWP Position": {"unit": "°", 
                                                           "range": SFT.MinMaxRangeType(min=0.0, max=360, decimals=1)}, 
                                    "Piezo X": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=-40e-6, max=40e-6, decimals=9)},
                                    "Piezo Y": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=-40e-6, max=40e-6, decimals=9)}}
        
        self.sweep_step_map = {"Power HWP Position": {"unit": "°", 
                                                           "range": SFT.MinMaxRangeType(min=0.0, max=360, decimals=1)}, 
                                    "Piezo X": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=0.0, max=80e-6, decimals=9)},
                                    "Piezo Y": {"unit": "m",
                                                "range": SFT.MinMaxRangeType(min=0.0, max=80e-6, decimals=9)}}

        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)
        SFT.connect_widget_to_param(self.SweepParameter_ComboBox, component.sweep_parameter)
        SFT.connect_widget_to_param(self.MeasuredParameter_ComboBox, component.measured_parameter)
        SFT.connect_widget_to_param(self.SweepStart_DoubleSpinBox, component.sweep_start)
        SFT.connect_widget_to_param(self.SweepStop_DoubleSpinBox, component.sweep_stop)
        SFT.connect_widget_to_param(self.SweepStep_DoubleSpinBox, component.sweep_step)

        component.sweep_parameter.sigValueChanged.connect(self._on_sweep_parameter_changed)
        component.n_measurements.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_label)



    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Energy", units="eV")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)


    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))


    @QtCore.Slot()
    def _on_sweep_parameter_changed(self):
    # Set property of Sweep ObjectParams dynamically depending on which sweep parameter is selected
        
        param = self.component.sweep_parameter.value()
        self.component.sweep_start.set_unit(self.sweep_start_map[param]["unit"])
        self.component.sweep_start.set_range(self.sweep_start_map[param]["range"])
        self.component.sweep_stop.set_unit(self.sweep_stop_map[param]["unit"])
        self.component.sweep_stop.set_range(self.sweep_stop_map[param]["range"])
        self.component.sweep_step.set_unit(self.sweep_step_map[param]["unit"])
        self.component.sweep_step.set_range(self.sweep_step_map[param]["range"])
        
    
    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))