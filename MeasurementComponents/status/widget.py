from PySide6 import QtCore
import ScopeFoundry as SFT
from ScopeFoundry import TurboComponentView
from .status_ui import Ui_StatusWidget


class StatusView(TurboComponentView, Ui_StatusWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)

        self.Power_Label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #232629;
                font-size: 30pt;
                font-weigth: bold;
                padding: 5px;
                border: 0px solid #9C27B0;
                border-radius: 3px;
            }
        """)

        self.Temperature_Label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #232629;
                font-size: 30pt;
                font-weigth: bold;
                padding: 5px;
                border: 0px solid #9C27B0;
                border-radius: 3px;
            }
        """)

        SFT.connect_widget_to_param(self.Start_PushButton, component.start_ActionParam)
        SFT.connect_widget_to_param(self.Stop_PushButton, component.stop_ActionParam)

        component.power.sigValueChanged.connect(self._update_power_label)

    @QtCore.Slot()
    def _update_power_label(self):
        p_mw = self.component.power.value() * 1e3
        self.Power_Label.setText(f"{p_mw:.3f}")
