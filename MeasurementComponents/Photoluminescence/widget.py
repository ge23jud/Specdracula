from PySide6 import QtCore
import ScopeFoundry as SFT
import pyqtgraph as pg
import numpy as np
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .photoluminescence_ui import Ui_PhotoluminescenceWidget

from PySide6 import QtCore, QtWidgets

plot_colors = ["#fde725", "#6ece58", "#35b779", "#1f9e89", "#26828e", "#31688e", "#3e4989", "#482878", "#440154"]

class PhotoluminescenceView(TurboComponentView, Ui_PhotoluminescenceWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        
        self.setupUi(self)
        self.setup_plot()

        SFT.connect_widget_to_param(self.yscale_ComboBox, component.y_scale)
        SFT.connect_widget_to_param(self.xlabel_ComboBox, component.x_label)
        SFT.connect_widget_to_param(self.PsStart_DoubleSpinBox, component.ps_start)
        SFT.connect_widget_to_param(self.PsStop_DoubleSpinBox, component.ps_stop)
        SFT.connect_widget_to_param(self.PsStep_DoubleSpinBox, component.ps_step)

        SFT.connect_widget_to_param(self.Snapshot_PushButton, component.single_ActionParam)
        SFT.connect_widget_to_param(self.StartLivePL_PushButton, component.continuous_ActionParam)
        SFT.connect_widget_to_param(self.StopLivePL_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.StartPS_PushButton, component.powerseries_ActionParam)


        component.x_label.sigValueChanged.connect(self._on_xlabel_changed)
        component.n_measurements.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_label)
        component.intensity_counts.sigValueChanged.connect(self._update_plot_single)
        component.intensity_counts_powerseries.sigValueChanged.connect(self._update_plot_powerseries)
        component.powerseries_ActionParam.sigActivated.connect(self._clear_plot)
        component.single_ActionParam.sigActivated.connect(self._clear_plot)
        component.continuous_ActionParam.sigActivated.connect(self._clear_plot)
        

    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Wavelength", units="nm")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)

        self.spectrum_plotDataItem = self.plot_widget.plot([], [])
        


    @QtCore.Slot()
    def _on_xlabel_changed(self):

        label_type = self.component.x_label.value()

        if label_type == "Energy":
            self.plot_widget.setLabel("bottom", "Energy", units="eV")
        else:
            self.plot_widget.setLabel("bottom", "Wavelength", units="nm")


    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))


    
    @QtCore.Slot()
    def _update_plot_single(self):
        xaxis = self.component.x_label.value()
        if xaxis == "Wavelength":
            X = self.component.wavelength_nm.value()
        elif xaxis == "Energy":
            X = self.component.energy_ev.value()
        Y = self.component.intensity_counts.value().flatten()
        if len(self.plot_widget.listDataItems()) == 0:
            self.spectrum_plotDataItem = self.plot_widget.plot(X, Y)
        else:
            self.spectrum_plotDataItem.setData(x=X, y=Y)


    @QtCore.Slot()
    def _update_plot_powerseries(self):
        num_items = len(self.plot_widget.listDataItems())
        
        xaxis = self.component.x_label.value()
        if xaxis == "Wavelength":
            X = self.component.wavelength_nm.value()
        elif xaxis == "Energy":
            X = self.component.energy_ev.value()

        Y = self.component.intensity_counts_powerseries.value().flatten()
        self.spectrum_plotDataItem = self.plot_widget.plot(X, Y, pen=plot_colors[num_items % len(plot_colors)])


    @QtCore.Slot()
    def _clear_plot(self):
        self.plot_widget.clear()
        

    