# Prompt For Coworker's Claude Agent

We are adding a Mac development/simulation path to `ge23jud/Specdracula` while preserving the real lab Windows setup. Please answer the questions below as concretely as possible, ideally with exact command output where relevant.

## Environment Details Needed

1. What exact command does the coworker use to start Specdracula on the lab PC?
2. What is the active Git branch on the lab PC?
3. What Python version is used in the lab environment?
   - Please run: `python --version`
4. What Python executable path is used?
   - Please run: `where python`
5. What Conda/env name is used?
   - Please run: `conda info --envs`
6. Is `C:\WSI\turbo` always present on the lab PC?
7. Is `C:\WSI\turbo` itself a Git checkout? If yes, what branch/commit?
   - Please run inside `C:\WSI\turbo`: `git status --short --branch` and `git log --oneline -3`
8. Which installed package versions matter for the app?
   - Please run in the active env: `python -m pip freeze`

## Real Hardware Compatibility Questions

1. Does the current app launch with real hardware from `master` without local edits?
2. Which real devices are currently connected and expected to connect at startup?
3. Are these still the correct configured identifiers?
   - Powermeter: `ASRL19::INSTR`
   - HWP KDC101 serial: `27253212`
   - Piezo: `ASRL12::INSTR`
   - Andor spectrograph device ID: `0`
4. Are the temperature readout and laser shutter intentionally not connected yet?
5. Are there any local uncommitted lab-PC changes that are not on GitHub?
   - Please run in Specdracula: `git status --short --branch`

## UI/Layout Questions

1. Please describe the expected normal lab UI layout.
   - Left sidebar?
   - Empty MDI workspace at startup?
   - Where should hardware controls/status/power appear?
2. Does `DashboardModule` normally appear as a module in the left sidebar, a dock on the right, or both?
3. Does `StatusModule` normally appear as a module in the left sidebar, a dock on the right, or both?

## Data/Simulation Questions

1. Which example files are the best references for normal PL/stitch behavior?
2. Which example files show clear lasing peaks?
3. Which dark files correspond to each exposure time and should be used for simulated dark/background data?
4. Are `.origin`, map `.txt`, and spotsize `.txt` files safe to parse as local fixtures, or should they remain completely outside Git?

## Branch Coordination

We currently have a local branch `codex/workspace-setup` on the Mac with:

- local setup docs
- simulated hardware classes
- Mac simulation startup
- ignored local `Data_examples/` and `turbo/`

Before merging or pushing this branch, please flag any changes that could risk the real hardware startup path.
