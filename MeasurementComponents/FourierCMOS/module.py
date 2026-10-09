import os
import time
import datetime as dt

import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module
from helperfunctions import HelperFunctions


class FourierCMOSModule(Module):

    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    hwp = SFT.ObjectParameter('HWP', SFT.TurboComponent)
    powermeter = SFT.ObjectParameter('Powermeter', SFT.TurboComponent)
    status = SFT.ObjectParameter('Status', SFT.TurboComponent)

    is_streaming = SFT.ObjectParameter('Live View On', dtype=bool, value=False, readonly=True)
    live_frame = SFT.ObjectParameter('Live Frame', dtype=np.ndarray, value=None, readonly=True)
    background_frame = SFT.ObjectParameter('Background Frame', dtype=np.ndarray, value=None, readonly=True)

    ps_start = SFT.ObjectParameter("Power HWP Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°")
    ps_stop = SFT.ObjectParameter("Power HWP Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    ps_step = SFT.ObjectParameter("Power HWP Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0, readonly=True)
    current_angles = SFT.ObjectParameter("Current Sweep Angles", dtype=np.ndarray, value=None, readonly=True)
    current_power_index = SFT.ObjectParameter("Current Power Index", dtype=int, value=0, readonly=True)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    powers = SFT.ObjectParameter("Powers", dtype=np.ndarray, value=None)
    measurement_running = SFT.ObjectParameter('Measurement Running', dtype=bool, value=False, readonly=True)

    save_png = SFT.ObjectParameter("Save png", dtype=bool, value=False)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")

    on_ActionParam = SFT.ActionParameter('On')
    off_ActionParam = SFT.ActionParameter('Off')
    powerseries_ActionParam = SFT.ActionParameter("Run Powerseries")
    interrupt_ActionParam = SFT.ActionParameter("Interrupt Acquire")
    save_single_ActionParam = SFT.ActionParameter("Save Image")
    clear_background_ActionParam = SFT.ActionParameter("Clear Background")

    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self.on_ActionParam.sigActivated.connect(self.start_live_view)
        self.off_ActionParam.sigActivated.connect(self.stop_live_view)

        self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        self.task_powerseries = SFT.WorkerTask("Run Powerseries", self.powerseries, default_thread_pool=self.thread_pool)
        self.task_save_single = SFT.WorkerTask("Save Image", self.save_single, default_thread_pool=self.thread_pool)
        self.powerseries_ActionParam.sigActivated.connect(lambda: self.task_powerseries.run_on_pool())
        self.save_single_ActionParam.sigActivated.connect(lambda: self.task_save_single.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.clear_background_ActionParam.sigActivated.connect(self.clear_background)

        self._interrupted = False
        self.active_power_adapter = None

    def connect(self):
        cam = self.camera.value()
        cam.most_recent_frame.sigValueChanged.connect(self._on_new_frame)
        cam.is_streaming.sigValueChanged.connect(self._on_streaming_changed)

    @QtCore.Slot()
    def start_live_view(self):
        self.camera.value().trigger_start_live_view()

    @QtCore.Slot()
    def stop_live_view(self):
        self.camera.value().trigger_stop_live_view()

    @QtCore.Slot()
    def interrupt(self):
        self._interrupted = True

    @QtCore.Slot()
    def _on_new_frame(self):
        self.live_frame.setValue(self.camera.value().most_recent_frame.value())

    @QtCore.Slot()
    def _on_streaming_changed(self):
        self.is_streaming.setValue(self.camera.value().is_streaming.value())

    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        n = int((self.ps_stop.value() - self.ps_start.value()) / self.ps_step.value()) + 1
        self.n_measurements.setValue(n)

    def get_background_subtracted(self, frame):
        """Subtract the loaded background from `frame`, for the live display and the
        single-image Save button. A powerseries never goes through this -- its saved
        frames are always the raw, un-subtracted camera data."""
        background = self.background_frame.value()
        if frame is None or background is None or np.shape(background) != np.shape(frame):
            return frame
        return np.clip(frame.astype(np.float64) - background, 0, None)

    @QtCore.Slot()
    def clear_background(self):
        self.background_frame.setValue(None)

    def load_background(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == '.png':
            image = self._read_background_png(path)
        elif ext == '.origin':
            image = self._read_background_origin(path)
        else:
            raise ValueError(f'Unsupported background file type: {ext}')
        self.background_frame.setValue(image)

    def _read_background_png(self, path):
        img = Image.open(path)
        # our own saved pngs embed the raw-count scale factor they were multiplied by
        # (see _save_png_frames) so the background can be un-scaled back to raw counts;
        # a png from elsewhere has no such metadata and is used as-is.
        scale = int(img.info.get('raw_scale', 1))
        return np.asarray(img).astype(np.float64) / scale

    def _read_background_origin(self, path):
        """Read the first pixel-array image out of a Powerseries_Fourier .origin file."""
        with open(path, encoding='latin-1') as fh:
            lines = [line.rstrip('\r\n') for line in fh]
        rows = []
        in_image = False
        for line in lines:
            if line.startswith('# Image'):
                if in_image:
                    break
                in_image = True
                continue
            if in_image:
                if line.strip() == '':
                    break
                rows.append([float(v) for v in line.split('\t')])
        if not rows:
            raise ValueError(f'No image data found in {path}.')
        return np.array(rows, dtype=np.float64)

    def save_single(self):
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._save_single()
        finally:
            if status is not None:
                status.resume()

    def _save_single(self):
        frame = self.live_frame.value()
        if frame is None:
            raise Exception('No image to save yet.')

        cam = self.camera.value()
        pm = self.powermeter.value()
        hwp = self.hwp.value()

        datetime_now = dt.datetime.now()
        temperature = 0  # to implement
        integration_time = cam.exposure_time.value() * 1e-3  # ms -> s

        pm.reading.trigger_read().wait(2.0)
        power = np.array([pm.reading.value()])

        angle_value = 0.0
        if hwp is not None:
            hwp.angle.trigger_read().wait(1.0)
            angle_value = hwp.angle.value()
        angle = np.array([angle_value])

        self._write_bgcorrected_and_raw(datetime_now, temperature, integration_time, power, angle, [frame])

    def powerseries(self):
        self._interrupted = False
        self.measurement_running.setValue(True)
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._powerseries()
        finally:
            if status is not None:
                status.resume()
            self.measurement_running.setValue(False)

    def _powerseries(self):
        if self.camera.value() is None:
            raise Exception('Camera not connected.')
        if self.powermeter.value() is None:
            raise Exception('Powermeter not connected.')

        start = self.ps_start.value()
        stop = self.ps_stop.value()
        step = self.ps_step.value()
        n = self.n_measurements.value()
        if n <= 0:
            return
        angles = start + np.arange(n) * step
        self.current_angles.setValue(angles)

        cam = self.camera.value()
        pm = self.powermeter.value()

        datetime = dt.datetime.now()
        temperature = 0  # to implement
        integration_time = cam.exposure_time.value() * 1e-3  # ms -> s

        self.active_power_adapter.set_setpoint(angles[0])

        data_power = np.empty(n)
        frames = [None] * n

        print("Number of Measurements:", n)

        for i in range(n):
            if self._interrupted:
                break
            self.active_power_adapter.set_setpoint(angles[i])
            self.current_power_index.setValue(i)
            pm.reading.trigger_read().wait(2.0)
            data_power[i] = pm.reading.value()
            self.powers.setValue(data_power)
            frames[i] = self._acquire_frame()
            self.live_frame.setValue(frames[i])

        valid = [i for i in range(n) if frames[i] is not None]
        if not valid:
            return

        pixel_arrays = [frames[i] for i in valid]
        excitation_power = data_power[valid]
        angles_used = angles[valid]

        self._write_bgcorrected_and_raw(
            datetime, temperature, integration_time, excitation_power, angles_used, pixel_arrays
        )

    def _acquire_frame(self):
        """Grab one fresh frame from the CMOS, starting live view if needed."""
        cam = self.camera.value()
        was_streaming = cam.is_streaming.value()
        if not was_streaming:
            cam.trigger_start_live_view()
        try:
            prev_timestamp = cam.most_recent_frame.actual_timestamp.value()
            timeout = cam.exposure_time.value() * 1e-3 + self.extra_timeout.value()
            deadline = time.monotonic() + timeout
            while True:
                timestamp = cam.most_recent_frame.actual_timestamp.value()
                if timestamp is not None and timestamp != prev_timestamp:
                    break
                if time.monotonic() > deadline:
                    raise Exception('Timed out waiting for a CMOS frame.')
                time.sleep(0.01)
            return cam.most_recent_frame.value().copy()
        finally:
            if not was_streaming:
                cam.trigger_stop_live_view()

    def _save_png_frames(self, origin_filepath, pixel_arrays, angles):
        # The CMOS ADC has fewer than 16 bits (e.g. 10-bit -> max count 1023), so raw counts
        # only fill a small fraction of a 16-bit PNG's range and render as near-black in
        # viewers that don't auto-stretch contrast. Scale by a fixed factor derived from the
        # sensor's actual bit depth so brightness is both visible and still comparable
        # linearly across power steps (unlike a per-image min/max normalization).
        bit_depth = getattr(self.camera.value(), 'bit_depth', 16)
        scale = (2 ** 16 - 1) // (2 ** bit_depth - 1) if bit_depth < 16 else 1

        base_dir = os.path.dirname(origin_filepath)
        base_name = os.path.splitext(os.path.basename(origin_filepath))[0]
        png_dir = os.path.join(base_dir, base_name)
        os.makedirs(png_dir, exist_ok=True)

        # embed the scale factor so a png loaded back in as a background can be
        # un-scaled to raw counts again (see _read_background_png)
        meta = PngInfo()
        meta.add_text("raw_scale", str(scale))

        for i, (frame, angle) in enumerate(zip(pixel_arrays, angles)):
            png_path = os.path.join(png_dir, f"{base_name}_{i:02d}_{angle:.2f}deg.png")
            scaled = np.clip(np.asarray(frame).astype(np.int64) * scale, 0, 65535).astype(np.uint16)
            Image.fromarray(scaled).save(png_path, pnginfo=meta)

    def _write_bgcorrected_and_raw(self, datetime_value, temperature, integration_time,
                                    excitation_power, angles, raw_pixel_arrays):
        """If a background is loaded (and matches the frame shape), writes two .origin
        files sharing the same file number:
        - the main file: background-subtracted and clamped to >= 0 (see
          get_background_subtracted), named with a "_bgcorrected" suffix, with pngs
          alongside it if "Save png" is enabled;
        - the same data before subtraction, in a "raw_pxl" subfolder, same base
          filename but without the suffix (no pngs -- just the raw pixel values).

        If no background is loaded (or its shape doesn't match), there is nothing to
        correct -- a single unsuffixed file is written directly in save_directory, as
        if background subtraction didn't exist.
        """
        background = self.background_frame.value()
        has_background = (
            background is not None
            and len(raw_pixel_arrays) > 0
            and np.shape(background) == np.shape(raw_pixel_arrays[0])
        )

        dir_ = self.save_directory.value()
        file = self.save_filename.value()
        filenumber = HelperFunctions().get_next_file_number(dir_)
        base = f"{filenumber}_{file}_{integration_time:.3f}s"

        if not has_background:
            path = f"{dir_}\\{base}.origin"
            HelperFunctions().write_fourier_powerseries_origin(
                datetime_value, temperature, integration_time, excitation_power, angles,
                raw_pixel_arrays, path
            )
            if self.save_png.value():
                self._save_png_frames(path, raw_pixel_arrays, angles)
            return

        corrected_arrays = [self.get_background_subtracted(frame) for frame in raw_pixel_arrays]

        corrected_path = f"{dir_}\\{base}_bgcorrected.origin"
        HelperFunctions().write_fourier_powerseries_origin(
            datetime_value, temperature, integration_time, excitation_power, angles,
            corrected_arrays, corrected_path
        )
        if self.save_png.value():
            self._save_png_frames(corrected_path, corrected_arrays, angles)

        raw_dir = os.path.join(dir_, "raw_pxl")
        os.makedirs(raw_dir, exist_ok=True)
        raw_path = os.path.join(raw_dir, f"{base}.origin")
        HelperFunctions().write_fourier_powerseries_origin(
            datetime_value, temperature, integration_time, excitation_power, angles,
            raw_pixel_arrays, raw_path
        )

    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
