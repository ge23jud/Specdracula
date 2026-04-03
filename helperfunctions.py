import numpy as np
from scipy.constants import h, c, e
import h5py
import datetime as dt
import math

class HelperFunctions():

    def wavelength_energy_converter(self, array):
        return h*c/array *1e9 /e


        
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
        lines.append(f"Excitation power:\t{power:.4f} uW{header_pad}")
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
        lines.append(f"Powerseries (mW)\t{ps_indices}")
 
        # -- data matrix -------------------------------------------------------
        for i in range(n):
            wl = f"{wavelength[i]:.9f}"
            counts = "\t".join(str(int(round(intensity[i, j]))) for j in range(m))
            lines.append(f"{wl}\t{counts}")
 
        # -- write with CRLF line endings --------------------------------------
        with open(filepath, "w", newline="\r\n", encoding="ascii") as fh:
            fh.write("\n".join(lines) + "\n")

        


# obj = HelperFunctions()
# obj.write_origin(
#     date=dt.datetime(2019, 2, 13, 15, 42),
#     measurement_type="X vs Y/Powerseries vs. Photoluminescence",
#     temperature=10.067,
#     integration_time=20.0,
#     power=194.0184,
#     center_wavelength=910.002,
#     dispersion_window=307.256,
#     entrance_slit_width=0.1,
#     exit_slit_width=0.0,
#     wavelength=wl,
#     excitation_power=ep,
#     intensity=counts,
#     filepath="C:\WSI\specdracula/test_output.origin",
# )