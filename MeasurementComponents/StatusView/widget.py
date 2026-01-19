from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .status_ui import Ui_StatusWidget

class StatusView(TurboComponentView, Ui_StatusWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)