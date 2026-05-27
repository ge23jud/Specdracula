from PySide6 import QtCore
import ScopeFoundry as SFT
import pyqtgraph as pg
import numpy as np
from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .Map_ui import Ui_MapWidget


class MapView(TurboComponentView, Ui_MapWidget):
    def __init__(self, component, parent=None):
        TurboComponentView.__init__(self, component, parent=parent)
        self.setupUi(self)

        self.replace_imageview_with_plotitem()
        self.setup_2d_plot()

        SFT.connect_widget_to_param(self.Directory_LineEdit, component.save_directory)
        SFT.connect_widget_to_param(self.Filename_LineEdit, component.save_filename)
        SFT.connect_widget_to_param(self.XStart_DoubleSpinBox, component.x_start)
        SFT.connect_widget_to_param(self.XStop_DoubleSpinBox, component.x_stop)
        SFT.connect_widget_to_param(self.XStep_DoubleSpinBox, component.x_step)
        SFT.connect_widget_to_param(self.YStart_DoubleSpinBox, component.y_start)
        SFT.connect_widget_to_param(self.YStop_DoubleSpinBox, component.y_stop)
        SFT.connect_widget_to_param(self.YStep_DoubleSpinBox, component.y_step)
        SFT.connect_widget_to_param(self.Start_Button, component.run_ActionParam)
        SFT.connect_widget_to_param(self.Stop_Button, component.interrupt_ActionParam)

        component.n_measurements.sigValueChanged.connect(self.update_nummeasurements_label)
        component.x_start.sigValueChanged.connect(self.update_roi)
        component.y_start.sigValueChanged.connect(self.update_roi)
        component.x_stop.sigValueChanged.connect(self.update_roi)
        component.y_stop.sigValueChanged.connect(self.update_roi)
        component.map_data.sigValueChanged.connect(self._update_map)
        self.roi.sigRegionChangeFinished.connect(self._on_roi_changed)
        self.target.sigPositionChangeFinished.connect(self._on_target_moved)

        self.update_nummeasurements_label()

    def update_nummeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))

    def replace_imageview_with_plotitem(self):
        parent = self.img_view.parent()
        layout = parent.layout()
        index = layout.indexOf(self.img_view)
        layout.removeWidget(self.img_view)
        self.img_view.deleteLater()
        self.img_view = pg.ImageView(view=pg.PlotItem())
        layout.insertWidget(index, self.img_view)

    def setup_2d_plot(self):
        self.plot_item = self.img_view.getView()
        self.plot_item.setLabel("bottom", "X", units="m")
        self.plot_item.setLabel("left", "Y", units="m")
        self.plot_item.showGrid(x=True, y=True, alpha=0.2)
        self.plot_item.setRange(xRange=(-100e-6, 100e-6), yRange=(-70e-6, 70e-6))
        self.plot_item.enableAutoRange(enable=False)

        self.target = pg.TargetItem()
        self.plot_item.addItem(self.target)
        self.target.setZValue(2)

        self.roi = pg.ROI(pos=(0, 0), size=(40e-6, 40e-6), resizable=True, rotatable=False, translateSnap=True, snapSize=10e-9)
        self.roi.addScaleHandle(pos=(1, 1), center=(0, 0))
        self.plot_item.addItem(self.roi)
        self.roi.setZValue(1)

    @QtCore.Slot()
    def _on_roi_changed(self):
        pos = self.roi.pos()
        size = self.roi.size()
        self.component.x_start.setValue(pos.x())
        self.component.x_stop.setValue(pos.x() + size.x())
        self.component.y_start.setValue(pos.y())
        self.component.y_stop.setValue(pos.y() + size.y())

    @QtCore.Slot()
    def update_roi(self):
        self.roi.blockSignals(True)
        self.roi.setPos((self.component.x_start.value(), self.component.y_start.value()))
        width = self.component.x_stop.value() - self.component.x_start.value()
        height = self.component.y_stop.value() - self.component.y_start.value()
        self.roi.setSize((width, height))
        self.roi.blockSignals(False)

    @QtCore.Slot()
    def _on_target_moved(self):
        pos = self.target.pos()
        self.component.move_to(pos.x(), pos.y())

    @QtCore.Slot()
    def _update_map(self):
        data = self.component.map_data.value()
        if data is None or data.size == 0:
            return
        display_data = np.where(np.isnan(data), 0, data)
        self.img_view.setImage(
            display_data,
            pos=(self.component.x_start.value(), self.component.y_start.value()),
            scale=(self.component.x_step.value(), self.component.y_step.value()),
            autoRange=False,
            autoLevels=True,
        )
