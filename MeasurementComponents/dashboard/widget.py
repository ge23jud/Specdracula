from PySide6 import QtCore, QtWidgets
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .dashboard_ui import Ui_DashboardWidget
import ScopeFoundry as SFT


class _WheelEventBlocker(QtCore.QObject):
    """Prevents mouse-wheel scrolling from changing the watched widget's value.

    Users have accidentally changed settings (e.g. grating, input/output mirror)
    by scrolling the dashboard while the cursor happened to be over a combo box
    or spin box. Forwarding the wheel event to the scroll area's viewport instead
    keeps normal page-scrolling working while making these controls click-only.
    """

    def __init__(self, scroll_area, parent=None):
        super().__init__(parent)
        self._scroll_area = scroll_area

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.Type.Wheel:
            QtWidgets.QApplication.sendEvent(self._scroll_area.viewport(), event)
            return True
        return False


class DashboardView(TurboComponentView, Ui_DashboardWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)

        # Make group boxes collapsible
        self.setup_collapsible_groups()
        self.disable_scroll_to_change()

        SFT.connect_widget_to_param(self.CenterWavelength_DoubleSpinBox, component.center_wavelength)
        SFT.connect_widget_to_param(self.CenterEnergy_DoubleSpinBox, component.center_energy)
        SFT.connect_widget_to_param(self.IntegrationTime_DoubleSpinBox, component.integration_time)
        SFT.connect_widget_to_param(self.PiezoX_DoubleSpinBox, component.piezo_x)
        SFT.connect_widget_to_param(self.PiezoY_DoubleSpinBox, component.piezo_y)
        SFT.connect_widget_to_param(self.PiezoStep_DoubleSpinBox, component.piezo_step)
        SFT.connect_widget_to_param(self.HWPPos_DoubleSpinBox, component.hwp_position)
        SFT.connect_widget_to_param(self.DirectInputSlit_DoubleSpinBox, component.direct_input_slit_width)
        SFT.connect_widget_to_param(self.SideInputSlit_DoubleSpinBox, component.side_input_slit_width)
        SFT.connect_widget_to_param(self.PiezoUp_Button, component.step_up_ActionParam)
        SFT.connect_widget_to_param(self.PiezoDown_Button, component.step_down_ActionParam)
        SFT.connect_widget_to_param(self.PiezoLeft_Button, component.step_left_ActionParam)
        SFT.connect_widget_to_param(self.PiezoRight_Button, component.step_right_ActionParam)
        SFT.connect_widget_to_param(self.Shutter_CheckBox, component.excitation_shutter)
        SFT.connect_widget_to_param(self.ActiveLaser_ComboBox, component.active_laser)
        SFT.connect_widget_to_param(self.Laser2On_CheckBox, component.laser2_on)
        SFT.connect_widget_to_param(self.Laser2Power_DoubleSpinBox, component.laser2_power)

    
    def disable_scroll_to_change(self):
        """Make all dashboard value controls ignore mouse-wheel scrolling.

        Scrolling over a combo box or spin box would otherwise change its value
        instead of scrolling the dashboard, causing unnoticed hardware changes.
        """
        self._wheel_blocker = _WheelEventBlocker(self.scrollArea, self)
        controls = [
            self.CenterWavelength_DoubleSpinBox,
            self.CenterEnergy_DoubleSpinBox,
            self.IntegrationTime_DoubleSpinBox,
            self.PiezoX_DoubleSpinBox,
            self.PiezoY_DoubleSpinBox,
            self.PiezoStep_DoubleSpinBox,
            self.HWPPos_DoubleSpinBox,
            self.DirectInputSlit_DoubleSpinBox,
            self.SideInputSlit_DoubleSpinBox,
            self.ActiveLaser_ComboBox,
            self.Laser2Power_DoubleSpinBox,
        ]
        for control in controls:
            control.installEventFilter(self._wheel_blocker)

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