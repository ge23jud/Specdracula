from PySide6 import QtCore
import ScopeFoundry as SFT
import pyqtgraph as pg
import numpy as np
import os
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .photoluminescence_ui import Ui_PhotoluminescenceWidget
from helperfunctions import HelperFunctions

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog

_HC_EV_NM = 1239.84193  # h·c in eV·nm, used for stitch-line repositioning

# Each scheme: list of hex colors from t=0 (low HWP angle) to t=1 (high HWP angle).
COLOR_SCHEMES = {
    'Viridis':  ['#440154','#3e4989','#31688e','#26828e','#1f9e89','#35b779','#6ece58','#fde725'],
    'Spectral': ['#9e0142','#d53e4f','#f46d43','#fdae61','#e6f598','#abdda4','#66c2a5','#3288bd','#5e4fa2'],
    'CoolWarm': ['#1565c0','#42a5f5','#80deea','#ffca28','#ef5350','#b71c1c'],
    'Warm':     ['#fff176','#ffca28','#ffa000','#ff6f00','#e64a19','#bf360c'],
    'Turbo':    ['#4777ef','#22cfdb','#3ddc84','#b2fd2f','#fdc328','#fe4f0c'],
}


def _scheme_color(t, scheme_name):
    """Return a hex color by linearly interpolating within the named scheme at position t ∈ [0, 1]."""
    colors = COLOR_SCHEMES.get(scheme_name, COLOR_SCHEMES['Viridis'])
    t = max(0.0, min(1.0, t))
    pos = t * (len(colors) - 1)
    i = int(pos)
    f = pos - i
    if i >= len(colors) - 1:
        return colors[-1]
    def parse(h):
        h = h.lstrip('#')
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r0, g0, b0 = parse(colors[i])
    r1, g1, b1 = parse(colors[i + 1])
    r = int(r0 + f * (r1 - r0))
    g = int(g0 + f * (g1 - g0))
    b = int(b0 + f * (b1 - b0))
    return f'#{r:02x}{g:02x}{b:02x}'

