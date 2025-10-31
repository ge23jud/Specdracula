import numpy as np

import ScopeFoundry as SFT


class AndorSpectrographHW(SFT.HardwareModule):
    entrance_mirror = SFT.PhysicalParameter(
        'Entrance mirror',
        dtype=str,
        doc="Current setting of the entrance of the spectrograph.",
        range=SFT.ChoiceRangeType(**{'Direct': 0, 'Side': 1})
    )
    exit_mirror = SFT.PhysicalParameter(
        'Exit mirror',
        dtype=str,
        doc="Current setting of the output of the spectrograph.",
        range=SFT.ChoiceRangeType(**{'Direct': 0, 'Side': 1})
    )
    selected_turret = SFT.PhysicalParameter(
        'Selected turret',
        dtype=str,
        doc="Selected grating turret of the spectrograph. "
            "Relevant only for spectrographs with more than 1 turret. "
            "User does not need to edit this value manually."
    )
    selected_grating = SFT.PhysicalParameter(
        'Selected grating',
        dtype=str,
        doc='Details of the currently selected grating. '
            'Information about installed gratings is retrieved from the spectrograph settings during connection.',
        range=SFT.ChoiceRangeType()
    )
    entrance_slit_direct = SFT.PhysicalParameter(
        'Entrance slit width',
        dtype=float,
        unit='m',
        doc='Width of the slit at the direct entrance of the spectrometer.',
        range=SFT.MinMaxRangeType(min=10e-6, max=2000e-6)
    )
    center_wavelength = SFT.PhysicalParameter(
        'Center wavelength',
        dtype=float,
        unit='m',
        doc='Wavelength that will be matched onto the center of the CCD.'
            'Changing the center wavelength moves the grating turret. '
            'The movement towards higher wavelengths is faster than reverse movement towards shorter wavelengths.',
        range=SFT.MinMaxRangeType(min=100e-9, max=2000e-9)
    )
    center_energy = SFT.PhysicalParameter(
        'Center energy',
        dtype=float,
        unit='eV',
        doc='Photon energy that will be matched onto the center of the CCD. This implicitly changed center wavelength.'
    )
    detector_pixels = SFT.PhysicalParameter(
        'No. detector pixels',
        dtype=int,
        value=2000,
        doc="Number of pixels of the detector in the X direction.",
        range=SFT.MinMaxRangeType(min=0, max=10000)
    )
    detector_pixel_width = SFT.PhysicalParameter(
        'Detector pixel width',
        dtype=float,
        value=15.0e-6,
        unit='m',
        doc="Width (in X direction) of a detector pixel.",
        range=SFT.MinMaxRangeType(min=0, max=100)
    )
    wavelength_calib = SFT.PhysicalParameter(
        'Wavelength array',
        dtype=np.ndarray,
        doc="An array containing `Detector pixels` elements, with `Center wavelength` in the center, "
            "mapping the detector pixels to wavelength."
    )
    calib_coeffs = SFT.PhysicalParameter(
        'Calibration coefficients',
        dtype=np.ndarray,
        doc="Internal spectrograph calibration coefficients, used to generate the `Wavelength array`."
    )
    device_id = SFT.ObjectParameter(
        'Device ID',
        str,
        value="0",
        doc="Device ID. Relevant only if more than one spectrograph is connected."
    )

    def connect(self):
        from .andor_spec_dev import AndorSpectrographDiscovery
        self.host = AndorSpectrographDiscovery()
        self.host.discover_hardware()
        dev_id = int(self.device_id.value())

        if int(self.host.IsFlipperMirrorPresent(dev_id, int(1))) == 1:
            self.entrance_mirror.connect_to_hardware(
                read_func=lambda: self.host.GetFlipperMirror(int(dev_id), 1),
                write_func=lambda x: self.host.SetFlipperMirror(int(dev_id), 1, int(self.exit_mirror.range[x]))
            )
            self.entrance_mirror.trigger_read()
        if int(self.host.IsFlipperMirrorPresent(dev_id, int(2))) == 1:
            self.exit_mirror.connect_to_hardware(
                read_func=lambda: self.host.GetFlipperMirror(int(dev_id), 2),
                write_func=lambda x: self.host.SetFlipperMirror(int(dev_id), 2, int(self.exit_mirror.range[x]))
            )
            self.exit_mirror.trigger_read()
        self.selected_turret.connect_to_hardware(
            read_func=lambda: str(self.host.GetTurret(int(dev_id))),
            write_func=lambda x: self.host.SetTurret(int(dev_id), int(x))
        )
        self.selected_grating.connect_to_hardware(
            read_func=lambda: self.host.GetGrating(int(dev_id)),
            write_func=lambda x: self.host.SetGrating(int(dev_id), self.selected_grating.range[x]),
            range_read_func=self._get_gratings_range
        )
        if int(self.host.IsSlitPresent(int(dev_id), int(2))) == 1:
            self.entrance_slit_direct.connect_to_hardware(
                read_func=lambda: float(self.host.GetSlitWidth(int(dev_id), int(2)) / 1e6),
                write_func=lambda w: self.host.SetSlitWidth(int(dev_id), int(2), width=float(w * 1e6))
            )
            self.entrance_slit_direct.trigger_read()
        self.center_wavelength.connect_to_hardware(
            read_func=lambda: float(self.host.GetWavelength(int(dev_id))) * 1e-9,
            write_func=lambda x: self.host.SetWavelength(int(dev_id), float(x / 1e-9)),
            range_read_func=self._get_wavelength_limits
        )
        self.center_energy.connect_to_hardware(
            read_func=self.get_center_energy,
            write_func=self.set_center_energy
        )
        self.detector_pixels.connect_to_hardware(
            write_func=lambda x: self.host.SetNumberPixels(int(dev_id), int(x)) and self.detector_pixels.setValue(x)
        )
        self.detector_pixel_width.connect_to_hardware(
            write_func=lambda x: self.host.SetPixelWidth(int(dev_id), float(x / 1e-6)),
            read_func=lambda: float(self.host.GetPixelWidth(int(dev_id))) * 1e-6
        )
        self.wavelength_calib.connect_to_hardware(
            read_func=lambda: np.array(self.host.GetCalibration(int(dev_id), self.detector_pixels.value()),
                                       dtype=np.float32)
        )
        self.calib_coeffs.connect_to_hardware(
            read_func=lambda: np.array(self.host.GetPixelCalibrationCoefficients(int(dev_id)), dtype=np.float32)
        )

        # cross-connections
        self.center_wavelength.sigValueChanged.connect(self.center_wavelength.trigger_range_read)
        self.center_wavelength.sigValueChanged.connect(self.wavelength_calib.trigger_read)
        self.center_wavelength.sigValueChanged.connect(self.calib_coeffs.trigger_read)
        self.center_wavelength.sigValueChanged.connect(self.center_energy.trigger_read)
        self.selected_grating.sigValueChanged.connect(self.center_wavelength.trigger_read)
        self.selected_grating.sigValueChanged.connect(self.center_wavelength.trigger_range_read)
        self.selected_grating.sigValueChanged.connect(self.wavelength_calib.trigger_read)
        self.selected_grating.sigValueChanged.connect(self.calib_coeffs.trigger_read)
        self.detector_pixels.sigValueChanged.connect(self.wavelength_calib.trigger_read)
        self.detector_pixels.sigValueChanged.connect(self.calib_coeffs.trigger_read)
        self.detector_pixel_width.sigValueChanged.connect(self.wavelength_calib.trigger_read)
        self.detector_pixel_width.sigValueChanged.connect(self.calib_coeffs.trigger_read)
        # manual adjustments
        self.selected_turret.trigger_read()
        self.detector_pixels.write_to_device(self.detector_pixels.value())
        self.detector_pixel_width.write_to_device(self.detector_pixel_width.value())
        self.selected_grating.trigger_range_read().wait(1.0)
        self.selected_grating.trigger_read().wait(1.0)
        self.center_wavelength.trigger_range_read().wait(1.0)
        self.center_wavelength.trigger_read()
        self.calib_coeffs.trigger_read()
        self.wavelength_calib.trigger_read()

    def disconnect(self):
        if self.host is not None:
            self.host.disconnect()
            self.host = None

    def get_center_energy(self):
        """Don't use this directly - use `center_energy` parameter instead."""
        center_wavelength = self.center_wavelength.value()
        h, c = 4.1457e-15, 2.9979e8  # eV . s, m / s
        if center_wavelength == 0:
            return float(0)
        else:
            energy = h * c / center_wavelength
            return energy

    def set_center_energy(self, energy: float):
        """Energy in eV.
        Don't use this directly - use `center_energy` parameter instead.
        """
        h, c = 4.1457e-15, 2.9979e8  # eV . s, m / s
        wavelength = h * c / energy
        self.center_wavelength.write_to_device(wavelength)

    def _get_wavelength_limits(self):
        grating_param = self.selected_grating
        min, max = self.host.GetWavelengthLimits(
            int(self.device_id.value()),
            int(grating_param.range[grating_param.value()])
        )
        return SFT.MinMaxRangeType(min=min, max=max, decimals=2)

    def _get_gratings_range(self) -> SFT.ChoiceRangeType:
        n_gratings = self.host.GetNumberGratings(int(self.device_id.value()))
        ret = SFT.ChoiceRangeType()
        for grating in range(1, n_gratings + 1):
            lines, blaze, home, offset = self.host.GetGratingInfo(0, grating, 64)
            grating_name = f"{str(int(lines))} l/mm, {str(int(blaze))} nm"
            ret[grating_name] = grating
        return ret
