import time
import numpy as np
import pyqtgraph as pg
import ScopeFoundry as SFT
from ScopeFoundry import TurboComponentView
from PySide6 import QtCore, QtWidgets

from .fourfpump_ui import Ui_FourFPumpWidget
from MeasurementComponents.Photoluminescence.widget import _format_duration
from helperfunctions import HelperFunctions


class FourFPumpView(TurboComponentView, Ui_FourFPumpWidget):
    """Spectrum plot (left) and window-max intensity map vs. mirror offset (right).

    During a scan the spectrum plot shows the latest point. Afterwards (or
    during), clicking a pixel of the map shows the spectrum measured there.
    The shaded region on the spectrum plot is the spectral window used for
    the map; it can be dragged or set via the Window spinboxes.
    """

    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)

        self.setupUi(self)
        self.replace_imageview_with_plotitem()
        self.setup_plot()
        self.setup_map()

        SFT.connect_widget_to_param(self.XRange_SpinBox, component.x_range)
        SFT.connect_widget_to_param(self.XStep_SpinBox, component.x_step)
        SFT.connect_widget_to_param(self.YRange_SpinBox, component.y_range)
        SFT.connect_widget_to_param(self.YStep_SpinBox, component.y_step)
        SFT.connect_widget_to_param(self.SettleTime_DoubleSpinBox, component.settle_time)
        SFT.connect_widget_to_param(self.ReturnToCenter_CheckBox, component.return_to_center)
        SFT.connect_widget_to_param(self.WindowMin_DoubleSpinBox, component.window_min_nm)
        SFT.connect_widget_to_param(self.WindowMax_DoubleSpinBox, component.window_max_nm)
        SFT.connect_widget_to_param(self.xlabel_ComboBox, component.x_label)
        SFT.connect_widget_to_param(self.yscale_ComboBox, component.y_scale)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)

        SFT.connect_widget_to_param(self.Snapshot_PushButton, component.single_ActionParam)
        SFT.connect_widget_to_param(self.StartLive_PushButton, component.continuous_ActionParam)
        SFT.connect_widget_to_param(self.StopLive_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.StopScan_PushButton, component.interrupt_ActionParam)

        self.StartScan_PushButton.clicked.connect(self._on_start_scan_clicked)

        component.n_measurements.sigValueChanged.connect(self.update_nummeasurements_label)
        component.x_label.sigValueChanged.connect(self._on_xlabel_changed)
        component.x_label.sigValueChanged.connect(self._update_window_region)
        component.window_min_nm.sigValueChanged.connect(self._update_window_region)
        component.window_max_nm.sigValueChanged.connect(self._update_window_region)
        component.y_scale.sigValueChanged.connect(self._on_yscale_changed)
        component.intensity_counts.sigValueChanged.connect(self._update_plot_single)
        component.intensity_counts_series.sigValueChanged.connect(self._update_plot_scan)
        component.map_data.sigValueChanged.connect(self._update_map)
        component.measurement_running.sigValueChanged.connect(self._on_measurement_running_changed)
        component.completed_measurement_steps.sigValueChanged.connect(self._on_progress_changed)

        self._run_start_time = None
        self._eta_seconds_remaining = None
        self._eta_timer = QtCore.QTimer(self)
        self._eta_timer.setInterval(1000)
        self._eta_timer.timeout.connect(self._tick_eta)

        self.update_nummeasurements_label()
        self._update_window_region()


    def replace_imageview_with_plotitem(self):
        """Swap the Designer ImageView for one with a PlotItem view, so the map has axes."""
        parent = self.img_view.parent()
        layout = parent.layout()
        index = layout.indexOf(self.img_view)
        size_policy = self.img_view.sizePolicy()
        layout.removeWidget(self.img_view)
        self.img_view.deleteLater()
        self.img_view = pg.ImageView(view=pg.PlotItem())
        self.img_view.setSizePolicy(size_policy)
        layout.insertWidget(index, self.img_view)

    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Energy", units="eV")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)
        self.spectrum_plotDataItem = self.plot_widget.plot([], [])

        self.window_region = pg.LinearRegionItem(brush=pg.mkBrush(255, 165, 0, 40))
        self.window_region.setZValue(-10)
        self.plot_widget.getPlotItem().addItem(self.window_region, ignoreBounds=True)
        self.window_region.sigRegionChangeFinished.connect(self._on_window_region_dragged)

    def setup_map(self):
        self.map_plot_item = self.img_view.getView()
        self.map_plot_item.setLabel("bottom", "Mirror X offset", units="steps")
        self.map_plot_item.setLabel("left", "Mirror Y offset", units="steps")
        self.map_plot_item.showGrid(x=True, y=True, alpha=0.2)
        self.map_plot_item.setAspectLocked(False)
        # ImageView rows are image x, so keep +Y pointing up like the axis label says.
        self.map_plot_item.invertY(False)

        self.selected_marker = pg.ScatterPlotItem(size=12, pen=pg.mkPen('r', width=2), brush=None, symbol='s')
        self.map_plot_item.addItem(self.selected_marker)
        self.selected_marker.setZValue(2)

        self.map_plot_item.scene().sigMouseClicked.connect(self._on_map_clicked)


    def update_nummeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))

    def _x_data(self):
        if self.component.x_label.value() == "Wavelength":
            return self.component.wavelength_nm.value()
        return self.component.energy_ev.value()

    @QtCore.Slot()
    def _on_xlabel_changed(self):
        if self.component.x_label.value() == "Energy":
            self.plot_widget.setLabel("bottom", "Energy", units="eV")
        else:
            self.plot_widget.setLabel("bottom", "Wavelength", units="nm")

    @QtCore.Slot()
    def _on_yscale_changed(self):
        self.plot_widget.setLogMode(y=self.component.y_scale.value() == "Logarithmic")


    def _energy_axis(self):
        return self.component.x_label.value() != "Wavelength"

    @QtCore.Slot()
    def _update_window_region(self):
        """Show the spectral window (stored in nm) in the current x-axis unit."""
        lo, hi = self.component.window_min_nm.value(), self.component.window_max_nm.value()
        if hi <= lo or lo <= 0:
            self.window_region.hide()
            return
        if self._energy_axis():
            lo, hi = HelperFunctions().wavelength_energy_converter(np.array([hi, lo]))
        self.window_region.blockSignals(True)
        self.window_region.setRegion((lo, hi))
        self.window_region.blockSignals(False)
        self.window_region.show()

    @QtCore.Slot()
    def _on_window_region_dragged(self):
        lo, hi = self.window_region.getRegion()
        if self._energy_axis():
            if lo <= 0:
                return
            lo, hi = HelperFunctions().wavelength_energy_converter(np.array([hi, lo]))
        # set max first if the window moves up, so min < max holds in between
        if lo >= self.component.window_max_nm.value():
            self.component.window_max_nm.setValue(float(hi))
            self.component.window_min_nm.setValue(float(lo))
        else:
            self.component.window_min_nm.setValue(float(lo))
            self.component.window_max_nm.setValue(float(hi))

    def _show_spectrum(self, Y, title=None):
        X = self._x_data()
        Y = np.asarray(Y).flatten()
        if X is None or len(X) != len(Y):
            X = np.arange(len(Y))
        self.spectrum_plotDataItem.setData(x=X, y=Y)
        self.plot_widget.setTitle(title)

    @QtCore.Slot()
    def _update_plot_single(self):
        self._show_spectrum(self.component.intensity_counts.value(), title=None)

    @QtCore.Slot()
    def _update_plot_scan(self):
        spectrum = self.component.intensity_counts_series.value()
        x_offsets = self.component.x_offsets.value()
        y_offsets = self.component.y_offsets.value()
        if spectrum is None or x_offsets is None or y_offsets is None:
            return
        ix = self.component.current_x_index.value()
        iy = self.component.current_y_index.value()
        if spectrum.ndim > 1:
            spectrum = spectrum.reshape(spectrum.shape[0], -1).mean(axis=0)
        self._show_spectrum(spectrum, title=f"X = {x_offsets[ix]}, Y = {y_offsets[iy]} steps")
        self.selected_marker.setData([x_offsets[ix]], [y_offsets[iy]])


    @QtCore.Slot()
    def _update_map(self):
        data = self.component.map_data.value()
        x_offsets = self.component.x_offsets.value()
        y_offsets = self.component.y_offsets.value()
        if data is None or data.size == 0 or x_offsets is None or y_offsets is None:
            return
        finite = data[np.isfinite(data)]
        fill = finite.min() if finite.size else 0.0
        display_data = np.where(np.isfinite(data), data, fill)
        x_step = (x_offsets[1] - x_offsets[0]) if len(x_offsets) > 1 else 1
        y_step = (y_offsets[1] - y_offsets[0]) if len(y_offsets) > 1 else 1
        # pixel centres on the offsets
        self.img_view.setImage(
            display_data,
            pos=(x_offsets[0] - x_step / 2, y_offsets[0] - y_step / 2),
            scale=(x_step, y_step),
            autoRange=True,
            autoLevels=True,
        )

    @QtCore.Slot(object)
    def _on_map_clicked(self, event):
        grid = self.component.spectra_grid.value()
        x_offsets = self.component.x_offsets.value()
        y_offsets = self.component.y_offsets.value()
        if grid is None or x_offsets is None or y_offsets is None:
            return
        view_box = self.map_plot_item.getViewBox()
        if not view_box.sceneBoundingRect().contains(event.scenePos()):
            return
        point = view_box.mapSceneToView(event.scenePos())
        ix = int(np.argmin(np.abs(x_offsets - point.x())))
        iy = int(np.argmin(np.abs(y_offsets - point.y())))
        spectrum = grid[ix, iy, :]
        if not np.any(np.isfinite(spectrum)):
            return
        self._show_spectrum(spectrum, title=f"X = {x_offsets[ix]}, Y = {y_offsets[iy]} steps")
        self.selected_marker.setData([x_offsets[ix]], [y_offsets[iy]])


    @QtCore.Slot()
    def _on_measurement_running_changed(self):
        if self.component.measurement_running.value():
            self._run_start_time = time.time()
            self._eta_seconds_remaining = None
            self._eta_timer.start()
            self.Status_Label.setText("Running...")
            self.Status_Label.setStyleSheet(
                "color: orange; font-size: 8pt; font-weight: bold; padding-right: 4px;")
        elif self.Status_Label.text().startswith("Running"):
            self._eta_timer.stop()
            self._run_start_time = None
            self._eta_seconds_remaining = None
            self.Status_Label.setText("Finished")
            self.Status_Label.setStyleSheet(
                "color: #00dd00; font-size: 8pt; font-weight: bold; padding-right: 4px;")

    @QtCore.Slot()
    def _on_progress_changed(self):
        if self._run_start_time is None:
            return
        completed = self.component.completed_measurement_steps.value()
        total = self.component.total_measurement_steps.value()
        if completed <= 0 or total <= completed:
            return
        elapsed = time.time() - self._run_start_time
        self._eta_seconds_remaining = elapsed / completed * (total - completed)
        self._update_status_label_eta()

    @QtCore.Slot()
    def _tick_eta(self):
        if self._eta_seconds_remaining is None:
            return
        self._eta_seconds_remaining = max(0.0, self._eta_seconds_remaining - 1.0)
        self._update_status_label_eta()

    def _update_status_label_eta(self):
        if self._eta_seconds_remaining is None:
            self.Status_Label.setText("Running...")
        else:
            self.Status_Label.setText(f"Running... (~{_format_duration(self._eta_seconds_remaining)} left)")


    @QtCore.Slot()
    def _on_start_scan_clicked(self):
        if not self.component.is_shutter_open():
            reply = QtWidgets.QMessageBox.question(
                self, "Shutter closed", "Shutter closed. Continue?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply != QtWidgets.QMessageBox.StandardButton.Yes:
                return
        self.component.scan_ActionParam.activate()