class _SettingsDialog(QtWidgets.QDialog):
    """Secondary settings panel (log steps, measurement count, plot display),
    kept out of the main view so the standard interface stays uncluttered."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        outer = QtWidgets.QVBoxLayout(self)
        columns = QtWidgets.QHBoxLayout()
        outer.addLayout(columns)

        left = QtWidgets.QVBoxLayout()
        self.LogSteps_CheckBox = QtWidgets.QCheckBox("Log Steps")
        left.addWidget(self.LogSteps_CheckBox)

        cal_row = QtWidgets.QHBoxLayout()
        cal_row.addWidget(QtWidgets.QLabel("Power Calibration"))
        self.SelectPowerCal_PushButton = QtWidgets.QPushButton("Select Power Cal File...")
        cal_row.addWidget(self.SelectPowerCal_PushButton)
        left.addLayout(cal_row)

        self.PowerCalFile_Label = QtWidgets.QLabel("No power calibration file selected")
        self.PowerCalFile_Label.setWordWrap(True)
        left.addWidget(self.PowerCalFile_Label)
        left.addStretch()

        right = QtWidgets.QFormLayout()
        self.NumMeasurements_SpinBox = QtWidgets.QSpinBox()
        self.NumMeasurements_SpinBox.setMinimum(1)
        self.NumMeasurements_SpinBox.setMaximum(100000)
        right.addRow("Measurements", self.NumMeasurements_SpinBox)

        self.yscale_ComboBox = QtWidgets.QComboBox()
        self.yscale_ComboBox.addItems(["Linear", "Logarithmic"])
        right.addRow("Scale", self.yscale_ComboBox)

        self.xlabel_ComboBox = QtWidgets.QComboBox()
        self.xlabel_ComboBox.addItems(["Energy", "Wavelength"])
        right.addRow("X-axis", self.xlabel_ComboBox)

        self.ColorScheme_ComboBox = QtWidgets.QComboBox()
        self.ColorScheme_ComboBox.addItems(["Viridis", "Spectral", "CoolWarm", "Warm", "Turbo"])
        right.addRow("Colors", self.ColorScheme_ComboBox)

        columns.addLayout(left)
        columns.addLayout(right)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.accept)
        outer.addWidget(close_button)


class PhotoluminescenceView(TurboComponentView, Ui_PhotoluminescenceWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)

        self.setupUi(self)
        self.setup_plot()

        self._settings_dialog = _SettingsDialog(self)
        self.LogSteps_CheckBox = self._settings_dialog.LogSteps_CheckBox
        self.SelectPowerCal_PushButton = self._settings_dialog.SelectPowerCal_PushButton
        self.PowerCalFile_Label = self._settings_dialog.PowerCalFile_Label
        self.NumMeasurements_SpinBox = self._settings_dialog.NumMeasurements_SpinBox
        self.yscale_ComboBox = self._settings_dialog.yscale_ComboBox
        self.xlabel_ComboBox = self._settings_dialog.xlabel_ComboBox
        self.ColorScheme_ComboBox = self._settings_dialog.ColorScheme_ComboBox

        SFT.connect_widget_to_param(self.yscale_ComboBox, component.y_scale)
        SFT.connect_widget_to_param(self.xlabel_ComboBox, component.x_label)
        SFT.connect_widget_to_param(self.PsStart_DoubleSpinBox, component.ps_start)
        SFT.connect_widget_to_param(self.PsStop_DoubleSpinBox, component.ps_stop)
        SFT.connect_widget_to_param(self.PsStep_DoubleSpinBox, component.ps_step)
        SFT.connect_widget_to_param(self.LogSteps_CheckBox, component.ps_log_steps)
        SFT.connect_widget_to_param(self.NumMeasurements_SpinBox, component.n_measurements)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)

        SFT.connect_widget_to_param(self.Snapshot_PushButton, component.single_ActionParam)
        SFT.connect_widget_to_param(self.SavePL_PushButton, component.save_single_ActionParam)
        SFT.connect_widget_to_param(self.StartLivePL_PushButton, component.continuous_ActionParam)
        SFT.connect_widget_to_param(self.StopLivePL_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.StartPS_PushButton, component.powerseries_ActionParam)
        SFT.connect_widget_to_param(self.PxlCorrection_checkBox, component.pixel_correction_enabled)
        SFT.connect_widget_to_param(self.ColorScheme_ComboBox, component.colorscheme)
        SFT.connect_widget_to_param(self.BandwidthSweepEnable_CheckBox, component.bs_enable)
        SFT.connect_widget_to_param(self.MinEnergy_DoubleSpinBox, component.bs_min_energy)
        SFT.connect_widget_to_param(self.MaxEnergy_DoubleSpinBox, component.bs_max_energy)
        SFT.connect_widget_to_param(self.Overlap_DoubleSpinBox, component.bs_overlap)

        self.SelectReference_PushButton.clicked.connect(self._on_select_reference_files)
        self.ShowReference_CheckBox.toggled.connect(self._on_reference_toggled)
        self.SelectPowerCal_PushButton.clicked.connect(self._on_select_powercal_file)
        self.Settings_PushButton.clicked.connect(self._on_open_settings)

        component.x_label.sigValueChanged.connect(self._on_xlabel_changed)
        component.intensity_counts.sigValueChanged.connect(self._update_plot_single)
        component.intensity_counts_powerseries.sigValueChanged.connect(self._update_plot_powerseries)
        component.stitch_edge_nm.sigValueChanged.connect(self._on_stitch_edge)
        component.measurement_running.sigValueChanged.connect(self._on_measurement_running_changed)
        component.powerseries_ActionParam.sigActivated.connect(self._clear_plot)
        component.single_ActionParam.sigActivated.connect(self._clear_plot)
        component.continuous_ActionParam.sigActivated.connect(self._clear_plot)

        self._stitch_edges_nm = []   # [(wl_lo, wl_hi), …] one per completed stitch
        self._stitch_lines  = []     # [(line_lo, line_hi), …] InfiniteLine pairs

        self._reference_files = []    # paths of previously saved measurements to overlay
        self._reference_curves = []   # PlotDataItems currently shown for those files
        self._live_curve_count = 1    # tracks live (non-reference) curves; 1 for the placeholder from setup_plot


    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Wavelength", units="nm")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)

        self.spectrum_plotDataItem = self.plot_widget.plot([], [])

        self.legend = self.plot_widget.addLegend(offset=(10, 10), labelTextSize='7pt')
        


    @QtCore.Slot()
    def _on_xlabel_changed(self):
        label_type = self.component.x_label.value()
        if label_type == "Energy":
            self.plot_widget.setLabel("bottom", "Energy", units="eV")
        else:
            self.plot_widget.setLabel("bottom", "Wavelength", units="nm")
        self._reposition_stitch_lines()
        if self.ShowReference_CheckBox.isChecked():
            self._replot_references()

    @QtCore.Slot()
    def _on_measurement_running_changed(self):
        if self.component.measurement_running.value():
            self.Status_Label.setText("Running...")
            self.Status_Label.setStyleSheet(
                "color: orange; font-size: 8pt; font-weight: bold; padding-right: 4px;")
        elif self.Status_Label.text() == "Running...":
            self.Status_Label.setText("Finished")
            self.Status_Label.setStyleSheet(
                "color: #00dd00; font-size: 8pt; font-weight: bold; padding-right: 4px;")

    @QtCore.Slot()
    def _on_stitch_edge(self):
        edges = self.component.stitch_edge_nm.value()
        if edges is None or len(edges) < 2:
            return
        wl_lo, wl_hi = float(edges[0]), float(edges[1])
        self._stitch_edges_nm.append((wl_lo, wl_hi))
        pen = pg.mkPen(color=(140, 140, 140), width=1, style=QtCore.Qt.PenStyle.DashLine)
        pos_lo, pos_hi = self._stitch_positions(wl_lo, wl_hi)
        line_lo = pg.InfiniteLine(pos=pos_lo, angle=90, pen=pen)
        line_hi = pg.InfiniteLine(pos=pos_hi, angle=90, pen=pen)
        self.plot_widget.addItem(line_lo)
        self.plot_widget.addItem(line_hi)
        self._stitch_lines.append((line_lo, line_hi))

    def _stitch_positions(self, wl_lo, wl_hi):
        """Return (pos_lo, pos_hi) in current x-axis units."""
        if self.component.x_label.value() == "Energy":
            return _HC_EV_NM / wl_lo, _HC_EV_NM / wl_hi
        return wl_lo, wl_hi

    def _reposition_stitch_lines(self):
        for k, (line_lo, line_hi) in enumerate(self._stitch_lines):
            wl_lo, wl_hi = self._stitch_edges_nm[k]
            pos_lo, pos_hi = self._stitch_positions(wl_lo, wl_hi)
            line_lo.setValue(pos_lo)
            line_hi.setValue(pos_hi)


    @QtCore.Slot()
    def _update_plot_single(self):
        xaxis = self.component.x_label.value()
        if xaxis == "Wavelength":
            X = self.component.wavelength_nm.value()
        elif xaxis == "Energy":
            X = self.component.energy_ev.value()
        Y = self.component.intensity_counts.value().flatten()
        if self._live_curve_count == 0:
            self.spectrum_plotDataItem = self.plot_widget.plot(X, Y)
            self._live_curve_count = 1
        else:
            self.spectrum_plotDataItem.setData(x=X, y=Y)


    @QtCore.Slot()
    def _update_plot_powerseries(self):
        n = self.component.n_measurements.value()
        num_items = self._live_curve_count
        i = num_items % max(n, 1)
        t = i / max(n - 1, 1)
        color = _scheme_color(t, self.component.colorscheme.value())
        current_angles = self.component.current_angles.value()
        if current_angles is not None and i < len(current_angles):
            angle = current_angles[i]
        else:
            angle = self.component.ps_start.value() + i * self.component.ps_step.value()

        xaxis = self.component.x_label.value()
        if xaxis == "Wavelength":
            X = self.component.wavelength_nm.value()
        elif xaxis == "Energy":
            X = self.component.energy_ev.value()

        Y = self.component.intensity_counts_powerseries.value().flatten()
        self.spectrum_plotDataItem = self.plot_widget.plot(X, Y, pen=color)
        self.spectrum_plotDataItem.setZValue(i)

        if num_items < n:
            self.legend.addItem(self.spectrum_plotDataItem, name=f"{angle:.1f}°")
        self._live_curve_count += 1


    @QtCore.Slot()
    def _clear_plot(self):
        self.plot_widget.clear()   # also removes InfiniteLines and reference curves
        self.legend.clear()
        self._stitch_edges_nm.clear()
        self._stitch_lines.clear()
        self._reference_curves.clear()
        self._live_curve_count = 0
        if self.ShowReference_CheckBox.isChecked():
            self._replot_references()


    @QtCore.Slot()
    def _on_select_reference_files(self):
        start_dir = self.component.save_directory.value() or ""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Reference Measurements", start_dir, "Origin files (*.origin);;All files (*)"
        )
        if not paths:
            return
        self._reference_files = paths
        names = ", ".join(os.path.basename(p) for p in paths)
        if len(names) > 60:
            names = f"{len(paths)} files selected"
        self.ReferenceFiles_Label.setText(names)
        if self.ShowReference_CheckBox.isChecked():
            self._replot_references()


    @QtCore.Slot()
    def _on_select_powercal_file(self):
        start_dir = self.component.save_directory.value() or ""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Power Calibration File", start_dir, "Origin files (*.origin);;All files (*)"
        )
        if not path:
            return
        self.component.powercal_filepath.setValue(path)
        self.PowerCalFile_Label.setText(os.path.basename(path))


    @QtCore.Slot()
    def _on_open_settings(self):
        self._settings_dialog.show()
        self._settings_dialog.raise_()
        self._settings_dialog.activateWindow()


    @QtCore.Slot(bool)
    def _on_reference_toggled(self, checked):
        if checked:
            self._replot_references()
        else:
            self._remove_reference_curves()


    def _replot_references(self):
        self._remove_reference_curves()
        if not self._reference_files:
            return
        xaxis = self.component.x_label.value()
        pen = pg.mkPen(color=(160, 160, 160), width=1, style=QtCore.Qt.PenStyle.DotLine)
        for path in self._reference_files:
            wavelength, intensity = self._load_reference_spectrum(path)
            if wavelength is None:
                continue
            if xaxis == "Energy":
                X = HelperFunctions().wavelength_energy_converter(wavelength)
            else:
                X = wavelength
            curve = self.plot_widget.plot(X, intensity, pen=pen, name=os.path.basename(path))
            curve.setZValue(-1)
            self._reference_curves.append(curve)


    def _remove_reference_curves(self):
        for curve in self._reference_curves:
            self.plot_widget.removeItem(curve)
            self.legend.removeItem(curve)
        self._reference_curves.clear()


    @staticmethod
    def _load_reference_spectrum(path):
        """Parse a .origin file, returning (wavelength_nm, intensity) averaged over its power columns."""
        wavelengths = []
        rows = []
        try:
            with open(path, encoding="latin-1") as fh:
                for line in fh:
                    parts = line.rstrip("\r\n").split("\t")
                    try:
                        wl = float(parts[0])
                    except (ValueError, IndexError):
                        continue
                    counts = []
                    for p in parts[1:]:
                        try:
                            counts.append(float(p))
                        except ValueError:
                            break
                    if counts:
                        wavelengths.append(wl)
                        rows.append(counts)
        except OSError:
            return None, None
        if not wavelengths:
            return None, None
        return np.array(wavelengths), np.mean(np.array(rows), axis=1)



    