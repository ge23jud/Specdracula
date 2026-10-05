import sys
sys.path.insert(0, 'C:/WSI/turbo')

import logging
import sys
import os
import datetime as dt
from time import sleep
import ScopeFoundry as SFT
import qdarkstyle
from qt_material import apply_stylesheet
from PySide6 import QtWidgets, QtCore

# Hardware components
from HardwareComponents.thorlabs_powermeter import ThorlabsPowerMeterHW
from HardwareComponents.arduino_shutter import ArduinoShutterHW
from HardwareComponents.thorlabs_motors import ThorlabsKDC101_PRMTZ8
from HardwareComponents.piezo_jena_NV403CLE import PiezoJenaNV40_HW
from HardwareComponents.andor_camera import AndorCCDHW
from HardwareComponents.andor_spec import AndorSpectrographHW
from HardwareComponents.thorlabs_laser import ThorlabsKLSLaserHW
from power_axis_adapters import HWPPowerAxisAdapter, LaserPowerAxisAdapter

from MeasurementComponents.XYMeasurement import XYMeasurementModule
from MeasurementComponents.Photoluminescence import PhotoluminescenceModule
from MeasurementComponents.dashboard import DashboardModule, DashboardView
from MeasurementComponents.status import StatusModule, StatusView
from MeasurementComponents.Map import MapModule
from MeasurementComponents.Spotsize import SpotsizeModule
from MeasurementComponents.PowerCalibration import PowerCalibrationModule


def set_initial(param, value):
    """Set initial value and target value of a parameter.
    
    
    TODO This is a hack, and should be part of ObjectParameter
    or elsewhere.
    """
    if isinstance(param, SFT.PhysicalParameter):
        param.target_value.setValue(value)
        param.target_value.setValue(value)
    param.setValue(value)
    param.setDefault(value)



