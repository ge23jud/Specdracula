import logging
from datetime import datetime

import numpy as np
from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import HardwareModule, PhysicalParameter, ActionParameter, WorkerTask

logger = logging.getLogger("ThorlabsCS165")


class ThorlabsCS165HW(HardwareModule):

    serial_number = SFT.ObjectParameter("Serial number", dtype=str, value="")

    exposure_time = PhysicalParameter(
        name="Exposure time", dtype=float, unit="ms", value=10.0,
        range=SFT.MinMaxRangeType(min=0.04, max=26843.0, decimals=3)
    )
    gain = PhysicalParameter(
        name="Gain", dtype=float, value=0.0,
        range=SFT.MinMaxRangeType(min=0, max=0, decimals=0)
    )
    is_streaming = PhysicalParameter(name="Live view on", dtype=bool, value=False, readonly=True)
    most_recent_frame = PhysicalParameter(name="Most recent frame", dtype=np.ndarray)

    start_live_view_ActionParam = ActionParameter(name="Start live view")
    stop_live_view_ActionParam = ActionParameter(name="Stop live view")

    def __init__(self, *args, **kwargs):
        HardwareModule.__init__(self, *args, **kwargs)
        self.device = None
        self.bit_depth = 16
        self._stop_requested = False
        self.poll_task = WorkerTask(
            "Poll CMOS frames", self._poll_frame,
            default_thread_pool=self.thread_pool
        )
        # this must be here, not in connect: making connections to objects created in different
        # threads is not possible and will fail silently!
        self.start_live_view_ActionParam.sigActivated.connect(self.trigger_start_live_view)
        self.stop_live_view_ActionParam.sigActivated.connect(self.trigger_stop_live_view)

    def connect(self):
        from .thorlabs_cs165_dev import ThorlabsCS165Camera
        self.device = ThorlabsCS165Camera(self.serial_number.value())
        self.device.connect()

        min_exposure_ms, max_exposure_ms = self.device.get_exposure_range_ms()
        self.exposure_time.set_range(SFT.MinMaxRangeType(min=min_exposure_ms, max=max_exposure_ms, decimals=3))
        self.bit_depth = self.device.get_bit_depth()

        self.exposure_time.connect_to_hardware(
            read_func=self.device.get_exposure_time_ms,
            write_func=self.device.set_exposure_time_ms
        )
        self.exposure_time.trigger_read().wait(2.0)

        gain_min, gain_max = self.device.get_gain_range()
        self.gain.set_range(SFT.MinMaxRangeType(min=gain_min, max=gain_max, decimals=0))
        if gain_max > gain_min:
            self.gain.connect_to_hardware(
                read_func=self.device.get_gain,
                write_func=self.device.set_gain
            )
            self.gain.trigger_read().wait(2.0)

    def disconnect(self):
        if self.device is not None:
            self.trigger_stop_live_view()
            self.device.disconnect()
            self.device = None

    @QtCore.Slot()
    def trigger_start_live_view(self):
        if self.device is None or self.is_streaming.value():
            return
        self.device.start_streaming()
        self.is_streaming.setValue(True)
        self._stop_requested = False
        self.poll_task.run_on_pool()

    @QtCore.Slot()
    def trigger_stop_live_view(self):
        self._stop_requested = True
        if self.device is not None:
            self.device.stop_streaming()
        self.is_streaming.setValue(False)

    def _poll_frame(self):
        if self._stop_requested or self.device is None:
            return None
        # Poll timeout must comfortably exceed the exposure time, or every poll
        # times out before a frame is ready (silently -- get_latest_frame just
        # returns None) whenever exposure is long.
        timeout_ms = max(200, int(self.exposure_time.value() * 2) + 100)
        frame = self.device.get_latest_frame(timeout_ms=timeout_ms)
        if frame is not None:
            self.most_recent_frame.setValue(frame)
            self.most_recent_frame.actual_timestamp.setValue(datetime.now())
        if not self._stop_requested:
            self.poll_task.run_on_pool()
        return frame
