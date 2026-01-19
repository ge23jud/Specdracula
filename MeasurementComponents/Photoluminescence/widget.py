from PySide6 import QtCore
import ScopeFoundry as SFT

from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .photoluminescence_ui import Ui_PhotoluminescenceWidget

from PySide6 import QtCore, QtWidgets


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
        #SFT.connect_widget_to_param(self.IntTime_DoubleSpinBox, component.int_time)


        component.x_label.sigValueChanged.connect(self._on_xlabel_changed)
        component.n_measurements.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_label)
        

    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Energy", units="eV")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)


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

    