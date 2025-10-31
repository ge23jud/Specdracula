import logging
from functools import wraps

from pyAndorSDK2 import atmcd

logger = logging.getLogger("AndorCCD")


def err_wrapper(func):
    """Wrapper for calls to atmcd object that takes care of the error codes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        retval = func(*args, **kwargs)
        if hasattr(retval, "__len__") and len(retval) > 1:
            err_code = retval[0]
            output = retval[1:]
            if hasattr(output, "__len__") and len(output) == 1:
                output = output[0]
        else:
            err_code = retval
            output = retval
        AndorCameraDiscovery.last_error = err_code
        logger.debug(
            f'pyAndorSDK2 call to {func.__name__}, args: {args}, err code: {err_code}, output: {output}')
        return output

    return wrapped


class AndorCameraDiscovery(atmcd):

    def discover_hardware(self):
        self.Initialize("")
        n_devices = self.GetNumberDevices()
        # AndorCameraDiscovery._devices = [AndorCCDHW(n) for n in range(n_devices)]
        # return AndorCameraDiscovery._devices

    def disconnect(self):
        pass

    def __del__(self):
        self.disconnect()

    def __getattribute__(self, name):
        attr = super(AndorCameraDiscovery, self).__getattribute__(name)
        if callable(attr):
            attr = err_wrapper(attr)
        return attr
