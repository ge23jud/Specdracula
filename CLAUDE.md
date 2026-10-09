# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

SpecDracula is a PySide6/ScopeFoundry lab control application for optical spectroscopy at TUM (Technical University of Munich). It drives real hardware (CCD camera, spectrograph, piezo stage, lasers, power meter, shutter, motorized half-wave plate) and runs measurement routines (photoluminescence, power calibration, spotsize, 2D mapping, XY measurement) through a Qt UI.

## Running the app

```
python specdracula.py
```

Entry point: `specdracula.py`. It prepends `C:/WSI/turbo` to `sys.path` — this is a required sibling checkout of the `ScopeFoundry`/Turbo framework (imported as `ScopeFoundry`/`SFT`), not an installed package. There is no `requirements.txt`/`environment.yml` in this repo; the working Python environment is the conda/miniforge env `turbo-py312`.

There is no test suite, linter config, or build step in this repo.

## Architecture

### Two-tier component model

- **`HardwareComponents/`** — one subpackage per physical instrument (e.g. `andor_camera`, `andor_spec`, `piezo_jena_NV403CLE`, `thorlabs_laser`, `thorlabs_motors`, `thorlabs_powermeter`, `arduino_shutter`). Each follows a `*_hw.py` (ScopeFoundry `HardwareComponent`, defines Parameters, connect/disconnect) + `*_dev.py` (the actual device driver / serial/SDK calls) split, exported via `__init__.py`.
- **`MeasurementComponents/`** — one subpackage per measurement routine or UI panel (e.g. `Photoluminescence`, `PowerCalibration`, `Spotsize`, `Map`, `XYMeasurement`, `dashboard`, `status`). Each follows a `module.py` (ScopeFoundry `Measurement`, Parameters + measurement loop logic) + `widget.py` (Qt widget wiring) + `<Name>.ui` / `<name>_ui.py` (Qt Designer form and its compiled Python, kept in sync by hand) split.

`specdracula.py` (`SpecDracula(SFT.TurboControl)`) is the composition root: it instantiates every hardware component and measurement module in `setup()`, wires hardware instances into each measurement module's parameters (e.g. `photoluminescence.camera.setValue(ccd_camera)`), and builds dock widgets in `setup_ui()`.

### Power axis adapters (`power_axis_adapters.py`)

Power-series sweeps (Photoluminescence, PowerCalibration) can be driven by either the HWP rotation (angle-based, needs a log-calibration curve) or a laser's own closed-loop power setpoint. `PowerAxisAdapter` is the common interface (`set_setpoint`, `to_min`, `supports_log_calibration`, `unit`, `range`) so the sweep loops don't branch on which mechanism is active. `specdracula.py` swaps the active adapter on every consumer module when the dashboard's active-laser selector changes, and refuses to switch while a measurement is running.

### ScopeFoundry parameter conventions

- `PhysicalParameter` = hardware-backed (read/write funcs; `value()` returns the last hardware read).
- `ObjectParameter` = plain in-memory value; `value()` always reflects the UI.
- All hardware I/O must run on ScopeFoundry's thread pool via `WorkerTask` — never block the main/UI thread.
- Synchronous hardware reads use `trigger_read().wait(timeout)`, e.g. `pm.reading.trigger_read().wait(2.0)` then `pm.reading.value()`.
- Piezo position: `set_position_SI(axis, meters)` / `get_single_position_SI(axis)` (the getter polls until settled).
- The piezo driver uses a `device_mutex` (QMutex/QMutexLocker) around `__ask`/`__write`/`__read` to prevent concurrent access between polling tasks and WorkerTasks.
- The `status` module (`MeasurementComponents/status`) runs a continuous power-readout loop; other modules call `status.pause()`/`status.resume()` (typically in a `try/finally`) before taking exclusive control of the power meter.

### UI files — do not regenerate

`pyside6-uic` is broken in this environment (exits 255 even invoked via full path). **Never run it.** When a `.ui` file changes, update the corresponding `_ui.py` by hand, diffing the `.ui` XML against the existing generated Python (add/remove widget declarations and retranslate entries to match).

### Hardware SDK caution

Never add SDK method calls without first verifying they exist in the vendor SDK/library (e.g. `pyAndorSDK2` for the Andor CCD — `SetBadPixelCorrection` does not exist in it).

### File formats

`.origin` files (Origin plotting software import format) are written latin-1 encoded with CRLF line endings and a 9-line metadata header — see `helperfunctions.write_origin` / `helperfunctions.write_powercal_origin`.
