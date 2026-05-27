from PySide6 import QtCore

import ScopeFoundry as SFT
from ScopeFoundry import Module


class StatusModule(Module):

    powermeter = SFT.ObjectParameter('Powermeter', SFT.TurboComponent)
    power = SFT.ObjectParameter('Power', dtype=float, value=0.0, unit='W', readonly=True)

    start_ActionParam = SFT.ActionParameter('Start')
    stop_ActionParam = SFT.ActionParameter('Stop')

    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self._running = False
        self._resume_after = False
        self.task_monitor = SFT.WorkerTask("Monitor Power", self._monitor_loop, default_thread_pool=self.thread_pool)
        self.start_ActionParam.sigActivated.connect(lambda: self.task_monitor.run_on_pool())
        self.stop_ActionParam.sigActivated.connect(self._stop)

    @QtCore.Slot()
    def _stop(self):
        self._running = False

    def pause(self):
        self._resume_after = self._running
        self._running = False

    def resume(self):
        if self._resume_after:
            self._resume_after = False
            self.task_monitor.run_on_pool()

    def _monitor_loop(self):
        self._running = True
        pm = self.powermeter.value()
        while self._running:
            pm.reading.trigger_read().wait(2.0)
            self.power.setValue(pm.reading.value())
