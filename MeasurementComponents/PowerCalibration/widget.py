from PySide6 import QtCore
import ScopeFoundry as SFT
import pyqtgraph as pg
import numpy as np
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .PowerCalibration_ui import Ui_PowerCalibrationWidget

from PySide6 import QtCore, QtWidgets


class PowerCalibrationView(TurboComponentView, Ui_PowerCalibrationWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)

        self.setupUi(self)
        self.setup_plot()

        SFT.connect_widget_to_param(self.PsStart_DoubleSpinBox, component.ps_start)
        SFT.connect_widget_to_param(self.PsStop_DoubleSpinBox, component.ps_stop)
        SFT.connect_widget_to_param(self.PsStep_DoubleSpinBox, component.ps_step)
        SFT.connect_widget_to_param(self.SettleTime_DoubleSpinBox, component.settle_time)
        SFT.connect_widget_to_param(self.AveragingTime_DoubleSpinBox, component.averaging_time)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)
        SFT.connect_widget_to_param(self.StartPS_PushButton, component.run_ActionParam)
        SFT.connect_widget_to_param(self.StopPS_PushButton, component.interrupt_ActionParam)

        component.n_measurements.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_label)
        component.powers_buffer.sigValueChanged.connect(self._update_plot)

    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Power", units="W")
        self.plot_widget.setLabel("bottom", "HWP Angle", units="deg")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)
        self.power_plotDataItem = self.plot_widget.plot([], [], pen="#35b779", symbol='o', symbolSize=5)

    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))

    @QtCore.Slot()
    def _update_plot(self):
        angles = self.component.angles_buffer.value()
        powers = self.component.powers_buffer.value()
        if angles is not None and powers is not None and len(angles) > 0:
            self.power_plotDataItem.setData(x=angles, y=powers)
