from .module import DashboardModule
from .widget import DashboardView

DashboardModule.register_tab("Dashboard", DashboardView)

