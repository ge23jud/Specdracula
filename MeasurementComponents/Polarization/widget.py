import time
import ScopeFoundry as SFT
from ScopeFoundry import TurboComponentView
from PySide6 import QtCore, QtWidgets

from .polarization_ui import Ui_PolarizationWidget
from MeasurementComponents.Photoluminescence.widget import _scheme_color, _format_duration


class _SettingsDialog(QtWidgets.QDialog):
    """Secondary settings panel (measurement count, plot display)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        outer = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        outer.addLayout(form)

        self.NumMeasurements_SpinBox = QtWidgets.QSpinBox()
        self.NumMeasurements_SpinBox.setMinimum(1)
        self.NumMeasurements_SpinBox.setMaximum(100000)
        form.addRow("Measurements", self.NumMeasurements_SpinBox)

        self.yscale_ComboBox = QtWidgets.QComboBox()
        self.yscale_ComboBox.addItems(["Linear", "Logarithmic"])
        form.addRow("Scale", self.yscale_ComboBox)

        self.xlabel_ComboBox = QtWidgets.QComboBox()
        self.xlabel_ComboBox.addItems(["Energy", "Wavelength"])
        form.addRow("X-axis", self.xlabel_ComboBox)

        self.ColorScheme_ComboBox = QtWidgets.QComboBox()
        self.ColorScheme_ComboBox.addItems(["Viridis", "Spectral", "CoolWarm", "Warm", "Turbo"])
        form.addRow("Colors", self.ColorScheme_ComboBox)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.accept)
        outer.addWidget(close_button)


class PolarizationView(TurboComponentView, Ui_PolarizationWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)

        self.setupUi(self)
        self.setup_plot()

        self._settings_dialog = _SettingsDialog(self)
        self.NumMeasurements_SpinBox = self._settings_dialog.NumMeasurements_SpinBox
        self.yscale_ComboBox = self._settings_dialog.yscale_ComboBox
        self.xlabel_ComboBox = self._settings_dialog.xlabel_ComboBox
        self.ColorScheme_ComboBox = self._settings_dialog.ColorScheme_ComboBox

        SFT.connect_widget_to_param(self.yscale_ComboBox, component.y_scale)
        SFT.connect_widget_to_param(self.xlabel_ComboBox, component.x_label)
        SFT.connect_widget_to_param(self.ColorScheme_ComboBox, component.colorscheme)
        SFT.connect_widget_to_param(self.NumMeasurements_SpinBox, component.n_measurements)
        SFT.connect_widget_to_param(self.AngleStart_DoubleSpinBox, component.ps_start)
        SFT.connect_widget_to_param(self.AngleStop_DoubleSpinBox, component.ps_stop)
        SFT.connect_widget_to_param(self.AngleStep_DoubleSpinBox, component.ps_step)
        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)

        SFT.connect_widget_to_param(self.Snapshot_PushButton, component.single_ActionParam)
        SFT.connect_widget_to_param(self.Save_PushButton, component.save_single_ActionParam)
        SFT.connect_widget_to_param(self.StartLive_PushButton, component.continuous_ActionParam)
        SFT.connect_widget_to_param(self.StopLive_PushButton, component.interrupt_ActionParam)
        SFT.connect_widget_to_param(self.StopSeries_PushButton, component.interrupt_ActionParam)

        self.Settings_PushButton.clicked.connect(self._on_open_settings)
        self.StartSeries_PushButton.clicked.connect(self._on_start_series_clicked)

        component.x_label.sigValueChanged.connect(self._on_xlabel_changed)
        component.y_scale.sigValueChanged.connect(self._on_yscale_changed)
        component.intensity_counts.sigValueChanged.connect(self._update_plot_single)
        component.intensity_counts_series.sigValueChanged.connect(self._update_plot_series)
        component.measurement_running.sigValueChanged.connect(self._on_measurement_running_changed)
        component.completed_measurement_steps.sigValueChanged.connect(self._on_progress_changed)
        component.series_ActionParam.sigActivated.connect(self._clear_plot)
        component.single_ActionParam.sigActivated.connect(self._clear_plot)
        component.continuous_ActionParam.sigActivated.connect(self._clear_plot)

        self._live_curve_count = 1    # 1 for the placeholder from setup_plot

        self._run_start_time = None
        self._eta_seconds_remaining = None
        self._eta_timer = QtCore.QTimer(self)
        self._eta_timer.setInterval(1000)
        self._eta_timer.timeout.connect(self._tick_eta)


    def setup_plot(self):
        self.plot_widget.clear()
        self.plot_widget.setLabel("left", "Intensity", units="arb. unit")
        self.plot_widget.setLabel("bottom", "Energy", units="eV")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().layout.setContentsMargins(10, 0, 0, 20)

        self.spectrum_plotDataItem = self.plot_widget.plot([], [])

        self.legend = self.plot_widget.addLegend(offset=(10, 10), labelTextSize='7pt')


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
    def _update_plot_single(self):
        Y = self.component.intensity_counts.value().flatten()
        X = self._x_data()
        if self._live_curve_count == 0:
            self.spectrum_plotDataItem = self.plot_widget.plot(X, Y)
            self._live_curve_count = 1
        else:
            self.spectrum_plotDataItem.setData(x=X, y=Y)


    @QtCore.Slot()
    def _update_plot_series(self):
        n = self.component.n_measurements.value()
        i = self.component.current_angle_index.value()
        color = _scheme_color(i / max(n - 1, 1), self.component.colorscheme.value())
        current_angles = self.component.current_angles.value()
        if current_angles is not None and i < len(current_angles):
            angle = current_angles[i]
        else:
            angle = self.component.ps_start.value() + i * self.component.ps_step.value()

        Y = self.component.intensity_counts_series.value().flatten()
        self.spectrum_plotDataItem = self.plot_widget.plot(self._x_data(), Y, pen=color)
        self.spectrum_plotDataItem.setZValue(i)
        self.legend.addItem(self.spectrum_plotDataItem, name=f"{angle:.1f}°")
        self._live_curve_count += 1


    @QtCore.Slot()
    def _clear_plot(self):
        self.plot_widget.clear()
        self.legend.clear()
        self._live_curve_count = 0


    @QtCore.Slot()
    def _on_start_series_clicked(self):
        if not self.component.is_shutter_open():
            reply = QtWidgets.QMessageBox.question(
                self, "Shutter closed", "Shutter closed. Continue?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply != QtWidgets.QMessageBox.StandardButton.Yes:
                return
        self.component.series_ActionParam.activate()


    @QtCore.Slot()
    def _on_open_settings(self):
        self._settings_dialog.show()
        self._settings_dialog.raise_()
        self._settings_dialog.activateWindow()
