from PySide6 import QtCore

from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .xymeasurement_ui import Ui_XYMeasurementWidget


class XYMeasurementView(TurboComponentView, Ui_XYMeasurementWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)
