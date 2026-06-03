# SpecDracula — Answers for Mac Simulation Branch

---

## Environment Details

### 1. Exact start command
```
C:\Users\NWPP\miniforge3\envs\turbo-py312\python.exe C:\WSI\specdracula\specdracula.py
```
Run from any working directory; `specdracula.py` uses absolute paths throughout.

### 2. Active git branch on lab PC
```
master  (tracking origin/master, fully up to date after last push)
```

### 3. Python version
```
Python 3.12.12
```

### 4. Python executable path
```
C:\Users\NWPP\miniforge3\envs\turbo-py312\python.exe
```
(Miniforge3, not Anaconda. The env is named `turbo-py312`.)

### 5. Conda env name
```
turbo-py312
```
Located at `C:\Users\NWPP\miniforge3\envs\turbo-py312`.

### 6. Is `C:\WSI\turbo` always present?
**Yes.** `C:\WSI\` is a workspace root that contains:
```
C:\WSI\
  turbo\        ← ScopeFoundry Turbo source (package root)
  specdracula\  ← the specdracula git repo
  netdrive\
  test\
```
`specdracula.py` does `sys.path.insert(0, 'C:/WSI/turbo')` so that `import ScopeFoundry as SFT` resolves to `C:\WSI\turbo\ScopeFoundry\`. If `C:\WSI\turbo` is missing, the app fails to import on the first line.

### 7. Is `C:\WSI\turbo` a git checkout?
**No.** It is NOT a git repository — `git status` inside it returns `fatal: not a git repository`. It appears to have been set up with `python setup.py develop` (a `ScopeFoundry.egg-info\` directory is present) but was not cloned. The CHANGELOG inside begins with:
```
ScopeFoundry 1.1.1 2018-08-14
```
This is a **custom / internal ScopeFoundry Turbo fork**, not upstream ScopeFoundry. Its version/commit is not tracked by git. For the Mac simulation branch, the coworker will need to either obtain this same source tree or stub out the relevant SFT imports.

### 8. Installed package versions (full `pip freeze` from `turbo-py312`)
```
cffi==2.0.0
contourpy==1.3.1
cycler==0.12.1
fonttools==4.63.0
h5py (conda build)
Jinja2==3.1.6
kiwisolver==1.5.0
llvmlite==0.45.1
MarkupSafe==3.0.3
matplotlib==3.10.9
numba==0.62.1
numpy==2.3.4
packaging==25.0
pandas (conda build)
pillow==12.2.0
plumbum==1.9.0
pyAndorSDK2==1.2.0         ← editable, C:\Program Files\Andor SDK\Python\pyAndorSDK2
pyAndorSpectrograph==1.2.0 ← editable, C:\Program Files\Andor SDK\Python\pyAndorSpectrograph
pycparser==2.23
pyft232==0.12
pylablib==1.4.4
pyparsing==3.3.2
pyqt-darktheme==1.3.1
PyQt5==5.15.11
pyqtgraph (conda build, ~0.13)
pyserial (conda build)
PySide6==6.9.0
python-dateutil (conda build)
pytz (conda build)
pyusb (conda build)
PyVISA (conda build)
PyVISA-py (conda build)
pywin32==311
QDarkStyle==3.2.3
qt-material==2.17
QtPy==2.4.3
rpyc==6.0.2
scipy==1.16.2
setuptools==80.9.0
shiboken6==6.9.0
six (conda build)
typing_extensions (conda build)
wheel==0.45.1
```

**Critical for simulation stub:** `PySide6==6.9.0`, `pyqtgraph` (conda build ~0.13), `ScopeFoundry` (from `C:\WSI\turbo`, not in pip). `pyAndorSDK2` and `pyAndorSpectrograph` are Windows-only editable installs — these are what need to be stubbed on Mac. `pyvisa`/`pyvisa-py` handle serial for piezo and power meter. `pylablib` handles the Thorlabs KDC101 motor.

---

## Real Hardware Compatibility

### 1. Does master launch with real hardware without local edits?
**Yes.** The lab PC is on `master`, fully synced with GitHub. The only uncommitted changes are `__pycache__/` bytecode and `spotsize.txt` (runtime output), both of which are irrelevant to startup. Source files are clean.

### 2. Devices connected and expected at startup
All five are connected and `connect()` is called unconditionally in `setup()`:
1. **Thorlabs PM100 power meter** — connects via PyVISA serial
2. **Thorlabs KDC101 HWP motor** — connects via pylablib
3. **Piezo Jena NV40** — connects via PyVISA serial
4. **Andor CCD camera** — connects via pyAndorSDK2
5. **Andor Spectrograph** — connects via pyAndorSpectrograph

### 3. Are the configured identifiers still correct?
**Yes, all confirmed from current `specdracula.py` on master:**
| Device | Identifier |
|---|---|
| Powermeter | `ASRL19::INSTR` |
| HWP KDC101 serial | `27253212` |
| Piezo | `ASRL12::INSTR` |
| Andor spectrograph device ID | `"0"` |

### 4. Temperature readout and laser shutter — intentionally not connected?
**Yes, both are intentionally inactive:**
- **Temperature**: `temperature = 0` is hardcoded in `_single_powerseries()` and `_save_single()` with a `# to implement` comment. No hardware temperature sensor is wired up.
- **Shutter**: The `ArduinoShutterHW` block in `setup()` is fully commented out (`# shutter = ArduinoShutterHW(...)`). No shutter object is created or connected. The import exists but is unused.

