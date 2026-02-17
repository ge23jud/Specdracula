'''
Created on May 6, 2014

@author: lab
'''
import logging
from datetime import datetime

import numpy as np
import win32event  # pip install pyWin32
from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import HardwareModule, PhysicalParameter, ActionParameter, WorkerTask

logger = logging.getLogger("AndorCCD")


class AndorCCDHW(HardwareModule):
    ccd_status = PhysicalParameter(
        name='CCD status',
        dtype=str,
        range=SFT.ChoiceRangeType(
            **{
                'Idle': 20073,
                'Acquiring': 20072,
                'Temperature cycle': 20074,
                'Accumulation time not met': 20023,
                'Error ack': 20013,
                'Acq buffer': 20018,
                'Spool error': 20026
            }))
    acquisition_progress = PhysicalParameter(
        name='Acquisition progress',
        dtype=tuple
    )
    exposure = PhysicalParameter(
        name="Exposure time",
        dtype=float,
        unit="s",
        range=SFT.MinMaxRangeType(min=0, max=86400, decimals=5)
    )
    acc_cycle_time = PhysicalParameter(
        name="Accumulation cycle time",
        dtype=float,
        unit="s",
        doc='Total readout time combining exposure, readout and an optional pause, in Accumulate readout mode.',
        range=SFT.MinMaxRangeType(min=0, max=86400, decimals=5)
    )
    kinetic_cycle_time = PhysicalParameter(
        name="Kinetic cycle time",
        dtype=float,
        unit="s",
        doc='Total readout time combining exposure, readout and an optional pause, in Kinetic readout mode.',
        range=SFT.MinMaxRangeType(min=0, max=86400, decimals=5)
    )
    accumulations_count = PhysicalParameter(
        'No. accumulations',
        int,
        doc='Number of accumulations in each acquisition. This only has effect if readout mode is Accumulate or Kinetic.',
        range=SFT.MinMaxRangeType(min=0, decimals=0),
        read_after_write=False
    )
    kinetics_count = PhysicalParameter(
        'No. kinetics cycles',
        int,
        doc='Number of (kinetic) cycles in each acquisition. This only has effect if readout mode is Kinetic.',
        range=SFT.MinMaxRangeType(min=0, decimals=0),
        read_after_write=False
    )
    temperature = PhysicalParameter(
        name="Temperature",
        dtype=int,
        unit="C"
    )
    temperature_status = PhysicalParameter(
        'Temperature status',
        dtype=np.ndarray,
    )
    cooler_active = PhysicalParameter(
        name="Cooler active",
        dtype=bool
    )
    # TODO FAST_KINETICS, RUN_TILL_ABORT not available
    acquisition_mode = PhysicalParameter(
        'Acquisition mode',
        dtype=str,
        doc='Mode of acquision (see CCD documentation)',
        range=SFT.ChoiceRangeType(**{'Single': 1, 'Accumulate': 2, 'Kinetics': 3}),
        read_after_write=False
    )
    readout_mode = PhysicalParameter(
        name='Readout mode',
        dtype=str,
        doc='Binning mode (see CCD documentation)',
        range=SFT.ChoiceRangeType(**{'FVB': 0, 'Image': 4}),
        read_after_write=False
    )
    ad_channel = PhysicalParameter(
        name='AD channel',
        dtype=str,
        doc='As your Andor SDK system may be capable of operating with more than one A-D converter the channel should be set.',
        range=SFT.ChoiceRangeType(),
        read_after_write=False
    )
    preamp_gain = PhysicalParameter(
        name='Preamp Gain',
        dtype=str,
        doc='The gain of the preamplifier can be set to one of the available values.',
        range=SFT.ChoiceRangeType(),
        read_after_write=False
    )
    vertical_shiftspeed = PhysicalParameter(
        name='Vertical shift speed',
        dtype=str,
        doc='Sets the shift speed of the registers in the vertical direction, there is one value recommended by the manufacturer.',
        range=SFT.ChoiceRangeType(),
        read_after_write=False
    )
    horizontal_shiftspeed = PhysicalParameter(
        name='Horizontal shift speed',
        dtype=str,
        doc='Sets the shift speed of the registers in the horizontal direction.',
        range=SFT.ChoiceRangeType(),
        read_after_write=False
    )
    detector_shape = PhysicalParameter(
        name='Detector shape',
        dtype=np.ndarray,
        doc='Shape of the detector'
    )
    pixel_size = PhysicalParameter(
        name='Pixel size',
        dtype=np.ndarray,
        unit='um'
    )
    shutter_mode = PhysicalParameter(
        'Shutter mode',
        dtype=str,
        doc='This determines whether the camera shutter should be open or closed and when. '
            'Auto FVB: Open during an FVB acquisition. '
            'Auto series: Open during a series. '
            'Auto: same as Solis Auto.',
        range=SFT.ChoiceRangeType(
            **{'Open': 1, 'Closed': 2, 'Auto FVB': 4, 'Auto series': 5, 'Auto': 0}),
        read_after_write=False
    )
    buffer = PhysicalParameter(
        name='Last acquisition',
        dtype=list,
        doc='Buffer in which acquired images from the whole kinetic series are stored.'
    )
    most_recent_buffer = PhysicalParameter(
        name='Most recent image',
        dtype=np.ndarray,
        doc='Buffer in which last retrieved image is stored.'
    )
    acquire = ActionParameter(name='Acquire')
    interrupt = ActionParameter(name='Interrupt acquisition')

    def __init__(self, *args, **kwargs):
        HardwareModule.__init__(self, *args, **kwargs)
        self._aborted = False
        self._current_kin = -1
        self.acquire_wait = WorkerTask(
            "Wait for acquisition",
            self.wait_for_acquisition,
            default_thread_pool=self.thread_pool
        )
        # polling functions
        self.poll_task = WorkerTask(
            "Poll CCD status",
            self._poll_all,
            default_thread_pool=self.thread_pool
        )
        self.poll_task.auxiliary_mutex = self.device_mutex
        # this must be here, not in connect: making connections to objects created in different
        # threads is not possible and will fail silently!
        self.acquire.sigActivated.connect(self.trigger_acquisition)
        self.interrupt.sigActivated.connect(self.interrupt_acquisition)
        self.polling_timer.timeout.connect(lambda: self.poll_task.run_on_pool())
        self.polling_status.sigValueChanged.connect(self.on_polling_status_sigValueChanged)
        self._last_temp = 0.0

    def connect(self):
        from .andor_ccd_dev import AndorCameraDiscovery
        self.host = AndorCameraDiscovery()
        self.host.discover_hardware()
        self.ccd_status.connect_to_hardware(
            read_func=self.host.GetStatus
        )
        self.acquisition_progress.connect_to_hardware(
            read_func=self.host.GetAcquisitionProgress
        )
        self.acquisition_mode.connect_to_hardware(
            write_func=lambda x: self.host.SetAcquisitionMode(
                self.acquisition_mode.range[x]) and self.acquisition_mode.setValue(x)
        )
        self.readout_mode.connect_to_hardware(
            write_func=self._set_readout_mode
        )
        self.exposure.connect_to_hardware(
            read_func=lambda: self._get_acquisition_timings()[0],
            write_func=lambda x: self.host.SetExposureTime(x)
        )
        self.acc_cycle_time.connect_to_hardware(
            read_func=lambda: self._get_acquisition_timings()[1],
            write_func=lambda x: self.host.SetAccumulationCycleTime(x)
        )
        self.accumulations_count.connect_to_hardware(
            write_func=lambda x: self.host.SetNumberAccumulations(x) and self.accumulations_count.setValue(x)
        )
        self.kinetics_count.connect_to_hardware(
            write_func=lambda x: self.host.SetNumberKinetics(x) and self.kinetics_count.setValue(x)
        )
        self.kinetic_cycle_time.connect_to_hardware(
            read_func=lambda: self._get_acquisition_timings()[2],
            write_func=lambda x: self.host.SetKineticCycleTime(x)
        )
        self.shutter_mode.connect_to_hardware(
            write_func=lambda x: (self.host.SetShutter(
                1,
                self.shutter_mode.range[x],
                40,
                40), self.shutter_mode.setValue(x))
        )
        self.temperature.connect_to_hardware(
            read_func=self.host.GetTemperature,
            write_func=lambda x: self.host.SetTemperature(int(x)),
            range_read_func=self._get_temperature_range
        )
        self.temperature_status.connect_to_hardware(
            read_func=lambda: np.array(self.host.GetTemperatureStatus())
        )
        self.cooler_active.connect_to_hardware(
            read_func=lambda: bool(self.host.IsCoolerOn()),
            write_func=lambda x: (self.host.CoolerOFF,
                                  self.host.CoolerON)[int(x)]()
        )
        self.ad_channel.connect_to_hardware(
            write_func=lambda x: self.host.SetADChannel(self.ad_channel.range[x]) and self.ad_channel.setValue(x),
            range_read_func=self._get_adchannel_range
        )
        self.preamp_gain.connect_to_hardware(
            write_func=lambda x: self.host.SetPreAmpGain(self.preamp_gain.range[x]) and self.preamp_gain.setValue(x),
            range_read_func=self._get_preamp_gain_range
        )
        self.vertical_shiftspeed.connect_to_hardware(
            write_func=lambda x: self.host.SetVSSpeed(
                self.vertical_shiftspeed.range[x]) and self.vertical_shiftspeed.setValue(x),
            range_read_func=self._get_vertical_shiftspeed_range
        )
        self.horizontal_shiftspeed.connect_to_hardware(
            write_func=lambda x: self.host.SetHSSpeed(0, self.horizontal_shiftspeed.range[
                x]) and self.horizontal_shiftspeed.setValue(x),
            range_read_func=self._get_horizontal_shiftspeed_range
        )
        self.detector_shape.connect_to_hardware(
            read_func=lambda: np.array(self.host.GetDetector())
        )
        self.pixel_size.connect_to_hardware(
            read_func=lambda: np.array(self.host.GetPixelSize())
        )
        # reset polling status
        self.log.info('connecting parameters finished, extra setup of CCD')
        self._nx_ny = None  # keeps track of acquisition X, Y size
        # add Andor events
        # must be manually resetted!
        # windows events signature:
        # win32event.CreateEvent(EventAttributes: PySECURITY_ATTRIBUTES, bManualReset: bool, bManualReset: bool, Name: PyUnicode)
        event = win32event.CreateEvent(None, True, False, "AndorCCDEvent")
        #self.host.SetDriverEvent(event)
        timeout = 5.0
        # some other stuff
        self.acquisition_progress.trigger_read().wait(timeout)
        self.accumulations_count.write_to_device(1).wait(timeout)
        self.kinetics_count.write_to_device(1).wait(timeout)
        # read ranges
        self.temperature.trigger_range_read().wait(timeout)
        self.preamp_gain.trigger_range_read().wait(timeout)
        self.ad_channel.trigger_range_read().wait(timeout)
        self.ad_channel.write_to_device("Channel 0").wait(timeout)
        # channel has to be set before hs, vs read range
        self.horizontal_shiftspeed.trigger_range_read().wait(timeout)
        self.vertical_shiftspeed.trigger_range_read().wait(timeout)
        # read values
        self.shutter_mode.write_to_device('Closed').wait(timeout)
        self.acquisition_mode.write_to_device('Single').wait(timeout)
        self.readout_mode.write_to_device('FVB').wait(timeout)
        # write values
        self.temperature.trigger_read().wait(timeout)
        self.ad_channel.write_to_device(list(self.ad_channel.range.keys())[0]).wait(timeout)
        self.preamp_gain.write_to_device(list(self.preamp_gain.range.keys())[0]).wait(timeout)
        self.horizontal_shiftspeed.write_to_device(list(self.horizontal_shiftspeed.range.keys())[0]).wait(timeout)
        #self.vertical_shiftspeed.write_to_device(list(self.vertical_shiftspeed.range.keys())[0]).wait(timeout)
        self.temperature.write_to_device(-80)
        self.temperature_status.trigger_read().wait(timeout)
        self.detector_shape.trigger_read().wait(timeout)
        self.pixel_size.trigger_read().wait(timeout)
        self.exposure.trigger_read().wait(timeout)  # one is enough as they share timings
        self.cooler_active.write_to_device(True).wait(timeout)
        self.cooler_active.trigger_read().wait(timeout)
        # acquisition mode impacts the timings
        self.acquisition_mode.sigValueChanged.connect(self.exposure.trigger_read)
        # readout mode impacts the timings
        self.readout_mode.sigValueChanged.connect(self.exposure.trigger_read)
        # shutter mode may impact timings
        self.shutter_mode.sigValueChanged.connect(self.exposure.trigger_read)
        # shiftSpeeds may impact timings
        self.horizontal_shiftspeed.sigValueChanged.connect(self.exposure.trigger_read)
        self.vertical_shiftspeed.sigValueChanged.connect(self.exposure.trigger_read)
        # kinetics/accumulations count can influence timings
        self.accumulations_count.sigValueChanged.connect(self.exposure.trigger_read)
        self.kinetics_count.sigValueChanged.connect(self.exposure.trigger_read)

    def disconnect(self):
        if self.host is not None:
            self.host.ShutDown()
        self.host = None

    def interrupt_acquisition(self):
        if self.host is None:
            raise Exception('not connected')
        self.host.AbortAcquisition()
        self._aborted = True

    @QtCore.Slot()
    def trigger_acquisition(self) -> WorkerTask:
        if self.host is None:
            raise Exception("not connected")
        # clear buffer
        self.buffer.setValue([])  # TODO: hopefully not None!
        # to keep track of acq progress
        self._n_acc = self.accumulations_count.value() if self.acquisition_mode.value() == 'Accumulate' else 1
        self._n_kin = self.kinetics_count.value() if self.acquisition_mode.value() == 'Kinetic' else 1
        self._current_kin = -1
        self.host.StartAcquisition()
        self.ccd_status.trigger_read()
        self.acquire_wait.run_on_pool()
        return self.acquire_wait

    def wait_for_acquisition(self):
        if self._aborted:
            self.log.info('acquisition interrupted')
            self._aborted = False
            return self.buffer.value()
        max_acq_duration = self.acc_cycle_time.value() + 1.0
        current_buffer = self.buffer.value()
        # this will wait for one image in an accumulation cycle only
        self.host.WaitForAcquisitionTimeOut(int(1000 * max_acq_duration))
        image = self._get_most_recent_image()
        self.acquire_wait.sig.sigResultReady.emit(image)  # emit at every new image
        self.most_recent_buffer.setValue(image)  # may be slow...?
        # the rest is for acc, kin series
        progress = self.host.GetAcquisitionProgress()
        progress_acc, progress_kin = progress
        if progress_kin > self._current_kin:
            # beginning of a new kinetic cycle
            current_buffer.append(image)
            self._current_kin = progress_kin
        else:
            # we are within an accumulation cycle, replace last data
            # TODO this may not catch ALL the images if they are very, very fast
            current_buffer[-1] = image
        # XXX: if value in the buffer paramater is mutable, then
        # the parameter does not emit sigValueChanged when modifying the value
        self.buffer.sigValueChanged.emit(self.buffer, self.buffer.value())
        # restart
        if progress_acc == (self._n_acc - 1) and progress_kin == (self._n_kin - 1):
            # end of acquisition
            self.ccd_status.trigger_read()
            return self.buffer.value()
        else:
            # not finished; start a new wait and return itself to wait for the next one
            self.acquire_wait.run_on_pool()
            return self.acquire_wait

    def _set_readout_mode(self, mode):
        x, y = self.host.GetDetector()
        if mode == 'FVB':
            self._nx_ny = (x, 1)
            self.host.SetFVBHBin(1)
            self.host.SetReadMode(0)
        elif mode == 'Image':
            self._nx_ny = (x, y)
            self.host.SetImage(1, 1, 1, x, 1, y)
            self.host.SetReadMode(4)
        self.readout_mode.setValue(mode)

    def _get_image(self):
        first, last = self.host.GetNumberNewImages()
        if self.host.last_error == 20024:  # DRV_NO_NEW_DATA
            raise Exception('no new images')
        self.log.debug(f'first: {first}, last: {last}')
        Nx, Ny = self._nx_ny
        arr, first, last = self.host.GetImages(first, last, Nx * Ny)
        arr = np.array(arr, dtype=np.int32)
        arr = arr.reshape((Nx, Ny)).T
        return arr

    def _get_most_recent_image(self):
        Nx, Ny = self._nx_ny
        arr = self.host.GetMostRecentImage(Nx * Ny)
        arr = np.array(arr, dtype=np.int32)
        arr = arr.reshape((Nx, Ny)).T
        return arr

    def _poll_all(self):
        status = self.host.GetStatus()
        self.ccd_status.setValue(status)
        self.ccd_status.actual_timestamp.setValue(datetime.now())
        if not self.ccd_status.value() == "Idle":
            # temperature can only be checked when CCD is idle (otherwise returns 0)
            temp = self._last_temp
        else:
            temp = self.host.GetTemperature()
        self._last_temp = temp
        self.temperature.setValue(temp)
        self.temperature.actual_timestamp.setValue(datetime.now())

    def _get_preamp_gain_range(self) -> SFT.ChoiceRangeType:
        n_gain_settings = int(self.host.GetNumberPreAmpGains())
        ret = SFT.ChoiceRangeType()
        for gain_setting in range(n_gain_settings):
            gain = float(self.host.GetPreAmpGain(gain_setting))
            gain_name = "{:2.2f}x".format(gain)
            ret[gain_name] = gain_setting
        return ret

    def _get_adchannel_range(self) -> SFT.ChoiceRangeType:
        n_ad_chan_settings = int(self.host.GetNumberADChannels())
        ret = SFT.ChoiceRangeType()
        for ad_chan_setting in range(n_ad_chan_settings):
            name = "Channel {}".format(ad_chan_setting)
            ret[name] = ad_chan_setting
        return ret

    def _get_horizontal_shiftspeed_range(self) -> SFT.ChoiceRangeType:
        channel = self.ad_channel.range[self.ad_channel.value()]
        if channel is None:
            raise ValueError("No AD channel selected.")
        n_shift_settings = int(self.host.GetNumberHSSpeeds(channel, 0))
        ret = SFT.ChoiceRangeType()
        for shift_setting in range(n_shift_settings):
            shift = float(self.host.GetHSSpeed(channel, 0, shift_setting))
            shift_name = "{:3.3f} MHz".format(shift)
            ret[shift_name] = shift_setting
        return ret

    def _get_vertical_shiftspeed_range(self) -> SFT.ChoiceRangeType:
        n_shift_settings = int(self.host.GetNumberVSSpeeds())
        recommended_shift_setting = self.host.GetFastestRecommendedVSSpeed()
        ret = SFT.ChoiceRangeType()
        for shift_setting in range(n_shift_settings):
            shift = float(self.host.GetVSSpeed(shift_setting))
            shift_name = "{:3.2f} us/pix".format(shift)
            if shift_setting == recommended_shift_setting[0]:
                shift_name = shift_name + " (recommended)"
            ret[shift_name] = shift_setting
        return ret

    def _get_acquisition_timings(self):
        exp, acc, kin = self.host.GetAcquisitionTimings()
        self.exposure.setValue(exp)
        self.acc_cycle_time.setValue(acc)
        self.kinetic_cycle_time.setValue(kin)
        return exp, acc, kin

    def _get_temperature_range(self):
        min, max = self.host.GetTemperatureRange()
        return SFT.MinMaxRangeType(min=min, max=max, decimals=0)
