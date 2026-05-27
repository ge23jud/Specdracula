from PySide6 import QtCore
import ScopeFoundry as SFT
import numpy as np
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .Spotsize_ui import Ui_SpotsizeWidget


class SpotsizeView(TurboComponentView, Ui_SpotsizeWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)

        self.setupUi(self)
        self.setup_plot()

        SFT.connect_widget_to_param(self.Start_DoubleSpinBox, component.start)
        SFT.connect_widget_to_param(self.Stop_DoubleSpinBox, component.stop)
        SFT.connect_widget_to_param(self.Step_DoubleSpinBox, component.step)
        SFT.connect_widget_to_param(self.Axis_ComboBox, component.axis)
        SFT.connect_widget_to_param(self.Start_PushButton, component.run_ActionParam)
        SFT.connect_widget_to_param(self.Stop_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)

        component.run_ActionParam.sigActivated.connect(self._clear_plot)
        component.powers_buffer.sigValueChanged.connect(self._update_plot)
        component.n_measurements.sigValueChanged.connect(
            lambda: self.NumMeasurements_Label.setText(str(component.n_measurements.value()))
        )

    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Power", units="W")
        self.plot_widget.setLabel("bottom", "Position", units="m")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)
        self.plot_data_item = self.plot_widget.plot([], [], pen="#35b779", symbol='o', symbolSize=4)

    @QtCore.Slot()
    def _update_plot(self):
        X = self.component.positions_buffer.value()
        Y = self.component.powers_buffer.value()
        if X is not None and Y is not None and len(X) > 0:
            self.plot_data_item.setData(x=X, y=Y)

    @QtCore.Slot()
    def _clear_plot(self):
        self.plot_data_item.setData([], [])
