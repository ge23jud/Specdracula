import sys
sys.path.insert(0, 'C:/WSI/turbo')
import ScopeFoundry as SFT
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

hwp_motor = ThorlabsKDC101(name='HWP Rotation')
_temp = hwp_motor.find_param_by_name('Serial number')
set_initial(_temp, '27253212')  # Your KDC101 serial number
hwp_motor.connect()

hwp_motor.write_angle(180)