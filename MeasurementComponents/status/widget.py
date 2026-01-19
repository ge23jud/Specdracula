from PySide6 import QtCore, QtWidgets
from ScopeFoundry import TurboComponentView, connect_widget_to_param
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
                border: 0px solid #9C27B0;  /* Optional: purple border */
                border-radius: 3px;          /* Optional: rounded corners */
            }
        """)

        self.Temperature_Label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #232629;
                font-size: 30pt;
                font-weigth: bold;
                padding: 5px;
                border: 0px solid #9C27B0;  /* Optional: purple border */
                border-radius: 3px;          /* Optional: rounded corners */
            }
        """)