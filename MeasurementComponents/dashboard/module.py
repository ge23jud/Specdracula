from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module, ObjectParameter

class DashboardModule(Module):

    center_wavelength = SFT.PhysicalParameter(
        "Center Wavelength",
        dtype=float,
        value=1050,
        unit="nm"
    )
    
    center_energy = SFT.PhysicalParameter(
        "Center Energy",
        dtype=float,
        value=1.2,
        unit="eV"
    )

    integration_time = SFT.PhysicalParameter(
        "Integration Time",
        dtype=float,
        value=1.,
        unit="s"
    )

    piezo_x = SFT.PhysicalParameter(
        "Piezo X",
        dtype=float,
        value=0.,
        unit="um"
    )

    piezo_y = SFT.PhysicalParameter(
        "Piezo Y",
        dtype=float,
        value=0.,
        unit="um"
    )

    piezo_step = SFT.PhysicalParameter(
        "Piezo Step",
        dtype=float,
        value=0.1,
        unit="um"
    )

    hwp_position = SFT.PhysicalParameter(
        "HWP Position",
        dtype=float,
        value=45.,
        unit="°"
    )