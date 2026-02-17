from PySide6 import QtCore
import ScopeFoundry as SFT
import pyqtgraph as pg
import numpy as np

from ScopeFoundry import TurboComponentView, connect_widget_to_param
from .Map_ui import Ui_MapWidget

from PySide6 import QtCore, QtWidgets


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
        
        component.n_measurements.sigValueChanged.connect(self.update_nummeasurements_label)
        component.x_start.sigValueChanged.connect(self.update_roi)
        component.y_start.sigValueChanged.connect(self.update_roi)
        component.x_stop.sigValueChanged.connect(self.update_roi)
        component.y_stop.sigValueChanged.connect(self.update_roi)
        self.roi.sigRegionChangeFinished.connect(self._on_roi_changed)

        self.update_nummeasurements_label()


    def update_nummeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))


    def replace_imageview_with_plotitem(self):
        # If the ImageView Widget is created in qtdesigner, the item inside is a ViewBox by default. For setting the axis labels, a PlotItem is required instead. 
        # It is therefore replaced in this method
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
        self.roi.addScaleHandle(pos=(1,1), center=(0,0))
        self.plot_item.addItem(self.roi)
        self.roi.setZValue(1)


    @QtCore.Slot()
    def _on_roi_changed(self):

        pos = self.roi.pos()
        pos_x = pos.x()
        pos_y = pos.y()
        size = self.roi.size()
        size_x = size.x()
        size_y = size.y()
        self.component.x_start.setValue(pos_x)
        self.component.x_stop.setValue(pos_x + size_x)
        self.component.y_start.setValue(pos_y)
        self.component.y_stop.setValue(pos_y + size_y)

    
    @QtCore.Slot()
    def update_roi(self):

        self.roi.blockSignals(True)

        self.roi.setPos((self.component.x_start.value(), self.component.y_start.value()))
        width = self.component.x_stop.value() - self.component.x_start.value()
        height = self.component.y_stop.value() - self.component.x_start.value()       
        self.roi.setSize((width, height))

        self.roi.blockSignals(False)


    