### 5. Any uncommitted lab-PC source changes not on GitHub?
**No.** `git status --short --branch` shows only:
- Modified `__pycache__/*.pyc` files (bytecode, not tracked)
- Modified `spotsize.txt` (runtime output, not tracked)
- Untracked: `testdata/`, `pixel_correction_2.txt`, `powercalibration_atBS__000.origin`, and a few personal notes (`.txt`, `make_plot.py`, `plot.png`)

All source `.py`, `.ui`, and `_ui.py` files are clean and match GitHub.

---

## UI / Layout

### 1. Expected normal lab UI layout
The app uses **`qt-material` dark_purple theme** (`apply_stylesheet(app, theme="dark_purple.xml")`). Layout:

- **Left sidebar**: Standard ScopeFoundry Turbo module list — shows all registered modules (Photoluminescence, Dashboard, 2D Map, Spotsize, Power Calibration, XYMeasurement, Status). Double-clicking opens/focuses the module tab.
- **Main MDI area**: Module views open as tabs here. At startup it is empty until a module tab is opened.
- **Right docks** (two stacked):
  - **"Hardware Control" dock** (top-right): `DashboardView` — piezo XY control, directional step buttons, HWP/spectrograph readouts.
  - **"Status" dock** (below Hardware Control, fixed 240px height): `StatusView` — live power readout + temperature. No title bar (hidden via `setTitleBarWidget(QWidget())`).

### 2. DashboardModule — where does it appear?
**Right dock only** ("Hardware Control"), created in `create_dashboard_dock()`. It is also a registered module in the left sidebar list, but its primary UI is the dock. The dock is added to `Qt.RightDockWidgetArea`.

### 3. StatusModule — where does it appear?
**Right dock only** ("Status"), created in `create_status_display_dock()`, stacked below the Dashboard dock on the right side. Fixed height 240px, minimum width 300px. Also appears in the left sidebar module list. The power and temperature labels are styled white-on-dark, 30pt font.

---

## Data / Simulation

