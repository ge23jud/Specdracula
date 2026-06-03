# SpecDracula — Agent Onboarding Instructions

## What is this project?

SpecDracula is a **PySide6 / ScopeFoundry Turbo** lab control application for optical photoluminescence (PL) spectroscopy at TUM. It controls an Andor CCD camera, an Andor spectrograph, a Thorlabs half-wave plate (HWP) rotation mount, a Piezo Jena NV40 stage, and a Thorlabs power meter — all from a single GUI.

The app is run by executing `specdracula.py` directly.

---

## Locations

| Item | Path |
|---|---|
| Repository root | `C:\WSI\specdracula` |
| GitHub | `https://github.com/ge23jud/Specdracula` (branch: `master`) |
| Python env | `C:\Users\NWPP\miniforge3\envs\turbo-py312` |
| ScopeFoundry Turbo source | `C:\WSI\turbo` (on `sys.path`) |
| Measurements saved to | `C:\Measurements\YYYYMMDD\` |

---

## Framework: ScopeFoundry Turbo

ScopeFoundry Turbo (SFT) is a custom fork of ScopeFoundry. Key concepts:

### Parameters

- **`SFT.ObjectParameter`** — plain in-memory value. `value()` always reflects the current state (UI or code). Use for settings, UI controls, calculated data.
- **`SFT.PhysicalParameter`** — hardware-backed. Has `read_func`/`write_func`. `value()` = last hardware read. To read: `param.trigger_read().wait(timeout)`. To write: `param.write_to_device(val)` (calls `write_func` on the hardware thread). `sigValueChanged` fires when the cached value changes.
- **`SFT.ActionParameter`** — a button. `sigActivated` fires when clicked.
- **`SFT.ChoiceRangeType`** — enum-style range for string parameters: `ChoiceRangeType(**{"Option A": 0, "Option B": 1})`.
- **`SFT.MinMaxRangeType`** — numeric range: `MinMaxRangeType(min=0, max=360, decimals=2)`.

### Threading

**Never block the main (UI) thread with hardware I/O.** All hardware work goes on `self.thread_pool` via `SFT.WorkerTask`. Measurement methods (like `powerseries`, `acquire_single`) run on worker threads — they are allowed to call hardware directly and to call `.wait()` on tasks.

Pattern for synchronous hardware reads from a worker thread:
```python
task = param.trigger_read()
task.wait(timeout=5.0)
result = task.result
```

### Connecting widgets to parameters

```python
SFT.connect_widget_to_param(self.MyWidget, component.my_param)
```

This creates a two-way binding. Works for `QDoubleSpinBox`, `QCheckBox`, `QComboBox`, `QPushButton` (ActionParam), `QLineEdit`.

### Module structure

Each measurement module has three files:
- `module.py` — `class FooModule(SFT.Module)`: all logic, parameters, WorkerTasks
- `widget.py` — `class FooView(TurboComponentView, Ui_FooWidget)`: connects widgets to params, handles plot updates
- `foo_ui.py` — generated from `foo.ui`; **edited by hand** (see below)
- `foo.ui` — Qt Designer XML; keep in sync with `foo_ui.py`

---

## Critical workflow rules

### 1. pyside6-uic is broken

`pyside6-uic.exe` exits with code 255 in this environment and produces no output. **Never run it.**

When a `.ui` file changes, **manually update the corresponding `_ui.py`** by diffing the XML:
- `setupUi`: add/remove widget construction and `addWidget`/`addLayout` calls
- `retranslateUi`: add/remove `.setText(...)`, `.setItemText(...)` etc.

Both `Photoluminescence.ui` and `photoluminescence_ui.py` must always be kept in sync.

### 2. Don't add non-existent SDK calls

`SetBadPixelCorrection` does NOT exist in pyAndorSDK2. Before adding any Andor SDK method call, verify it exists in the SDK. We had to revert a commit because of this.

### 3. Commit at the start of each session

Before doing any new work, check for uncommitted changes (`git status`), review them, and commit the relevant source files. Exclude: `__pycache__/`, `spotsize.txt`, lab data files (`.origin`, `testdata/`, `plot.png`, etc.).

### 4. File format

Saved data files use `.origin` format: Latin-1 encoding, CRLF line endings, 9-line metadata header. See `helperfunctions.py` → `write_origin()` and `write_powercal_origin()`.

---

## Hardware modules

### Andor CCD (`HardwareComponents/andor_camera/andor_ccd_hw.py`)

- `cam.exposure` — integration time (PhysicalParameter, seconds)
- `cam.acc_cycle_time` — actual cycle time including readout (PhysicalParameter)
- `cam.trigger_acquisition()` — triggers acquisition; returns a task. Wait with `task.wait(acc_cycle_time + extra_timeout)`.
- `cam.acquire_wait.result[0]` — the acquired counts array after waiting

### Andor Spectrograph (`HardwareComponents/andor_spec/andor_spec_hw.py`)

- `spec.center_wavelength` — PhysicalParameter, **in meters**. Read with `.value() * 1e9` to get nm. Write with `.write_to_device(λ_m)`.
- `spec.center_energy` — PhysicalParameter, **in eV**. Write: `.write_to_device(E_eV)` → internally calls `center_wavelength.write_to_device`.
- `spec.wavelength_calib` — PhysicalParameter, ndarray of nm values (one per pixel, ascending). Auto-triggered when `center_wavelength` changes.
- `spec.entrance_slit_direct` — PhysicalParameter, **in meters**. Read with `.value() * 1e3` for mm.
- `spec.detector_pixels` — 512 (default)
- When you move `center_wavelength`, call `spec.wavelength_calib.trigger_read().wait(5.0)` afterward to ensure the calibration is updated before reading it.
- `spec.center_wavelength.trigger_read().wait(30.0)` — 30s timeout because physical grating movement can be slow.

### Piezo Jena NV40 (`HardwareComponents/piezo_jena_NV403CLE/piezo_jena_hw.py`)

- Serial via pyvisa. **`self.device_mutex` (QMutex) guards all serial comms** — use `QMutexLocker(self.device_mutex)` in every `__ask`/`__write`/`__read` call to prevent concurrent access.
- `set_position_SI(axis, meters)` — move to position, polls until settled
- `get_single_position_SI(axis)` — read current position

### Thorlabs Power Meter

- `pm.reading` — PhysicalParameter (Watts)
- Pattern: `pm.reading.trigger_read()` then `pm.reading.value()` (or `.wait(2.0)` for synchronous read)
- Reading is in Watts; multiply by `1e3` for mW, `1e6` for µW.

### Thorlabs HWP Motor

- `hwp.write_angle(degrees)` — synchronous, blocks until motor reaches position
- Used to control excitation power via a half-wave plate + PBS combination

---

## Measurement modules

### StatusModule (`MeasurementComponents/status/`)

Runs a continuous power readout loop. Other modules must call `status.pause()` before using the power meter and `status.resume()` afterward. Always wrap in `try/finally`.

### DashboardModule (`MeasurementComponents/dashboard/`)

Piezo XY control (PhysicalParameters, µm, wired to `set/get_position_SI` with ×1e-6). Four directional step buttons. `piezo_step` as ObjectParameter. Also shows HWP and spectrograph center wavelength/energy.

### MapModule (`MeasurementComponents/Map/`)

2D piezo sweep with live ImageView. `pg.TargetItem` drags to move piezo.

### SpotsizeModule (`MeasurementComponents/Spotsize/`)

Measures laser spot size by scanning the piezo across a knife edge while recording power.

### PowerCalibrationModule (`MeasurementComponents/PowerCalibration/`)

HWP angle sweep while recording power meter readings. Produces a power calibration curve saved as `.origin`.

### PhotoluminescenceModule (`MeasurementComponents/Photoluminescence/`) ← most active

See full details below.

---

## PhotoluminescenceModule — detailed

This is the most recently developed and most complex module. Everything below reflects the current state of `master`.

### Parameters (class-level)

| Parameter | Type | Description |
|---|---|---|
| `camera`, `spectrograph`, `hwp`, `powermeter`, `status` | ObjectParameter (TurboComponent) | Device references |
| `x_label` | str, ChoiceRangeType | "Energy" (default) or "Wavelength" |
| `y_scale` | str, ChoiceRangeType | "Linear" or "Logarithmic" |
| `ps_start/stop/step` | float, °  | HWP sweep range for power series |
| `n_measurements` | int, readonly | Auto-computed from start/stop/step |
| `extra_timeout` | float, s | Added to `acc_cycle_time` for acquisition wait |
| `wavelength_nm` | ndarray, readonly | Current wavelength calibration (nm, ascending) |
| `energy_ev` | ndarray, readonly | Derived from `wavelength_nm` |
| `intensity_counts` | ndarray, readonly | Live single-spectrum data |
| `intensity_counts_powerseries` | ndarray, readonly | Latest spectrum in powerseries (triggers plot update) |
| `intensity_counts_powerseries_complete` | ndarray, readonly | Full (n × pixels) matrix for current stitch |
| `stitch_edge_nm` | ndarray, readonly | [wl[0], wl[-1]] of most recently completed bandwidth stitch |
| `measurement_running` | bool, readonly | True while powerseries is executing |
| `powers` | ndarray | Power readings per HWP step |
| `repetitions` | int | Exposures per HWP step |
| `averaging` | bool | Average repetitions or stack them |
| `pixel_correction_enabled` | bool | Apply pixel correction from `pixel_correction_2.txt` |
| `colorscheme` | str, ChoiceRangeType | One of: Viridis, Spectral, CoolWarm, Warm, Turbo |
| `bs_enable` | bool | Enable bandwidth sweep mode |
| `bs_min_energy` | float, eV | Low-energy boundary of desired sweep range |
| `bs_max_energy` | float, eV | High-energy boundary |
| `bs_overlap` | float, eV | Energy overlap between adjacent stitches |
| `save_directory` | str | Save path (auto-created if missing) |
| `save_filename` | str | Base filename (prefixed with 3-digit auto-increment) |

### Pixel correction

Loaded from `pixel_correction_2.txt` (512 values, energy order). **Reversed at init** so it's in wavelength/pixel order. Applied as `counts / correction` when `pixel_correction_enabled = True`.

### Powerseries flow

```
powerseries()                      ← runs on WorkerTask thread
  measurement_running = True
  status.pause()
  _powerseries()
    if bs_enable → _bandwidth_sweep_powerseries()
    else         → _single_powerseries()
  status.resume()
  measurement_running = False
