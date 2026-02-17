import logging
from functools import wraps
import os

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


class AndorCameraDiscovery:
    """Wrapper class for Andor SDK atmcd DLL."""
    
    last_error = None
    
    def __init__(self, dll_path=None):
        """Initialize the Andor camera discovery.
        
        Args:
            dll_path: Directory containing the Andor SDK DLL (not the full path to the DLL).
                     Defaults to C:\Program Files\Andor SDK
        """
        # The SDK expects a DIRECTORY path, not the full DLL path!
        # It will look for atmcd64d.dll or atmcd32d.dll in that directory
        if dll_path is None:
            dll_path = r"C:\Program Files\Andor SDK"
            
        if not os.path.isdir(dll_path):
            raise FileNotFoundError(
                f"Could not find Andor SDK directory at: {dll_path}\n"
                "Please specify the directory containing atmcd64d.dll"
            )
        
        logger.info(f"Using Andor SDK directory: {dll_path}")
        
        # Create an instance of the atmcd class with the directory path
        try:
            self._sdk = atmcd.atmcd(dll_path)
            logger.info(f"Successfully loaded Andor SDK")
        except Exception as e:
            logger.error(f"Failed to load Andor SDK: {e}")
            logger.error(f"Make sure atmcd64d.dll exists in: {dll_path}")
            raise
        
        
    def discover_hardware(self):
        """Initialize and discover connected Andor cameras."""
        # Initialize the SDK
        init_result = self._call_wrapped('Initialize', "")
        logger.info(f"Initialize result: {init_result}")
        
        # Get number of devices
        n_devices = self._call_wrapped('GetNumberDevices')
        logger.info(f"Found {n_devices} Andor device(s)")
        return n_devices
    
    def _call_wrapped(self, method_name, *args, **kwargs):
        """Helper to call a method with error wrapping."""
        method = getattr(self._sdk, method_name)
        wrapped_method = err_wrapper(method)
        return wrapped_method(*args, **kwargs)
    
    def disconnect(self):
        """Shutdown the SDK."""
        if not hasattr(self, '_sdk') or self._sdk is None:
            return
            
        try:
            shutdown_result = self._call_wrapped('ShutDown')
            logger.info(f"Andor SDK shut down successfully: {shutdown_result}")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
    
    def __getattr__(self, name):
        """Forward all other attribute access to the SDK object with error wrapping."""
        if hasattr(self._sdk, name):
            attr = getattr(self._sdk, name)
            if callable(attr):
                return err_wrapper(attr)
            return attr
        raise AttributeError(
            f"'{type(self).__name__}' object and SDK have no attribute '{name}'"
        )
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.disconnect()
        except:
            pass  # Ignore errors during cleanup