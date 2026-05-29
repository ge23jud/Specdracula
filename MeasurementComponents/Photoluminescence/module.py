from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
import datetime as dt
from ScopeFoundry import Module, ObjectParameter
from helperfunctions import HelperFunctions
import os


class PhotoluminescenceModule(Module):

    # devices
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    hwp = SFT.ObjectParameter("HWP", SFT.TurboComponent)
    powermeter = SFT.ObjectParameter("Powermeter", SFT.TurboComponent)
    status = SFT.ObjectParameter("Status", SFT.TurboComponent)

    y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    x_label = SFT.ObjectParameter("X Label", dtype=str, value="Wavelength", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")
    ps_start = SFT.ObjectParameter("Power HWP Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°" )
    ps_stop = SFT.ObjectParameter("Power HWP Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    ps_step = SFT.ObjectParameter("Power HWP Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)
    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    wavelength_nm = SFT.ObjectParameter('Wavelength', dtype=np.ndarray, unit='nm', value=None, readonly=True)
    energy_ev = SFT.ObjectParameter("Energy", dtype=np.ndarray, unit="eV", value=None, readonly=True)
    intensity_counts = SFT.ObjectParameter('Intensity (counts)', dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_powerseries = SFT.ObjectParameter("Intensities for Powerseries", dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_powerseries_complete = SFT.ObjectParameter("Intensities for Powerseries Complete Array", dtype=np.ndarray, value=None, readonly=True)
    powers = SFT.ObjectParameter("Powers", dtype=np.ndarray, value=None)
    repetitions = SFT.ObjectParameter('Repetitions', dtype=int, value=1, readonly=False)
    averaging = SFT.ObjectParameter('Averaging', dtype=bool, value=True, readonly=False)
    pixel_correction_enabled = SFT.ObjectParameter('Pixel Correction', dtype=bool, value=False)
    #integration_time = SFT.ObjectParameter()
    save_directory = SFT.ObjectParameter("Save Directory", dtype=str, value=f"C:\Measurements\{dt.date.today().__str__().replace("-", "")}")
    save_filename = SFT.ObjectParameter("Save Filename", dtype=str, value="")
    # save_string = SFT.ObjectParameter("Save String", dtype=str, value="", readonly=True) 

    single_ActionParam = SFT.ActionParameter('Acquire Single')
    save_single_ActionParam = SFT.ActionParameter("Save PL Snapshot")
    continuous_ActionParam = SFT.ActionParameter('Acquire Continuous')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt Acquire')
    powerseries_ActionParam = SFT.ActionParameter("Run Powerseries")



    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        _corr_path = os.path.join(os.path.dirname(__file__), 'pixel_correction_2.txt')
        self._pixel_correction = np.loadtxt(_corr_path)[::-1]  # file is energy order; reverse for wavelength/pixel order

        self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.save_directory.sigValueChanged.connect(self.check_dir_exists)

        '''Connect action parameters to ui buttons'''
        self.task_single = SFT.WorkerTask("Acquire single", self.acquire_single, default_thread_pool=self.thread_pool)
        self.task_save_single = SFT.WorkerTask("Save PL Snapshot", self.save_single, default_thread_pool=self.thread_pool)
        self.task_continuous = SFT.WorkerTask("Acquire continuous", self.acquire_continuous, default_thread_pool=self.thread_pool)
        self.task_powerseries = SFT.WorkerTask("Run Powerseries", self.powerseries, default_thread_pool=self.thread_pool)

        self.single_ActionParam.sigActivated.connect(lambda: self.task_single.run_on_pool())
        self.save_single_ActionParam.sigActivated.connect(lambda: self.task_save_single.run_on_pool())
        self.continuous_ActionParam.sigActivated.connect(lambda: self.task_continuous.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.powerseries_ActionParam.sigActivated.connect(lambda: self.task_powerseries.run_on_pool())
        self._interrupted = False
        #self.file_exporters["HDF files (*.h5)"] = AndorCCDReadoutMeasure.to_hdf

        self.wavelength_nm.sigValueChanged.connect(self._update_energy_array)
        self.spectrograph.sigValueChanged.connect(self._on_spectrograph_set)


    def acquire_single(self):
        """Acquire a signal spectrum."""
        self._acquire(
            intensity_buffer=self.intensity_counts,
            wavelength_buffer=self.wavelength_nm,
            averaging=self.averaging.value(),
            repetitions=self.repetitions.value()
        )
        self._interrupted = False

    
    def save_single(self):
        """Save currently displayed PL Snapshot"""
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._save_single()
        finally:
            if status is not None:
                status.resume()

    def _save_single(self):
        cam = self.camera.value()
        spec = self.spectrograph.value()
        pm = self.powermeter.value()

        datetime = dt.datetime.now()
        temperature = 0 # to implement
        integration_time = cam.exposure.value()
        pm.reading.trigger_read()
        power = pm.reading.value() * 1e3 # convert to mW
        center_wavelength = spec.center_wavelength.value() * 1e9
        entrance_slit_width = spec.entrance_slit_direct.value() * 1e3 # convert to mm
        exit_slit_width = 0
        excitation_power = np.zeros(1)
        filepath = self.update_save_string()

        intensity = self.intensity_counts.value().T
        wavelength = self.wavelength_nm.value()
        dispersion_window = wavelength[-1] - wavelength[0]

        HelperFunctions().write_origin(datetime, "Powerseries", temperature, integration_time, power, center_wavelength, dispersion_window,
                                       entrance_slit_width, exit_slit_width, wavelength, excitation_power, np.zeros(1), intensity, filepath)


    def acquire_continuous(self):
        """Acquire a continuous spectrum.
        """
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


    def get_wavelength_calibration(self):
        # First collect the WL if required:
        if self.spectrograph.value() is None:
            raise Exception('Spectrograph not connected.')
        # elif not self.spectrograph.value().connected.value():
        #     raise Exception('Spectrograph not connected.')
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
        # elif self.camera.value().connected.value() == False:
        #     raise Exception('Camera not connected.')
        cam = self.camera.value()
        if wavelength_buffer is not None:
            try:
                x_data = self.get_wavelength_calibration()
            except Exception as e:
                self.log.error(f'Wavelength calibration unavailable.')
                x_data = np.arange(512)
            wavelength_buffer.setValue(x_data)
        assert repetitions >= 0, "Number of repetitions must be non-negative."

        def _inner():
            counts_list = None  # for multiexposure mode
            counts = None  # for averaging mode
            current_progress = 0.0
            progress_step = 100.0 / repetitions
            # self.accumulation_progress.setValue(current_progress)
            for rep in range(repetitions):
                # will work even if repetitions = 0 (then sets intensity buffer to 0)
                wait_task = cam.trigger_acquisition()  # this triggers the acquisition AND requests acquire_wait internally
                wait_time = cam.acc_cycle_time.value() + self.extra_timeout.value()
                wait_task.wait(wait_time)
                # waits in measure thread for AndorCCD stuff
                new_counts = cam.acquire_wait.result[0].copy()
                if new_counts is None:
                    raise Exception('camera returned no counts yet. you need to wait for acquisition')
                if self.pixel_correction_enabled.value():
                    new_counts = new_counts / self._pixel_correction
                if averaging:
                    if counts is None:
                        # first iteration
                        counts = new_counts
                    else:
                        counts = (rep * counts + new_counts) / (rep + 1.0)
                    counts_list = counts
                else:
                    if counts_list is None:
                        # first iteration
                        counts_list = new_counts
                    else:
                        counts_list = np.append(counts_list, new_counts, axis=0)
                # update data after every spectrum so the plot can be updated
                # temp_counts = np.vstack(counts_list)
                intensity_buffer.setValue(counts_list)
                # update the progress bar
                current_progress = current_progress + progress_step
                # self.accumulation_progress.setValue(current_progress)
                if self._interrupted:
                    break
            # self.accumulation_progress.setValue(100.0)

        if continuous:
            while not self._interrupted:
                _inner()
        else:
            _inner()



    def powerseries(self):
        status = self.status.value()
        if status is not None:
            status.pause()
        try:
            self._powerseries()
        finally:
            if status is not None:
                status.resume()

    def _powerseries(self):
        start = self.ps_start.value()
        stop = self.ps_stop.value()
        step = self.ps_step.value()
        hwp = self.hwp.value()
        spec = self.spectrograph.value()
        
        hwp.write_angle(start)

        no_pixels = spec.detector_pixels.value()
        n = self.n_measurements.value()
        data = np.empty((n, no_pixels))
        self.intensity_counts_powerseries_complete.setValue(data)
        data_power = np.empty(n)
        data_angle = np.empty(n)
        print("Number of Measurements:", self.n_measurements.value())


        cam = self.camera.value()
        spec = self.spectrograph.value()
        pm = self.powermeter.value()

        datetime = dt.datetime.now()
        temperature = 0 # to implement
        integration_time = cam.exposure.value()
        center_wavelength = spec.center_wavelength.value() * 1e9
        entrance_slit_width = spec.entrance_slit_direct.value() * 1e3 # convert to mm
        exit_slit_width = 0
        filepath = self.update_save_string()


        for i in range(self.n_measurements.value()):    

            hwp.write_angle(start + i*step)
            data_angle[i] = start + i*step
            self._acquire(self.intensity_counts_powerseries, self.wavelength_nm, self.averaging.value(), False)
            pm.reading.trigger_read()
            power = pm.reading.value()
            data_power[i] = power
            self.powers.setValue(data_power)
            data[i, :] = self.intensity_counts_powerseries.value().flatten()
            self.intensity_counts_powerseries_complete.setValue(data)

        intensity = self.intensity_counts_powerseries_complete.value().T
        wavelength = self.wavelength_nm.value()
        dispersion_window = wavelength[-1] - wavelength[0]
        excitation_power = self.powers.value()
        power = excitation_power[0]

        HelperFunctions().write_origin(datetime, "Powerseries", temperature, integration_time, power, center_wavelength, dispersion_window,
                                       entrance_slit_width, exit_slit_width, wavelength, excitation_power, data_angle, intensity, filepath)



    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        n = int((self.ps_stop.value()-self.ps_start.value())/self.ps_step.value()) + 1
        self.n_measurements.setValue(n)


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


    def update_save_string(self):
        dir = self.save_directory.value()
        file = self.save_filename.value()
        
        helper = HelperFunctions()
        filenumber = helper.get_next_file_number(dir)

        new_save_string =  f"{dir}\\{filenumber}_{file}.origin"
        # self.save_string.setValue(new_save_string)
        return new_save_string
    
    def check_dir_exists(self):
        filepath = self.save_directory.value()
        if not os.path.isdir(filepath):
            os.makedirs(filepath)

        