```

**`_single_powerseries()`**: Sweeps HWP from `ps_start` to `ps_stop` in `ps_step` increments. For each step: moves HWP, acquires spectrum, reads power. Saves one `.origin` file via `HelperFunctions().write_origin(...)`. File number auto-increments.

**`_bandwidth_sweep_powerseries()`**: Moves spectrograph to multiple center wavelengths and calls `_single_powerseries()` at each one. Each stitch gets its own `.origin` file (auto-numbered). After each stitch, sets `stitch_edge_nm = [wl[0], wl[-1]]`.

### Bandwidth sweep algorithm

The spectrograph window width **in nm is constant** for a given grating. Window width in eV varies with center energy (nonlinear E = hc/λ). The algorithm:

1. Get `W_nm = wl[-1] - wl[0]` from current calibration
2. Compute center energies using exact closed-form formulas:
   - `upper_edge_ev(E_c) = HC / (HC/E_c − W_nm/2)` where `HC = 1239.84193 eV·nm`
   - `lower_edge_ev(E_c) = HC / (HC/E_c + W_nm/2)`
   - `center_from_upper_ev(E_upper) = HC / (HC/E_upper + W_nm/2)`
3. Two-pass greedy placement (high → low energy):
   - Pass 1: upper edge of window 0 = E_max → find N centers until lower edge ≤ E_min
   - Compute `excess_per_side = (E_min - bottom) / 2`
   - Pass 2: upper edge = E_max + excess_per_side → redo, distributing excess equally
4. Move spectrograph: `spec.center_wavelength.write_to_device(HC_eV_m / E_center)`
5. Then: `spec.center_wavelength.trigger_read().wait(30.0)` and `spec.wavelength_calib.trigger_read().wait(5.0)`

### Plot / view features

- **x-axis**: Energy (eV) by default. Toggle to Wavelength (nm).
- **Colors**: mapped to HWP position via `_scheme_color(t, scheme)` where `t = i/(n-1)`, `i` = within-stitch HWP index. Five schemes with smooth RGB interpolation.
- **z-ordering**: `setZValue(i)` on each curve — same HWP index = same z-level across all stitches.
- **Legend**: `pg.LegendItem` at top-left (7pt), shows angle per color. Populated only on first stitch to avoid duplicates.
- **Stitch boundary lines**: Gray dashed `pg.InfiniteLine`s at each stitch's wavelength/energy edges. Repositioned correctly on x-axis switch. Stored as `(wl[0], wl[-1])` in nm and converted on demand.
- **Status label**: QLabel above the plot, right-aligned. "Running..." (orange) during measurement; "Finished" (bright green) when done. Driven by `measurement_running` parameter.

---

## helperfunctions.py

Key utilities:

```python
hf = HelperFunctions()
hf.wavelength_energy_converter(array_nm)  # nm → eV using scipy constants
hf.get_next_file_number(directory)        # returns zero-padded 3-digit string e.g. "007"
hf.write_origin(...)                       # write PL powerseries .origin file
hf.write_powercal_origin(...)              # write power calibration .origin file
```

Energy conversion: `E_eV = h*c / (λ_nm * 1e-9) / e` (scipy constants).

For **reverse conversion** (eV → nm or m): use `_HC_EV_NM = 1239.84193` eV·nm → `λ_nm = 1239.84193 / E_eV`.

The spectrograph's internal `set_center_energy` uses slightly different constants (`h=4.1457e-15 eV·s, c=2.9979e8 m/s`) — this gives `HC = 1242.7 eV·nm`, a ~0.2% discrepancy vs scipy. Negligible in practice.

---

## UI files — conventions

Every module has:
- `SomeName.ui` — Qt Designer XML (source of truth for layout intent)
- `somename_ui.py` — Python translation (maintained manually since pyside6-uic is broken)

**When adding a widget:**
1. Add it to `SomeName.ui` with proper XML
2. Mirror it in `somename_ui.py` in `setupUi()` (widget construction + `addWidget`) and `retranslateUi()` (text labels)
3. Wire it in `widget.py` with `SFT.connect_widget_to_param(...)`

**Widget naming convention**: `WidgetName_WidgetType`, e.g. `PsStart_DoubleSpinBox`, `BandwidthSweepEnable_CheckBox`, `ColorScheme_ComboBox`, `Status_Label`.

**pyqtgraph items** (legend, InfiniteLine, TextItem) cannot be defined in `.ui` files — they are created programmatically in `widget.py`'s `setup_plot()`.

---

## Things that will bite you

- **`spec.center_wavelength` is in meters**, not nm. Always multiply by `1e9` for display.
- **`spec.entrance_slit_direct` is in meters**. Multiply by `1e3` for mm.
- **`pm.reading` is in Watts**. Multiply by `1e3` for mW.
- `wavelength_calib` array is **ascending** (wl[0] = short λ = high E, wl[-1] = long λ = low E). `dispersion_window = wavelength[-1] - wavelength[0]` is positive.
- `energy_ev` array is **descending** (derived from ascending wavelength). pyqtgraph plots it left-to-right as high-E to low-E.
- `QMutex`/`QMutexLocker` is required in piezo serial comms to prevent concurrent access from polling tasks and WorkerTasks.
- `SFT.connect_widget_to_param` for a `QComboBox` connected to a `ChoiceRangeType` parameter: combobox item texts must match the ChoiceRangeType keys exactly.
- After `plot_widget.clear()`, InfiniteLines added via `addItem` are removed, but the `LegendItem` (child of ViewBox) is NOT. Call `legend.clear()` separately.
- `measurement_running` is set to `False` in the `finally` block of `powerseries()` — so it resets even on interruption or exception.
- The `_interrupted` flag is set by `interrupt_ActionParam` and must be checked in measurement loops. It is reset to `False` at the end of `acquire_single` and `acquire_continuous`.

---

## Hardware serial numbers / ports (as configured in specdracula.py)

| Device | Config |
|---|---|
| Power meter | `ASRL19::INSTR` |
| HWP motor | Serial `27253212` (KDC101) |
| Piezo stage | `ASRL12::INSTR` |
| Andor CCD | auto-detected |
| Andor Spectrograph | device ID `"0"` |

---

## Branch / workflow note

This project has at least two people working on it simultaneously on separate branches. Always check what branch you're on before starting. Pull before working. The main branch is `master`. Commit only source files — never `__pycache__/`, `*.pyc`, `spotsize.txt`, `*.origin`, `testdata/`, `plot.png`, `*.txt` lab notes.

---

## Quick reference: common patterns

```python
# Synchronous hardware read (from worker thread)
task = param.trigger_read()
task.wait(timeout=5.0)
value = task.result  # or param.value()

# Power meter read
pm.reading.trigger_read()
power_w = pm.reading.value()

# Move spectrograph to energy E_eV
λ_m = 1239.84193 / E_eV * 1e-9
spec.center_wavelength.write_to_device(λ_m)
spec.center_wavelength.trigger_read().wait(30.0)   # grating movement can be slow
spec.wavelength_calib.trigger_read().wait(5.0)

# Status pause/resume (ALWAYS use try/finally)
status = self.status.value()
if status is not None:
    status.pause()
try:
    # ... do hardware work ...
finally:
    if status is not None:
        status.resume()

# Save a file (auto-increments 3-digit prefix)
filepath = self.update_save_string()   # returns e.g. "C:\Measurements\...\007_myfile.origin"
HelperFunctions().write_origin(..., filepath)
```
