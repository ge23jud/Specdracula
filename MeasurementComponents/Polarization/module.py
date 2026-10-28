from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from ScopeFoundry import Module
from helperfunctions import HelperFunctions
import os


class PolarizationModule(Module):
    """PL spectra as a function of the K10CR1 rotation stage angle.

    Mirrors the Photoluminescence powerseries, but the swept axis is the
    rotation stage (polarization analyzer) instead of the excitation HWP.
    Excitation power is read once per series and only stored in the header.
    """

    # devices
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    rotation_stage = SFT.ObjectParameter("Rotation Stage", SFT.TurboComponent)
    powermeter = SFT.ObjectParameter("Powermeter", SFT.TurboComponent)
    status = SFT.ObjectParameter("Status", SFT.TurboComponent)
    shutter = SFT.ObjectParameter("Shutter", SFT.TurboComponent)

    y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    x_label = SFT.ObjectParameter("X Label", dtype=str, value="Energy", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")
    ps_start = SFT.ObjectParameter("Rotation Start Angle", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°")
    ps_stop = SFT.ObjectParameter("Rotation Stop Angle", dtype=float, value=180.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°")
    ps_step = SFT.ObjectParameter("Rotation Step", dtype=float, value=10.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=19)
    current_angles = SFT.ObjectParameter("Current Sweep Angles", dtype=np.ndarray, value=None, readonly=True)
    current_angle_index = SFT.ObjectParameter("Current Angle Index", dtype=int, value=0, readonly=True)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    wavelength_nm = SFT.ObjectParameter('Wavelength', dtype=np.ndarray, unit='nm', value=None, readonly=True)
    energy_ev = SFT.ObjectParameter("Energy", dtype=np.ndarray, unit="eV", value=None, readonly=True)
    intensity_counts = SFT.ObjectParameter('Intensity (counts)', dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_series = SFT.ObjectParameter("Intensities for Polarization Series", dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_series_complete = SFT.ObjectParameter("Intensities for Polarization Series Complete Array", dtype=np.ndarray, value=None, readonly=True)
    measurement_running = SFT.ObjectParameter('Measurement Running', dtype=bool, value=False, readonly=True)
    total_measurement_steps = SFT.ObjectParameter('Total Measurement Steps', dtype=int, value=0, readonly=True)
    completed_measurement_steps = SFT.ObjectParameter('Completed Measurement Steps', dtype=int, value=0, readonly=True)
    repetitions = SFT.ObjectParameter('Repetitions', dtype=int, value=1, readonly=False)
    averaging = SFT.ObjectParameter('Averaging', dtype=bool, value=True, readonly=False)
    colorscheme = SFT.ObjectParameter(
        'Color Scheme', dtype=str, value='Viridis',
        range=SFT.ChoiceRangeType(**{'Viridis': 0, 'Spectral': 1, 'CoolWarm': 2, 'Warm': 3, 'Turbo': 4})
    )
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\\Measurements\\{dt.date.today().__str__().replace('-', '')}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")

    single_ActionParam = SFT.ActionParameter('Acquire Single')
    save_single_ActionParam = SFT.ActionParameter("Save Polarization Snapshot")
    continuous_ActionParam = SFT.ActionParameter('Acquire Continuous')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt Acquire')
    series_ActionParam = SFT.ActionParameter("Run Polarization Series")


    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.ps_start.sigValueChanged.connect(self._on_input_update_nmeasurements_value)
        self.ps_stop.sigValueChanged.connect(self._on_input_update_nmeasurements_value)
        self.ps_step.sigValueChanged.connect(self._on_input_update_nmeasurements_value)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        self.task_single = SFT.WorkerTask("Acquire single", self.acquire_single, default_thread_pool=self.thread_pool)
        self.task_save_single = SFT.WorkerTask("Save Polarization Snapshot", self.save_single, default_thread_pool=self.thread_pool)
        self.task_continuous = SFT.WorkerTask("Acquire continuous", self.acquire_continuous, default_thread_pool=self.thread_pool)
        self.task_series = SFT.WorkerTask("Run Polarization Series", self.polarization_series, default_thread_pool=self.thread_pool)

        self.single_ActionParam.sigActivated.connect(lambda: self.task_single.run_on_pool())
        self.save_single_ActionParam.sigActivated.connect(lambda: self.task_save_single.run_on_pool())
        self.continuous_ActionParam.sigActivated.connect(lambda: self.task_continuous.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.series_ActionParam.sigActivated.connect(lambda: self.task_series.run_on_pool())
        self._interrupted = False

        self.wavelength_nm.sigValueChanged.connect(self._update_energy_array)
        self.spectrograph.sigValueChanged.connect(self._on_spectrograph_set)


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


    def save_single(self):
        """Save the currently displayed spectrum, tagged with the current stage angle."""
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._save_single()
        finally:
            if status is not None:
                status.resume()

    def _save_single(self):
        stage = self._get_rotation_stage()
        stage.angle.trigger_read().wait(1.0)
        angle = stage.angle.value()

        intensity = self.intensity_counts.value()
        if intensity is None:
            raise Exception('No spectrum acquired yet.')
        self._write_file(np.array([angle]), np.atleast_2d(intensity).T, self._read_power_mW())


    def is_shutter_open(self):
        """Live hardware read of the excitation shutter state (see PhotoluminescenceModule)."""
        shutter = self.shutter.value()
        if shutter is None:
            return True
        return bool(shutter.device.get_shutter_state(shutter.shutter_id.value()))


    def _get_rotation_stage(self):
        stage = self.rotation_stage.value()
        if stage is None or stage.device is None:
            raise Exception('K10CR1 rotation stage not connected.')
        return stage


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


    def polarization_series(self):
        self._interrupted = False
        self.measurement_running.setValue(True)
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._polarization_series()
        finally:
            if status is not None:
                status.resume()
            self.measurement_running.setValue(False)

    def _polarization_series(self):
        stage = self._get_rotation_stage()
        spec = self.spectrograph.value()

        n = self.n_measurements.value()
        if n <= 0:
            return
        angles = self.ps_start.value() + np.arange(n) * self.ps_step.value()
        self.current_angles.setValue(angles)
        self.completed_measurement_steps.setValue(0)
        self.total_measurement_steps.setValue(n)

        # Excitation power is constant over the series (only the analyzer
        # rotates), so it is read once and only written to the header.
        power = self._read_power_mW()

        no_pixels = spec.detector_pixels.value()
        data = np.empty((n, no_pixels))
        self.intensity_counts_series_complete.setValue(data)
        n_done = 0
        print("Number of Measurements:", n)

        for i in range(n):
            if self._interrupted:
                break
            stage.write_angle(angles[i])  # blocks until the stage has stopped
            self.current_angle_index.setValue(i)
            self._acquire(self.intensity_counts_series, self.wavelength_nm, self.averaging.value(), False)
            data[i, :] = self.intensity_counts_series.value().flatten()
            n_done = i + 1
            self.intensity_counts_series_complete.setValue(data)
            self.completed_measurement_steps.setValue(n_done)

        if n_done == 0:
            return
        # On interrupt, save only the angles actually measured.
        self._write_file(angles[:n_done], data[:n_done].T, power)


    def _write_file(self, angles, intensity, power_mW):
        cam = self.camera.value()
        spec = self.spectrograph.value()

        integration_time = cam.exposure.value()
        center_wavelength = spec.center_wavelength.value() * 1e9
        center_energy = HelperFunctions().wavelength_energy_converter(center_wavelength)
        entrance_slit_width = spec.entrance_slit_direct.value() * 1e3  # convert to mm
        wavelength = self.wavelength_nm.value()
        dispersion_window = wavelength[-1] - wavelength[0]
        filepath = self.update_save_string(integration_time, center_energy)

        HelperFunctions().write_polarization_origin(
            dt.datetime.now(), 0, integration_time, power_mW, center_wavelength, dispersion_window,
            entrance_slit_width, 0, wavelength, angles, intensity, filepath
        )


    @QtCore.Slot()
    def _on_input_update_nmeasurements_value(self):
        step = self.ps_step.value()
        if step <= 0:
            return
        n = int((self.ps_stop.value() - self.ps_start.value()) / step) + 1
        self.n_measurements.setValue(max(n, 1))


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


    def update_save_string(self, integration_time, center_energy):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        filenumber = HelperFunctions().get_next_file_number(dir)
        return f"{dir}\\{filenumber}_{file}_pol_{integration_time:.3f}s_{center_energy:.3f}eV.origin"

    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
