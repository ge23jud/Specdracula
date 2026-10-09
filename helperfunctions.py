import numpy as np
from scipy.constants import h, c, e
import h5py
import datetime as dt
import math
import os
import re
import time

class HelperFunctions():

    def wavelength_energy_converter(self, array):
        return h*c/array *1e9 /e

    def read_averaged_power(self, pm, duration, is_interrupted=None):
        """Average the power meter's reading over `duration` seconds.

        Repeatedly triggers a fresh read and averages the results. If
        `duration` is 0 (or less), takes a single reading. `is_interrupted`,
        if given, is polled between reads so a running sweep can bail out early.
        """
        if duration <= 0:
            pm.reading.trigger_read().wait(2.0)
            return float(pm.reading.value())

        readings = []
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            if is_interrupted is not None and is_interrupted():
                break
            pm.reading.trigger_read().wait(2.0)
            readings.append(pm.reading.value())

        if not readings:
            pm.reading.trigger_read().wait(2.0)
            readings.append(pm.reading.value())

        return float(np.mean(readings))


    def get_next_file_number(self, directory: str) -> str:
        """
        Scans a directory for files starting with a 3-digit number and returns
        the next number in the sequence as a zero-padded 3-digit string.

        Args:
            directory: Path to the directory to scan.

        Returns:
            The next available number as a 3-digit string (e.g. '007').

        Raises:
            ValueError: If the next number would exceed 999.
        """
        highest = -1
        pattern = re.compile(r'^(\d{3})')

        if not os.path.isdir(directory):
            return "000"

        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                highest = max(highest, int(match.group(1)))

        next_number = highest + 1

        if next_number > 999:
            raise ValueError("File number limit reached (999). Cannot increment further.")

        return f"{next_number:03d}"

        
    def write_origin(
        self,
        date: dt.datetime,
        measurement_type: str,
        temperature: float,
        integration_time: float,
        power: float,
        center_wavelength: float,
        dispersion_window: float,
        entrance_slit_width: float,
        exit_slit_width: float,
        wavelength: np.ndarray,
        excitation_power: np.ndarray,
        angles: np.ndarray,
        intensity: np.ndarray,
        filepath: str,
    ) -> None:
        """
        Write a power-series photoluminescence dataset to a .origin text file.
 
        The output format is a tab-delimited ASCII file with CRLF line endings,
        matching the structure of the reference file.
 
        Parameters
        ----------
        date : datetime
            Timestamp of the measurement (e.g. datetime(2019, 2, 13, 15, 42)).
        measurement_type : str
            Human-readable description stored in the "Measurement type:" header
            line (e.g. "X vs Y/Powerseries vs. Photoluminescence").
        temperature : float
            Sample temperature in Kelvin.
        integration_time : float
            CCD integration time in seconds.
        power : float
            Nominal excitation power for the "Excitation power:" header line,
            given in uW.
        center_wavelength : float
            Centre wavelength of the spectrometer window in nm.
        dispersion_window : float
            Full spectral width of the detector window in nm.
        entrance_slit_width : float
            Entrance slit width in mm.
        exit_slit_width : float
            Exit slit width in mm.
        wavelength : np.ndarray, shape (n,)
            Wavelength axis in nm. Each value is written with 9 decimal places.
        excitation_power : np.ndarray, shape (m,)
            Excitation power for each spectrum in Watts, written to the
            "Excitation power (W)" row.
        intensity : np.ndarray, shape (n, m)
            Detected intensity matrix. Row i, column j contains the counts for
            wavelength[i] at excitation_power[j]. Values are written as integers.
        filepath : str
            Destination path for the .origin file, including the file name and
            extension (e.g. "output/my_measurement.origin").
 
        Notes
        -----
        * The "Powerseries (mW)" row stores sequential integer indices (0, 1, 2, ...)
          rather than power values -- this mirrors the reference file behaviour.
        * Line endings are Windows-style CRLF (\\r\\n) to match the original format.
        * All header rows are padded with trailing tabs so that every row spans
          exactly m + 1 tab-delimited fields (key + value + m-1 empty fields),
          keeping the file rectangular when opened in spreadsheet applications.
        """

        def _fmt_ev(value: float, decimals: int = 3) -> str:
            """
            Format an eV value by *truncating* (flooring) to `decimals` decimal places.
    
            The original acquisition software truncates rather than rounds, so
            e.g. 0.4735 -> "0.473" rather than "0.474".
            """
            factor = 10 ** decimals
            truncated = math.floor(value * factor) / factor
            return f"{truncated:.{decimals}f}"
        

        def _dispersion_window_ev(center_nm: float, window_nm: float) -> float:
            """
            Return the energy span (eV) covered by a spectrometer dispersion window.
    
            The window spans [center - window/2, center + window/2] in wavelength.
            In energy space this is a non-symmetric interval; the eV value stored
            in the file is the absolute difference between the two edge energies.
            """
            lower_nm = center_nm - window_nm / 2.0
            upper_nm = center_nm + window_nm / 2.0
            return abs(
                self.wavelength_energy_converter(lower_nm)
                - self.wavelength_energy_converter(upper_nm)
            )


        wavelength = np.asarray(wavelength)

        excitation_power = np.asarray(excitation_power)
        intensity = np.asarray(intensity)
 
        n = wavelength.shape[0]
        m = excitation_power.shape[0]
 
        if intensity.shape != (n, m):
            raise ValueError(
                f"intensity must have shape (n, m) = ({n}, {m}), "
                f"got {intensity.shape}"
            )
 
        # --- derived values ---------------------------------------------------
        date_str = (
            f"{date.strftime('%A, %B')} {date.day}, {date.year}, "
            f"{date.hour % 12 or 12}:{date.strftime('%M')} "
            f"{'AM' if date.hour < 12 else 'PM'}"
        )
        center_ev = self.wavelength_energy_converter(center_wavelength)
        window_ev = _dispersion_window_ev(center_wavelength, dispersion_window)
 
        # trailing tabs that pad header rows to m+1 fields total:
        #   field_0 (key) + \t + field_1 (value) + (m-1) x \t = m+1 fields
        header_pad = "\t" * (m - 1)
 
        # the blank separator row has m+1 fields:  " " + m x \t
        blank_pad = "\t" * m
 
        # column-header / units strings repeat m times (once per power step)
        col_headers = "\t".join(["Powerspectrum "] * m)
        col_units = "\t".join([f"(Counts/{integration_time:.3f}s)"] * m)
 
        # excitation power row  (values in W)
        exc_power_vals = "\t".join(f"{v:g}" for v in excitation_power)
 
        # powerseries index row  (0-based integer indices)
        ps_indices = "\t".join(str(i) for i in range(m))
 
        # --- assemble lines ---------------------------------------------------
        lines: list[str] = []
 
        # -- metadata header ---------------------------------------------------
        lines.append(f"Date:\t{date_str}{header_pad}")
        lines.append(f"Measurement type:\t{measurement_type}{header_pad}")
        lines.append(f"Temperature: \t{temperature:.3f} K{header_pad}")
        lines.append(f"Integration time:\t{integration_time:.3f} s{header_pad}")
        lines.append(f"Excitation power:\t{power:.4f} mW{header_pad}")
        lines.append(
            f"Center wavelength\t{center_wavelength:.3f} nm"
            f" / {_fmt_ev(center_ev)} eV{header_pad}"
        )
        lines.append(
            f"Dispersion window:\t{dispersion_window:.3f} nm"
            f" / {_fmt_ev(window_ev)} eV{header_pad}"
        )
        lines.append(f"Entrance slit width:\t{entrance_slit_width:.3f} mm{header_pad}")
        lines.append(f"Exit slit width:\t{exit_slit_width:.3f} mm{header_pad}")
        lines.append(f" {blank_pad}")  # blank separator row
 
        # -- column headers ----------------------------------------------------
        lines.append(f"Wavelength \t{col_headers}")
        lines.append(f"(nm)\t{col_units}")
        lines.append(f"Excitation power (W)\t{exc_power_vals}")
        lines.append(f"Power HWP Position (°)\t{angles}")
 
        # -- data matrix -------------------------------------------------------
        for i in range(n):
            wl = f"{wavelength[i]:.9f}"
            counts = "\t".join(str(int(round(intensity[i, j]))) for j in range(m))
            lines.append(f"{wl}\t{counts}")
 
        # -- write with CRLF line endings --------------------------------------
        with open(filepath, "w", newline="\r\n", encoding="latin-1") as fh:
            fh.write("\n".join(lines) + "\n")


    def write_fourier_powerseries_origin(
        self,
        date: dt.datetime,
        temperature: float,
        integration_time: float,
        excitation_power: np.ndarray,
        angles: np.ndarray,
        pixel_arrays: list,
        filepath: str,
    ) -> None:
        """
        Write a power-series Fourier-imaging dataset to a .origin text file.

        Unlike `write_origin`, each power step contributes a full 2D pixel
        array (CMOS frame) rather than a single spectrum column, so the data
        block stores one image block per power step instead of one shared
        wavelength-indexed matrix. A "# Image" marker line precedes each
        block so the images can be split apart again when reading the file.

        Parameters
        ----------
        date : datetime
            Timestamp of the measurement.
        temperature : float
            Sample temperature in Kelvin.
        integration_time : float
            CMOS exposure time in seconds.
        excitation_power : np.ndarray, shape (m,)
            Powermeter reading for each power step, in Watts.
        angles : np.ndarray, shape (m,)
            Power HWP position for each power step, in degrees.
        pixel_arrays : list of np.ndarray, length m
            2D CMOS pixel array (height x width) for each power step.
        filepath : str
            Destination path for the .origin file.
        """
        excitation_power = np.asarray(excitation_power)
        angles = np.asarray(angles)
        m = excitation_power.shape[0]

        if len(pixel_arrays) != m or angles.shape[0] != m:
            raise ValueError(
                f"excitation_power, angles and pixel_arrays must all have length {m}, "
                f"got angles={angles.shape[0]}, pixel_arrays={len(pixel_arrays)}"
            )

        date_str = (
            f"{date.strftime('%A, %B')} {date.day}, {date.year}, "
            f"{date.hour % 12 or 12}:{date.strftime('%M')} "
            f"{'AM' if date.hour < 12 else 'PM'}"
        )

        exc_power_vals = "\t".join(f"{v:g}" for v in excitation_power)
        angle_vals = "\t".join(f"{a:g}" for a in angles)

        lines: list[str] = []

        # -- metadata header ---------------------------------------------------
        lines.append(f"Date:\t{date_str}")
        lines.append(f"Measurement type:\tPowerseries_Fourier")
        lines.append(f"Temperature: \t{temperature:.3f} K")
        lines.append(f"Integration time:\t{integration_time:.3f} s")
        lines.append(" ")  # blank separator row

        # -- power / angle axes --------------------------------------------------
        lines.append(f"Excitation power (W)\t{exc_power_vals}")
        lines.append(f"Power HWP Position (°)\t{angle_vals}")
        lines.append(" ")  # blank separator row

        # -- one 2D pixel block per power step, each preceded by a marker line --
        for i, frame in enumerate(pixel_arrays):
            frame = np.asarray(frame)
            lines.append(f"# Image {i}\tPower HWP Position (°)\t{angles[i]:g}\tExcitation power (W)\t{excitation_power[i]:g}")
            for row in frame:
                lines.append("\t".join(str(int(round(v))) for v in row))
            lines.append(" ")  # separator row before the next image

        # -- write with CRLF line endings --------------------------------------
        with open(filepath, "w", newline="\r\n", encoding="latin-1") as fh:
            fh.write("\n".join(lines) + "\n")


    def write_powercal_origin(
        self,
        date: dt.datetime,
        temperature: float,
        integration_time: float,
        excitation_power_uw: float,
        center_wavelength: float,
        dispersion_window: float,
        entrance_slit_width: float,
        exit_slit_width: float,
        angles: np.ndarray,
        powers: np.ndarray,
        filepath: str,
    ) -> None:
        """Write a power calibration dataset to a .origin text file.

        Parameters
        ----------
        temperature : float
            Sample temperature in Kelvin.
        integration_time : float
            Reference integration time in seconds (CCD exposure at time of calibration).
        excitation_power_uw : float
            Reference excitation power in µW for the header line.
        center_wavelength : float
            Centre wavelength in nm (0 if unavailable).
        dispersion_window : float
            Dispersion window in nm (0 if unavailable).
        entrance_slit_width : float
            Entrance slit width in mm (0 if unavailable).
        exit_slit_width : float
            Exit slit width in mm.
        angles : np.ndarray
            HWP angles in degrees for each measurement step.
        powers : np.ndarray
            Measured power in Watts for each step.
        filepath : str
            Destination .origin file path.
        """

        def _fmt_ev(value: float, decimals: int = 3) -> str:
            factor = 10 ** decimals
            truncated = math.floor(value * factor) / factor
            return f"{truncated:.{decimals}f}"

        def _fmt_power(v: float) -> str:
            s = f"{v:.7G}"
            s = re.sub(r'E([+-])0*(\d)', r'E\1\2', s)
            return s

        angles = np.asarray(angles)
        powers = np.asarray(powers)

        date_str = (
            f"{date.strftime('%A, %B')} {date.day}, {date.year}, "
            f"{date.hour % 12 or 12}:{date.strftime('%M')} "
            f"{'AM' if date.hour < 12 else 'PM'}"
        )

        if center_wavelength > 0:
            center_ev = self.wavelength_energy_converter(center_wavelength)
            lower_nm = center_wavelength - dispersion_window / 2.0
            upper_nm = center_wavelength + dispersion_window / 2.0
            window_ev = abs(
                self.wavelength_energy_converter(lower_nm)
                - self.wavelength_energy_converter(upper_nm)
            )
        else:
            center_ev = 0.0
            window_ev = 0.0

        lines: list[str] = []

        lines.append(f"Date:\t{date_str}\t")
        lines.append(f"Measurement type:\tX vs Y/Power HWP position vs. Power\t")
        lines.append(f"Temperature: \t{temperature:.3f} K\t")
        lines.append(f"Integration time:\t{integration_time:.3f} s\t")
        lines.append(f"Excitation power:\t{excitation_power_uw:.4f} uW\t")
        lines.append(
            f"Center wavelength\t{center_wavelength:.3f} nm"
            f" / {_fmt_ev(center_ev)} eV\t"
        )
        lines.append(
            f"Dispersion window:\t{dispersion_window:.3f} nm"
            f" / {_fmt_ev(window_ev)} eV\t"
        )
        lines.append(f"Entrance slit width:\t{entrance_slit_width:.3f} mm\t")
        lines.append(f"Exit slit width:\t{exit_slit_width:.3f} mm\t")
        lines.append(f" \t\t")

        lines.append(f"Energy \tExcitation power\tPowerspectrum ")
        lines.append(f"(eV)\t(W)\t(Counts/{integration_time:.3f}s)")
        lines.append(f"\t\t")

        for angle, power in zip(angles, powers):
            lines.append(f"{_fmt_power(power)}\t{angle:g}\t{_fmt_power(power)}")

        with open(filepath, "w", newline="\r\n", encoding="ascii") as fh:
            fh.write("\n".join(lines) + "\n")


    def read_powercal_origin(self, filepath: str):
        """Parse a power-calibration .origin file back into (angles_deg, powers_W).

        Each data row written by `write_powercal_origin` has the shape
        "<power W>\\t<angle deg>\\t<power W>"; header/unit rows are skipped
        since their fields don't all parse as floats.
        """
        angles = []
        powers = []
        with open(filepath, encoding="latin-1") as fh:
            for line in fh:
                parts = line.rstrip("\r\n").split("\t")
                if len(parts) < 2:
                    continue
                try:
                    power = float(parts[0])
                    angle = float(parts[1])
                except ValueError:
                    continue
                angles.append(angle)
                powers.append(power)
        return np.array(angles), np.array(powers)


