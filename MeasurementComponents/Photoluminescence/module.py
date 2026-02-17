from PySide6 import QtCore
import numpy as np
import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter


class PhotoluminescenceModule(Module):

    # devices
    camera = SFT.ObjectParameter('Camera', SFT.TurboComponent)
    spectrograph = SFT.ObjectParameter('Spectrograph', SFT.TurboComponent)
    hwp = SFT.ObjectParameter("HWP", SFT.TurboComponent)

    y_scale = SFT.ObjectParameter("Y scale", dtype=str, value="Linear", range=SFT.ChoiceRangeType(**{"Linear": 0, "Logarithmic": 1}), doc="Y-axis scale type")
    x_label = SFT.ObjectParameter("X Label", dtype=str, value="Energy", range=SFT.ChoiceRangeType(**{"Energy": 0, "Wavelength": 1}), doc="X-label")
    ps_start = SFT.ObjectParameter("Power HWP Start Position", dtype=float, value=0.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0, decimals=2), unit="°" )
    ps_stop = SFT.ObjectParameter("Power HWP Stop Position", dtype=float, value=45.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    ps_step = SFT.ObjectParameter("Power HWP Step", dtype=float, value=1.0, range=SFT.MinMaxRangeType(min=0.0, max=360.0), unit="°")
    n_measurements = SFT.ObjectParameter("N Measurements", dtype=int, value=0)




    extra_timeout = SFT.ObjectParameter('Acquisition timeout', dtype=float, unit='s', value=3.0)
    wavelength_nm = SFT.ObjectParameter('Wavelength', dtype=np.ndarray, unit='nm', value=None, readonly=True)
    intensity_counts = SFT.ObjectParameter('Intensity (counts)', dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_powerseries = SFT.ObjectParameter("Intensities for Powerseries", dtype=np.ndarray, value=None, readonly=True)
    intensity_counts_powerseries_complete = SFT.ObjectParameter("Intensities for Powerseries Complete Array", dtype=np.ndarray, value=None, readonly=True)
    repetitions = SFT.ObjectParameter('Repetitions', dtype=int, value=1, readonly=False)
    averaging = SFT.ObjectParameter('Averaging', dtype=bool, value=True, readonly=False)

    single_ActionParam = SFT.ActionParameter('Acquire Single')
    continuous_ActionParam = SFT.ActionParameter('Acquire Continuous')
    interrupt_ActionParam = SFT.ActionParameter('Interrupt Acquire')
    powerseries_ActionParam = SFT.ActionParameter("Run Powerseries")




    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
   
        self.ps_start.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_stop.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)
        self.ps_step.sigValueChanged.connect(self._on_ps_input_update_nmeasurements_value)

        '''Connect action parameters to ui buttons'''
        self.task_single = SFT.WorkerTask("Acquire single", self.acquire_single, default_thread_pool=self.thread_pool)
        self.task_continuous = SFT.WorkerTask("Acquire continuous", self.acquire_continuous, default_thread_pool=self.thread_pool)
        self.task_powerseries = SFT.WorkerTask("Run Powerseries", self.powerseries, default_thread_pool=self.thread_pool)

        self.single_ActionParam.sigActivated.connect(lambda: self.task_single.run_on_pool())
        self.continuous_ActionParam.sigActivated.connect(lambda: self.task_continuous.run_on_pool())
        self.interrupt_ActionParam.sigActivated.connect(self.interrupt)
        self.powerseries_ActionParam.sigActivated.connect(lambda: self.task_powerseries.run_on_pool())
        self._interrupted = False
        #self.file_exporters["HDF files (*.h5)"] = AndorCCDReadoutMeasure.to_hdf


    def acquire_single(self):
        """Acquire a signal spectrum."""
        self._acquire(
            intensity_buffer=self.intensity_counts,
            wavelength_buffer=self.wavelength_nm,
            averaging=self.averaging.value(),
            repetitions=self.repetitions.value()
        )
        self._interrupted = False


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
        elif not self.spectrograph.value().connected.value():
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
        elif self.camera.value().connected.value() == False:
            raise Exception('Camera not connected.')
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
        print("Number of Measurements:", self.n_measurements.value())
        for i in range(self.n_measurements.value()):    

            hwp.write_angle(start + i*step)
            #print("angle:", start+i*step)
            self._acquire(self.intensity_counts_powerseries, self.wavelength_nm, self.averaging.value(), False)
            data[i, :] = self.intensity_counts_powerseries.value().flatten()
            self.intensity_counts_powerseries_complete.setValue(data)



    @QtCore.Slot()
    def _on_ps_input_update_nmeasurements_value(self):
        n = int((self.ps_stop.value()-self.ps_start.value())/self.ps_step.value()) + 1
        self.n_measurements.setValue(n)
        