### 1. Best reference files for normal PL/stitch behavior
`C:\WSI\specdracula\testdata\` contains five bandwidth-sweep stitches of sample `spl2625`:
```
000_spl2625_1.45eV_stich.origin
001_spl2625_1.35eV_stich.origin
002_spl2625_1.25eV_stich.origin
003_spl2625_1.15eV_stich.origin
004_spl2625_1.55eV_stich.origin
```
These cover ~1.15–1.55 eV in overlapping stitches and are the best existing reference for the `.origin` file format and stitch data layout.

### 2. Which files show clear lasing peaks?
Unknown from code inspection alone — this depends on the physical measurement. The `spl2625` files above are the only available testdata; whether they show lasing peaks would need to be checked by opening them. No other data files are in the repo.

### 3. Dark files for simulated background?
There are no dedicated dark/background files in the repo. The `pixel_correction_2.txt` file in `MeasurementComponents/Photoluminescence/` (512 float values, energy order, reversed at load) is the only correction data. For simulation purposes this file can be used directly — it is already in the repo and loaded unconditionally at module init.

### 4. Are `.origin`, map `.txt`, and spotsize `.txt` files safe to include as fixtures?
- **`.origin` files** in `testdata/`: safe to parse as local fixtures. The format is documented in `helperfunctions.py → write_origin()`. Latin-1 encoding, CRLF line endings, 9-line tab-delimited header.
- **`spotsize.txt`**: runtime output, changes every run, should stay outside git (already in `.gitignore` behavior — it shows as modified).
- **Map `.txt` files**: not present in the repo currently.
- **Recommendation**: keep `testdata/` out of git (or add it to `.gitignore`) and provide it as a separate download, OR commit only the `testdata/` `.origin` files since they are small and fixed reference data. Do not commit personal lab output files (`powercalibration_atBS__000.origin` etc.).

---

## Branch Coordination — Risk Flags

The `codex/workspace-setup` branch with simulated hardware, Mac startup path, and ignored `Data_examples/`+`turbo/` is a sound approach. Before merging, watch for these specific risks to the real hardware path:

### 🔴 High risk

1. **`sys.path.insert(0, 'C:/WSI/turbo')`** — This line in `specdracula.py` is load-bearing on the lab PC. If the Mac branch introduces a platform check that removes or skips it on non-Windows, ScopeFoundry will fail to import on Windows unless turbo is installed another way. Safest pattern:
   ```python
   import sys, os
   if os.path.isdir('C:/WSI/turbo'):
       sys.path.insert(0, 'C:/WSI/turbo')
   ```

2. **Hardware `connect()` calls in `setup()`** — Currently all five devices call `.connect()` unconditionally. On Mac without real hardware, this will crash. The Mac branch needs a simulation flag that skips or replaces these calls. This flag must NOT affect the lab PC path. Recommended: environment variable `SPECDRACULA_SIM=1` or a CLI argument, NOT a hardcoded hostname/platform check.

3. **`pyAndorSDK2` and `pyAndorSpectrograph`** — These are installed from `C:\Program Files\Andor SDK\...` and are Windows-only. The Mac simulation stubs for `AndorCCDHW` and `AndorSpectrographHW` must be importable without these packages. Use conditional imports at the hardware module level, not at the top of `specdracula.py`.

### 🟡 Medium risk

4. **`pywin32==311`** — Several Windows-only features. Check that none of the hardware modules import it directly (the lab PC pip freeze shows it's installed; it's pulled in by pyqtgraph/PySide6 on Windows).

5. **`pylablib`** — Used for the Thorlabs KDC101 motor. Mac stubs must replace `ThorlabsKDC101_PRMTZ8`. `pylablib` itself is cross-platform so it can be installed on Mac, but actual USB communication will fail without the device.

6. **PyVISA backends** — `pyvisa-py` is installed (pure-Python backend). On Mac, VISA instruments (powermeter, piezo) won't connect but won't crash at import. The crash happens at `rm.open_resource(port)`. Stubs need to mock at the ResourceManager level.

7. **`qt-material` theme file** — `apply_stylesheet(app, theme="dark_purple.xml")` — qt-material is cross-platform, this should work on Mac as-is.

### 🟢 Safe / no risk

- All `MeasurementComponents/` Python source (module.py, widget.py, _ui.py) is pure PySide6/pyqtgraph and fully cross-platform.
- `helperfunctions.py` is pure Python/numpy/scipy — safe.
- `.ui` and `_ui.py` files are platform-neutral.
- The `.origin` file format (latin-1, CRLF) works on Mac if opened with `newline="\r\n"` as already coded.
- `pixel_correction_2.txt` and data files are platform-neutral.

### Recommended merge strategy
1. Keep `specdracula.py` as the single entry point but accept an env var `SPECDRACULA_SIM=1`.
2. Create `specdracula_sim.py` (or a `--sim` CLI flag) that swaps hardware classes for stubs — don't touch the real hardware class files.
3. Stub files should live in a `SimulatedHardware/` directory not imported on real hardware.
4. Add `SPECDRACULA_SIM`, `Data_examples/`, and Mac-specific files to `.gitignore` rather than committing them, until the simulation path is stable.
5. The real `setup()` in `specdracula.py` should remain unchanged.