class SpecDracula(SFT.TurboControl):
    name = 'Specdracula'
    available_modules = {}
    
    def setup(self):
        
        self.log.info('setup')
        
        dashboard = DashboardModule(name='Dashboard')
        xymeasurement = XYMeasurementModule(name="XYMeasurement")
        photoluminescence = PhotoluminescenceModule(name="Photoluminescence")
        status = StatusModule(name='Status')
        map = MapModule(name="2D Map")
        spotsize = SpotsizeModule(name="Spotsize")
        powercalibration = PowerCalibrationModule(name="Power Calibration")

        # Powermeter setup
        power_meter = ThorlabsPowerMeterHW(name='PM100')
        _temp = power_meter.find_param_by_name('Port')
        set_initial(_temp, 'ASRL14::INSTR')
        _temp = power_meter.find_param_by_name('Friendly name')
        set_initial(_temp, 'Powermeter')
        power_meter.connect()

        # # Shutter setup
        shutter = ArduinoShutterHW(name='Shutter 1')
        _temp = shutter.find_param_by_name('Port')
        set_initial(_temp, 'ASRL57::INSTR')
        _temp = shutter.find_param_by_name('Shutter ID')
        set_initial(_temp, 11)
        shutter.connect()

        # HWP setup
        hwp_motor = ThorlabsKDC101_PRMTZ8(name='HWP Rotation')
        _temp = hwp_motor.find_param_by_name('Serial number')
        set_initial(_temp, '27253212')  # KDC101 serial number
        hwp_motor.connect()

        # Laser 2 setup (Thorlabs KLS635 K-Cube Laser Source)
        laser2 = ThorlabsKLSLaserHW(name='Laser 2 (KLS635)')
        _temp = laser2.find_param_by_name('Serial number')
        set_initial(_temp, '56534954')  # KLS635 serial number
        #laser2.connect()

        # Piezo setup
        piezo_stage = PiezoJenaNV40_HW(name='Piezo stage')
        _temp = piezo_stage.find_param_by_name('Port')
        set_initial(_temp, 'ASRL12::INSTR')
        _temp = piezo_stage.find_param_by_name('Friendly name')
        set_initial(_temp, "Piezo stage")
        piezo_stage.connect()

        ccd_camera = AndorCCDHW(name='AndorCCD')
        _temp = ccd_camera.find_param_by_name('Friendly name')
        set_initial(_temp, "Camera")
        ccd_camera.connect()

        spec = AndorSpectrographHW(name='AndorSpectrograph')
        _temp = spec.find_param_by_name('Friendly name')
        set_initial(_temp, "Spectrograph")
        spec.connect()

        photoluminescence.camera.setValue(ccd_camera)
        photoluminescence.spectrograph.setValue(spec)
        photoluminescence.hwp.setValue(hwp_motor)
        photoluminescence.powermeter.setValue(power_meter)
        photoluminescence.shutter.setValue(shutter)

        dashboard.camera.setValue(ccd_camera)
        dashboard.spectrograph.setValue(spec)
        dashboard.halfwaveplate.setValue(hwp_motor)
        dashboard.piezo.setValue(piezo_stage)
        dashboard.shutter.setValue(shutter)
        dashboard.laser2.setValue(laser2)
        dashboard.connect()

        spotsize.powermeter.setValue(power_meter)
        spotsize.piezo.setValue(piezo_stage)

        map.camera.setValue(ccd_camera)
        map.spectrograph.setValue(spec)
        map.piezo.setValue(piezo_stage)

        powercalibration.powermeter.setValue(power_meter)
        powercalibration.hwp.setValue(hwp_motor)
        powercalibration.status.setValue(status)

        photoluminescence.status.setValue(status)

        spotsize.status.setValue(status)

        status.powermeter.setValue(power_meter)

        # Power axis adapter (see power_axis_adapters.py) -- lets the powerseries
        # sweep loops call one uniform method regardless of which laser/power
        # control mechanism is active.
        hwp_power_adapter = HWPPowerAxisAdapter(hwp_motor)
        photoluminescence.active_power_adapter = hwp_power_adapter
        powercalibration.active_power_adapter = hwp_power_adapter

        # Active-laser selector (dashboard combo box) -- reassigns the power
        # adapter (and its unit/range) on every consumer module.
        laser_power_adapters = {
            "Laser 1 (HWP)": hwp_power_adapter,
            "Laser 2 (KLS)": LaserPowerAxisAdapter(laser2),
        }
        _current_laser_choice = ["Laser 1 (HWP)"]
        power_axis_consumers = (photoluminescence, powercalibration)

        def _apply_laser_choice(choice):
            adapter = laser_power_adapters[choice]
            for consumer in power_axis_consumers:
                consumer.active_power_adapter = adapter
                for pname in ("ps_start", "ps_stop", "ps_step"):
                    p = getattr(consumer, pname)
                    p.set_unit(adapter.unit)
                    p.set_range(adapter.range)
                    p.setValue(adapter.range.min)

        def _on_active_laser_changed():
            choice = dashboard.active_laser.value()
            if choice == _current_laser_choice[0]:
                return
            running = any(c.measurement_running.value() for c in power_axis_consumers)
            if running:
                logging.getLogger(__name__).warning(
                    'Refusing to switch active laser while a measurement is running.'
                )
                dashboard.active_laser.setValue(_current_laser_choice[0])
                return
            laser_power_adapters[_current_laser_choice[0]].to_min()
            _apply_laser_choice(choice)
            _current_laser_choice[0] = choice

        dashboard.active_laser.sigValueChanged.connect(_on_active_laser_changed)


    def setup_ui(self, main_window):
        self.main_window = main_window
    

    def create_dashboard_dock(self):
        """Create and add dashboard as docked widget."""
        from MeasurementComponents.dashboard import DashboardView
        
        dashboard_view = DashboardView(self.dashboard)
            
        self.dashboard_dock = QtWidgets.QDockWidget("Hardware Control", self.main_window)
        self.dashboard_dock.setWidget(dashboard_view)
        
        self.dashboard_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | 
            QtCore.Qt.RightDockWidgetArea
        )
        
        self.dashboard_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetClosable
        )
        
        self.main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dashboard_dock)
        self.dashboard_dock.setMinimumWidth(300)


    def create_status_display_dock(self):
        """Create status display stacked below dashboard on the right."""
        from MeasurementComponents.status import StatusView
        
        status_view = StatusView(self.status)
        
        self.status_dock = QtWidgets.QDockWidget("Status", self.main_window)
        self.status_dock.setWidget(status_view)
        
        self.status_dock.setTitleBarWidget(QtWidgets.QWidget())

        self.status_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | 
            QtCore.Qt.RightDockWidgetArea
        )
        
        self.status_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetClosable
        )
        
        status_view.Power_Label.setStyleSheet("""
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

        status_view.Temperature_Label.setStyleSheet("""
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

        # Split the dashboard dock vertically - status goes below
        # self.main_window.splitDockWidget(
        #     self.dashboard_dock,
        #     self.status_dock,
        #     QtCore.Qt.Vertical  # Stack vertically
        # )
        
        #Set size constraints - small height for status
        self.status_dock.setMaximumHeight(240)
        self.status_dock.setMinimumHeight(240)
        self.status_dock.setMinimumWidth(300)
        
        # Store reference
        self.status_view = status_view


if __name__ == "__main__":
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(threadName)s:%(name)s: %(message)s",
        level=logging.DEBUG
    )
    app = SpecDracula()
    app.setup()

    filepath = f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}"
    if not os.path.isdir(filepath):

        os.makedirs(filepath)

    window = SFT.TurboMainWindow()

    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    apply_stylesheet(app, theme="dark_purple.xml")
    app.setStyleSheet(app.styleSheet())

    app.setup_ui(window)



    window.show()
    sys.exit(app.exec())