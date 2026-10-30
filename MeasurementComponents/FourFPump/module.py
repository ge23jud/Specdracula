from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from time import sleep
from ScopeFoundry import Module
from helperfunctions import HelperFunctions
import os


class FourFPumpModule(Module):
    """PL spectra as a function of the 4F-pump motorized mirror position.

    The Picomotor mirror (Newport 8742) is scanned on a grid centred on its
    current position: X and Y each run from -range to +range in steps of
    `step` (all in Picomotor steps). A full spectrum is taken at every point.

    The scan is a serpentine: rows run alternately -X -> +X and +X -> -X, so
    no time is spent on flyback moves. Picomotors are open loop and their step
    size depends on direction, so odd rows may be shifted slightly in X
    relative to even rows. After the scan the mirror is moved back to the
    centre; due to the same open-loop hysteresis this return is only approximate.

    The map shows, per point, the maximum counts within the spectral window
    [Window Min, Window Max] (nm). If Window Max <= Window Min the whole
    spectrum is used.

    Excitation power is read once per scan and only stored in the header.
    """

    # devices
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    mirror = SFT.ObjectParameter('Motorized Mirror', SFT.TurboComponent)
    powermeter = SFT.ObjectParameter("Powermeter", SFT.TurboComponent)
    status = SFT.ObjectParameter("Status", SFT.TurboComponent)
    shutter = SFT.ObjectParameter("Shutter", SFT.TurboComponent)

    y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    x_label = SFT.ObjectParameter("X Label", dtype=str, value="Energy", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")

    x_range = SFT.ObjectParameter("X Range", dtype=int, value=500, unit="steps",
                                  range=SFT.MinMaxRangeType(min=0, max=100000, decimals=0),
                                  doc="Scan X from -range to +range around the current mirror position")
    x_step = SFT.ObjectParameter("X Step", dtype=int, value=100, unit="steps",
                                 range=SFT.MinMaxRangeType(min=1, max=100000, decimals=0))
    y_range = SFT.ObjectParameter("Y Range", dtype=int, value=500, unit="steps",
                                  range=SFT.MinMaxRangeType(min=0, max=100000, decimals=0),
                                  doc="Scan Y from -range to +range around the current mirror position")
    y_step = SFT.ObjectParameter("Y Step", dtype=int, value=100, unit="steps",
                                 range=SFT.MinMaxRangeType(min=1, max=100000, decimals=0))
    settle_time = SFT.ObjectParameter("Settle Time", dtype=float, value=0.1, unit="s",
                                      range=SFT.MinMaxRangeType(min=0.0, max=60.0, decimals=3),
                                      doc="Wait after each mirror move before acquiring")
    return_to_center = SFT.ObjectParameter("Return To Center", dtype=bool, value=True)
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0, readonly=True)

    x_offsets = SFT.ObjectParameter("X Offsets", dtype=np.ndarray, value=None, readonly=True)
    y_offsets = SFT.ObjectParameter("Y Offsets", dtype=np.ndarray, value=None, readonly=True)
    current_x_index = SFT.ObjectParameter("Current X Index", dtype=int, value=0, readonly=True)
    current_y_index = SFT.ObjectParameter("Current Y Index", dtype=int, value=0, readonly=True)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    wavelength_nm = SFT.ObjectParameter('Wavelength', dtype=np.ndarray, unit='nm', value=None, readonly=True)
    energy_ev = SFT.ObjectParameter("Energy", dtype=np.ndarray, unit="eV", value=None, readonly=True)
    intensity_counts = SFT.ObjectParameter('Intensity (counts)', dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_series = SFT.ObjectParameter("Intensities for 4F-Pump Scan", dtype=np.ndarray, value=None, readonly=True)
    spectra_grid = SFT.ObjectParameter("4F-Pump Spectra Grid", dtype=np.ndarray, value=None, readonly=True,
                                       doc="Shape (nx, ny, pixels); NaN where not measured yet")
    window_min_nm = SFT.ObjectParameter("Window Min", dtype=float, value=0.0, unit="nm",
                                        range=SFT.MinMaxRangeType(min=0.0, max=10000.0, decimals=2),
                                        doc="Lower wavelength bound of the spectral window used for the map")
    window_max_nm = SFT.ObjectParameter("Window Max", dtype=float, value=0.0, unit="nm",
                                        range=SFT.MinMaxRangeType(min=0.0, max=10000.0, decimals=2),
                                        doc="Upper wavelength bound of the spectral window used for the map")
    map_data = SFT.ObjectParameter("Window Max Intensity Map", dtype=np.ndarray, value=None, readonly=True,
                                   doc="Shape (nx, ny): max counts within the spectral window per point; NaN where not measured yet")
    measurement_running = SFT.ObjectParameter('Measurement Running', dtype=bool, value=False, readonly=True)
    total_measurement_steps = SFT.ObjectParameter('Total Measurement Steps', dtype=int, value=0, readonly=True)
    completed_measurement_steps = SFT.ObjectParameter('Completed Measurement Steps', dtype=int, value=0, readonly=True)
    repetitions = SFT.ObjectParameter('Repetitions', dtype=int, value=1, readonly=False)
    averaging = SFT.ObjectParameter('Averaging', dtype=bool, value=True, readonly=False)
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\\Measurements\\{dt.date.today().__str__().replace('-', '')}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")

    single_ActionParam = SFT.ActionParameter('Acquire Single')
    continuous_ActionParam = SFT.ActionParameter('Acquire Continuous')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt Acquire')
    scan_ActionParam = SFT.ActionParameter("Run 4F-Pump Scan")


    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.x_range.sigValueChanged.connect(self.update_no_measurements)
        self.x_step.sigValueChanged.connect(self.update_no_measurements)
        self.y_range.sigValueChanged.connect(self.update_no_measurements)
        self.y_step.sigValueChanged.connect(self.update_no_measurements)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        self.task_single = SFT.WorkerTask("Acquire single", self.acquire_single, default_thread_pool=self.thread_pool)
        self.task_continuous = SFT.WorkerTask("Acquire continuous", self.acquire_continuous, default_thread_pool=self.thread_pool)
        self.task_scan = SFT.WorkerTask("Run 4F-Pump Scan", self.fourf_scan, default_thread_pool=self.thread_pool)

        self.single_ActionParam.sigActivated.connect(lambda: self.task_single.run_on_pool())
        self.continuous_ActionParam.sigActivated.connect(lambda: self.task_continuous.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.scan_ActionParam.sigActivated.connect(lambda: self.task_scan.run_on_pool())
        self._interrupted = False

        self.wavelength_nm.sigValueChanged.connect(self._update_energy_array)
        self.spectrograph.sigValueChanged.connect(self._on_spectrograph_set)
        self.window_min_nm.sigValueChanged.connect(self._recompute_map)
        self.window_max_nm.sigValueChanged.connect(self._recompute_map)

        self.update_no_measurements()


    @staticmethod
    def _offsets(half_range, step):
        """Grid offsets -half_range, -half_range + step, ... <= +half_range."""
        n = int(2 * half_range // step) + 1
        return -half_range + np.arange(n, dtype=int) * step

    @QtCore.Slot()
    def update_no_measurements(self):
        if self.x_step.value() <= 0 or self.y_step.value() <= 0:
            return
        nx = len(self._offsets(self.x_range.value(), self.x_step.value()))
        ny = len(self._offsets(self.y_range.value(), self.y_step.value()))
        self.n_measurements.setValue(nx * ny)


    def acquire_single(self):
        """Acquire a single spectrum."""
        self._acquire(
            intensity_buffer=self.intensity_counts,
            wavelength_buffer=self.wavelength_nm,
            averaging=self.averaging.value(),
            repetitions=self.repetitions.value()
        )
        self._interrupted = False


    def acquire_continuous(self):
        """Acquire spectra continuously until interrupted."""
        self._acquire(
            intensity_buffer=self.intensity_counts,
            wavelength_buffer=self.wavelength_nm,
            averaging=self.averaging.value(),
            continuous=True,
            repetitions=self.repetitions.value()
        )
        self._interrupted = False


    @QtCore.Slot()
    def interrupt(self):
        self._interrupted = True


    def is_shutter_open(self):
        """Live hardware read of the excitation shutter state (see PhotoluminescenceModule)."""
        shutter = self.shutter.value()
        if shutter is None:
            return True
        return bool(shutter.device.get_shutter_state(shutter.shutter_id.value()))


    def _window_mask(self, no_pixels):
        """Boolean pixel mask of the spectral window; all pixels if the window is unset."""
        wavelengths = self.wavelength_nm.value()
        lo, hi = self.window_min_nm.value(), self.window_max_nm.value()
        if hi <= lo or wavelengths is None or len(wavelengths) != no_pixels:
            return np.ones(no_pixels, dtype=bool)
        return (wavelengths >= lo) & (wavelengths <= hi)

    def _window_max_map(self, grid):
        """Max counts within the spectral window for every grid point; NaN where not measured."""
        window = grid[:, :, self._window_mask(grid.shape[2])]
        result = np.full(grid.shape[:2], np.nan)
        measured = np.isfinite(window).any(axis=2)
        if window.shape[2] > 0 and measured.any():
            result[measured] = np.nanmax(window[measured], axis=1)
        return result

    @QtCore.Slot()
    def _recompute_map(self):
        grid = self.spectra_grid.value()
        if grid is not None:
            self.map_data.setValue(self._window_max_map(grid))


    def _get_mirror(self):
        mirror = self.mirror.value()
        if mirror is None or mirror.device is None:
            raise Exception('Motorized mirror (Picomotor 8742) not connected.')
        return mirror


    def _move_mirror(self, mirror, x, y):
        """Move the mirror to absolute step positions (x, y); blocks until stopped."""
        for which, target, position in (('h', x, mirror.position_h), ('v', y, mirror.position_v)):
            mirror.write_position(which, int(target))
            position.setValue(mirror.read_position(which))
            position.target_value.setValue(int(target))


    def _read_power_mW(self):
        pm = self.powermeter.value()
        if pm is None:
            return 0.0
        pm.reading.trigger_read().wait(2.0)
        return pm.reading.value() * 1e3  # convert to mW


    def get_wavelength_calibration(self):
        if self.spectrograph.value() is None:
            raise Exception('Spectrograph not connected.')
        spec = self.spectrograph.value()
        task = spec.wavelength_calib.trigger_read()
        task.wait(timeout=3.0)
        if task.exception is not None:
            raise task.exception
        return np.array(task.result)


    def _acquire(self, intensity_buffer, wavelength_buffer=None, averaging=False, continuous=False, repetitions=1):
        """Acquire a spectrum or spectra, either single, multiple averaged or multiple saved individually.
        If wavelength_buffer is not passed, it will not be retrieved for speed.
        """
        if self.camera.value() is None:
            raise Exception('Camera not connected.')
        cam = self.camera.value()
        if wavelength_buffer is not None:
            try:
                x_data = self.get_wavelength_calibration()
            except Exception:
                self.log.error('Wavelength calibration unavailable.')
                x_data = np.arange(512)
            wavelength_buffer.setValue(x_data)
        assert repetitions >= 0, "Number of repetitions must be non-negative."

        def _inner():
            counts_list = None  # for multiexposure mode
            counts = None  # for averaging mode
            for rep in range(repetitions):
                wait_task = cam.trigger_acquisition()  # triggers the acquisition AND requests acquire_wait internally
                wait_time = cam.acc_cycle_time.value() + self.extra_timeout.value()
                wait_task.wait(wait_time)
                new_counts = cam.acquire_wait.result[0].copy()
                if new_counts is None:
                    raise Exception('camera returned no counts yet. you need to wait for acquisition')
                if averaging:
                    if counts is None:
                        counts = new_counts
                    else:
                        counts = (rep * counts + new_counts) / (rep + 1.0)
                    counts_list = counts
                else:
                    if counts_list is None:
                        counts_list = new_counts
                    else:
                        counts_list = np.append(counts_list, new_counts, axis=0)
                intensity_buffer.setValue(counts_list)
                if self._interrupted:
                    break

        if continuous:
            while not self._interrupted:
                _inner()
        else:
            _inner()


    def fourf_scan(self):
        self._interrupted = False
        self.measurement_running.setValue(True)
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._fourf_scan()
        finally:
            if status is not None:
                status.resume()
            self.measurement_running.setValue(False)

    def _fourf_scan(self):
        mirror = self._get_mirror()
        spec = self.spectrograph.value()

        x_offsets = self._offsets(self.x_range.value(), self.x_step.value())
        y_offsets = self._offsets(self.y_range.value(), self.y_step.value())
        nx, ny = len(x_offsets), len(y_offsets)
        n = nx * ny

        center_x = mirror.read_position('h')
        center_y = mirror.read_position('v')

        self.x_offsets.setValue(x_offsets)
        self.y_offsets.setValue(y_offsets)
        self.completed_measurement_steps.setValue(0)
        self.total_measurement_steps.setValue(n)

        # Excitation power is constant over the scan (only the mirror moves),
        # so it is read once and only written to the header.
        power = self._read_power_mW()

        no_pixels = spec.detector_pixels.value()
        grid = np.full((nx, ny, no_pixels), np.nan)
        self.spectra_grid.setValue(grid.copy())
        self.map_data.setValue(np.full((nx, ny), np.nan))

        measured = []  # (ix, iy) in acquisition order, for the file columns
        try:
            for iy, dy in enumerate(y_offsets):
                if self._interrupted:
                    break
                # serpentine: odd rows run from +X back to -X
                x_order = range(nx) if iy % 2 == 0 else range(nx - 1, -1, -1)
                for ix in x_order:
                    dx = x_offsets[ix]
                    if self._interrupted:
                        break
                    self._move_mirror(mirror, center_x + dx, center_y + dy)
                    sleep(self.settle_time.value())
                    self.current_x_index.setValue(ix)
                    self.current_y_index.setValue(iy)
                    self._acquire(self.intensity_counts_series, self.wavelength_nm, self.averaging.value(), False,
                                  self.repetitions.value())
                    spectrum = self.intensity_counts_series.value()
                    if spectrum.ndim > 1:
                        # averaging off: keep the mean of the repetitions
                        spectrum = spectrum.reshape(-1, no_pixels).mean(axis=0)
                    spectrum = spectrum.flatten()
                    grid[ix, iy, :] = spectrum
                    measured.append((ix, iy))
                    self.spectra_grid.setValue(grid.copy())
                    self.map_data.setValue(self._window_max_map(grid))
                    self.completed_measurement_steps.setValue(len(measured))
        finally:
            if self.return_to_center.value():
                try:
                    self._move_mirror(mirror, center_x, center_y)
                except Exception as e:
                    self.log.error(f'Could not return mirror to scan centre: {e}')

        if not measured:
            return
        # On interrupt, save only the points actually measured.
        ix_list = [ix for ix, _ in measured]
        iy_list = [iy for _, iy in measured]
        intensity = np.stack([grid[ix, iy, :] for ix, iy in measured], axis=1)
        self._write_file(x_offsets[ix_list], y_offsets[iy_list], intensity, power)


    def _write_file(self, x_positions, y_positions, intensity, power_mW):
        cam = self.camera.value()
        spec = self.spectrograph.value()

        integration_time = cam.exposure.value()
        center_wavelength = spec.center_wavelength.value() * 1e9
        center_energy = HelperFunctions().wavelength_energy_converter(center_wavelength)
        entrance_slit_width = spec.entrance_slit_direct.value() * 1e3  # convert to mm
        wavelength = self.wavelength_nm.value()
        dispersion_window = wavelength[-1] - wavelength[0]
        filepath = self.update_save_string(integration_time, center_energy)

        HelperFunctions().write_4fpump_origin(
            dt.datetime.now(), 0, integration_time, power_mW, center_wavelength, dispersion_window,
            entrance_slit_width, 0, wavelength, x_positions, y_positions, intensity, filepath
        )


    @QtCore.Slot()
    def _on_spectrograph_set(self):
        spec = self.spectrograph.value()
        if spec is not None:
            spec.wavelength_calib.sigValueChanged.connect(self._on_wavelength_calib_changed)

    @QtCore.Slot()
    def _on_wavelength_calib_changed(self):
        spec = self.spectrograph.value()
        if spec is None:
            return
        calib = spec.wavelength_calib.value()
        if calib is not None:
            self.wavelength_nm.setValue(np.array(calib))

    @QtCore.Slot()
    def _update_energy_array(self):
        wavelengths = self.wavelength_nm.value()
        energies = HelperFunctions().wavelength_energy_converter(wavelengths)
        self.energy_ev.setValue(energies)
        # default the map window to the full spectrum once a calibration is known
        if self.window_max_nm.value() <= self.window_min_nm.value():
            self.window_min_nm.setValue(float(np.min(wavelengths)))
            self.window_max_nm.setValue(float(np.max(wavelengths)))


    def update_save_string(self, integration_time, center_energy):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        filenumber = HelperFunctions().get_next_file_number(dir)
        return f"{dir}\\{filenumber}_{file}_4fpump_{integration_time:.3f}s_{center_energy:.3f}eV.origin"

    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
