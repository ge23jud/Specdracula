from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog
import ScopeFoundry as SFT
from ScopeFoundry import TurboComponentView
from .fouriercmos_ui import Ui_FourierCMOSWidget


class FourierCMOSView(TurboComponentView, Ui_FourierCMOSWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)

        SFT.connect_widget_to_param(self.On_Button, component.on_ActionParam)
        SFT.connect_widget_to_param(self.Off_Button, component.off_ActionParam)

        SFT.connect_widget_to_param(self.PsStart_DoubleSpinBox, component.ps_start)
        SFT.connect_widget_to_param(self.PsStop_DoubleSpinBox, component.ps_stop)
        SFT.connect_widget_to_param(self.PsStep_DoubleSpinBox, component.ps_step)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)
        SFT.connect_widget_to_param(self.SavePng_CheckBox, component.save_png)
        SFT.connect_widget_to_param(self.StartPS_PushButton, component.powerseries_ActionParam)
        SFT.connect_widget_to_param(self.StopPS_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.Save_PushButton, component.save_single_ActionParam)
        SFT.connect_widget_to_param(self.ClearBackground_PushButton, component.clear_background_ActionParam)

        self.LoadBackground_PushButton.clicked.connect(self._on_load_background)

        component.live_frame.sigValueChanged.connect(self._update_image)
        component.background_frame.sigValueChanged.connect(self._update_image)
        component.background_frame.sigValueChanged.connect(self._on_background_changed)
        self._first_frame = True

    @QtCore.Slot()
    def _update_image(self):
        frame = self.component.live_frame.value()
        if frame is None:
            return
        display = self.component.get_background_subtracted(frame)
        self.img_view.setImage(display.T, autoRange=self._first_frame, autoLevels=True)
        self._first_frame = False

    @QtCore.Slot()
    def _on_background_changed(self):
        self.ClearBackground_PushButton.setEnabled(self.component.background_frame.value() is not None)

    @QtCore.Slot()
    def _on_load_background(self):
        start_dir = self.component.save_directory.value() or ""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Background Image", start_dir,
            "Background images (*.origin *.png);;Origin files (*.origin);;PNG files (*.png);;All files (*)"
        )
        if not path:
            return
        try:
            self.component.load_background(path)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Load background failed", str(e))
