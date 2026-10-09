import os
import logging

import numpy as np

logger = logging.getLogger("ThorlabsCS165")

# The Scientific Camera Interfaces SDK ships its Python Toolkit dlls/64_lib
# folder empty (just a "copy native libraries here" placeholder) -- the ThorCam
# application install already contains the exact same native DLLs
# (thorlabs_tsi_camera_sdk.dll and its dependencies), so point there directly.
_DEFAULT_DLL_DIRS = [
    r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam",
    r"C:\Program Files\Thorlabs\Scientific Imaging\Scientific Camera Support\Scientific Camera Interfaces\SDK\Python Toolkit\dlls\64_lib",
]


def _add_dll_directory(dll_dir=None):
    """Make the native TSI camera DLLs loadable before importing thorlabs_tsi_sdk.

    thorlabs_tsi_sdk is a ctypes wrapper around the native TLCamera_*.dll's
    shipped with the Scientific Camera Interfaces SDK -- a plain pip install
    of the Python package does not put those DLLs on the search path.
    """
    candidates = [dll_dir] if dll_dir else _DEFAULT_DLL_DIRS
    for path in candidates:
        if path and os.path.isdir(path):
            os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
            os.add_dll_directory(path)
            return path
    raise FileNotFoundError(
        "Could not find the Thorlabs TSI camera DLLs. Looked in: "
        f"{', '.join(c for c in candidates if c)}. "
        "Install the Scientific Camera Interfaces SDK from thorlabs.com/software, "
        "or pass dll_dir= explicitly."
    )


class ThorlabsCS165Camera:
    """Thin wrapper around Thorlabs' thorlabs_tsi_sdk for a Zelux CS165
    Compact Scientific Camera (CMOS, 1440 x 1080, 3.45 um pixels, 10-bit ADC).

    Uses the SDK's continuous-streaming mode: setting
    frames_per_trigger_zero_for_unlimited=0 and issuing a single software
    trigger starts free-running acquisition; frames are then retrieved one at
    a time via get_pending_frame_or_null().
    """

    def __init__(self, serial_number="", dll_dir=None):
        self.serial_number = serial_number
        self._dll_dir = dll_dir
        self._sdk = None
        self._camera = None

    def connect(self):
        _add_dll_directory(self._dll_dir)
        from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

        self._sdk = TLCameraSDK()
        available_cameras = self._sdk.discover_available_cameras()
        if not available_cameras:
            raise RuntimeError("No Thorlabs TSI cameras found.")
        camera_id = self.serial_number if self.serial_number in available_cameras else available_cameras[0]
        self._camera = self._sdk.open_camera(camera_id)
        self.serial_number = camera_id
        self._camera.frames_per_trigger_zero_for_unlimited = 0  # continuous mode

    def disconnect(self):
        if self._camera is not None:
            try:
                self.stop_streaming()
            except Exception:
                pass
            self._camera.dispose()
            self._camera = None
        if self._sdk is not None:
            self._sdk.dispose()
            self._sdk = None

    def start_streaming(self):
        self._camera.arm(2)
        self._camera.issue_software_trigger()

    def stop_streaming(self):
        if self._camera.is_armed:
            self._camera.disarm()

    def get_latest_frame(self, timeout_ms=200):
        """Poll for the most recent frame, waiting up to timeout_ms.

        Returns a 2D numpy array (height x width) or None if no frame arrived
        within the timeout.
        """
        self._camera.image_poll_timeout_ms = timeout_ms
        frame = self._camera.get_pending_frame_or_null()
        if frame is None:
            return None
        return np.copy(frame.image_buffer).reshape(
            self._camera.image_height_pixels, self._camera.image_width_pixels
        )

    def get_exposure_time_ms(self):
        return self._camera.exposure_time_us / 1000.0

    def set_exposure_time_ms(self, value_ms):
        self._camera.exposure_time_us = int(round(value_ms * 1000.0))

    def get_exposure_range_ms(self):
        exposure_range = self._camera.exposure_time_range_us
        return exposure_range.min / 1000.0, exposure_range.max / 1000.0

    def get_bit_depth(self):
        """ADC bit depth (e.g. 10) -- pixel values never exceed 2**bit_depth - 1,
        a small fraction of the 16-bit range a saved frame is stored in."""
        return self._camera.bit_depth

    def get_gain(self):
        return self._camera.gain

    def set_gain(self, value):
        self._camera.gain = int(round(value))

    def get_gain_range(self):
        """(min, max) raw gain index. max == 0 means gain is not supported by
        this camera -- callers should treat that as "no adjustable gain"."""
        gain_range = self._camera.gain_range
        return gain_range.min, gain_range.max
