import sys
sys.path.insert(0, 'C:/WSI/turbo')

import logging
import sys
from time import sleep
import ScopeFoundry as SFT

# Hardware components
from HardwareComponents.thorlabs_powermeter import ThorlabsPowerMeterHW
from HardwareComponents.arduino_shutter import ArduinoShutterHW
from HardwareComponents.thorlabs_motors import ThorlabsKDC101

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
        
        # Powermeter setup
        power_meter = ThorlabsPowerMeterHW(name='PM100')
        _temp = power_meter.find_param_by_name('Port')
        set_initial(_temp, 'ASRL19::INSTR')
        _temp = power_meter.find_param_by_name('Friendly name')
        set_initial(_temp, 'Powermeter')
        power_meter.connect()

        # Shutter setup
        shutter = ArduinoShutterHW(name='Shutter 1')
        _temp = shutter.find_param_by_name('Port')
        set_initial(_temp, 'ASRL11::INSTR')
        _temp = shutter.find_param_by_name('Shutter ID')
        set_initial(_temp, 10)
        shutter.connect()

        # HWP setup
        hwp_motor = ThorlabsKDC101(name='HWP Rotation')
        _temp = hwp_motor.find_param_by_name('Serial number')
        set_initial(_temp, '27253212')  # Your KDC101 serial number
        hwp_motor.connect()


if __name__ == "__main__":
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(threadName)s:%(name)s: %(message)s",
        level=logging.DEBUG
    )
    app = SpecDracula()
    app.setup()
    window = SFT.TurboMainWindow()
    window.show()
    sys.exit(app.exec())