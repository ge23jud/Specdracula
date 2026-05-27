from PySide6 import QtCore, QtWidgets
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .dashboard_ui import Ui_DashboardWidget
import ScopeFoundry as SFT

class DashboardView(TurboComponentView, Ui_DashboardWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)
        
        # Make group boxes collapsible
        self.setup_collapsible_groups()

        SFT.connect_widget_to_param(self.CenterWavelength_DoubleSpinBox, component.center_wavelength)
        SFT.connect_widget_to_param(self.CenterEnergy_DoubleSpinBox, component.center_energy)
        SFT.connect_widget_to_param(self.IntegrationTime_DoubleSpinBox, component.integration_time)
        SFT.connect_widget_to_param(self.PiezoX_DoubleSpinBox, component.piezo_x)
        SFT.connect_widget_to_param(self.PiezoY_DoubleSpinBox, component.piezo_y)
        SFT.connect_widget_to_param(self.PiezoStep_DoubleSpinBox, component.piezo_step)
        SFT.connect_widget_to_param(self.HWPPos_DoubleSpinBox, component.hwp_position)
        SFT.connect_widget_to_param(self.Grating_ComboBox, component.selected_grating)
        SFT.connect_widget_to_param(self.InputMirror_ComboBox, component.input_mirror)
        SFT.connect_widget_to_param(self.OutputMirror_ComboBox, component.output_mirror)
        SFT.connect_widget_to_param(self.DirectInputSlit_DoubleSpinBox, component.direct_input_slit_width)
        SFT.connect_widget_to_param(self.SideInputSlit_DoubleSpinBox, component.side_input_slit_width)
        SFT.connect_widget_to_param(self.PiezoUp_Button, component.step_up_ActionParam)
        SFT.connect_widget_to_param(self.PiezoDown_Button, component.step_down_ActionParam)
        SFT.connect_widget_to_param(self.PiezoLeft_Button, component.step_left_ActionParam)
        SFT.connect_widget_to_param(self.PiezoRight_Button, component.step_right_ActionParam)
        
    
    def setup_collapsible_groups(self):
        """Make group boxes collapsible by clicking their title."""
        group_boxes = [
            self.groupBox_2,  # Spectrometer
            self.groupBox_4,  # Detector
            self.groupBox_3,  # Piezo
            self.groupBox_6,  # Power Control
        ]
        
        for gb in group_boxes:
            gb.setCheckable(True)
            gb.setChecked(True)  # Start expanded
            gb.toggled.connect(lambda checked, box=gb: self.toggle_groupbox(box, checked))
    
    def toggle_groupbox(self, groupbox, checked):
        """Show/hide group box content when toggled."""
        # Find the layout inside the group box
        layout = groupbox.layout()
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    item.widget().setVisible(checked)
                elif item.spacerItem():
                    # Spacers don't need to be hidden
                    pass