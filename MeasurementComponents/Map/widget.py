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

        self.update_nummeasurements_label()


    def update_nummeasurements_label(self):
        self.NumMeasurements_Label.setText(str(self.component.n_measurements.value()))


    def replace_imageview_with_plotitem(self):
        # Get the parent and layout of the old img_view
        parent = self.img_view.parent()
        layout = parent.layout()
        
        # Find the position in layout
        index = layout.indexOf(self.img_view)
        
        # Remove old widget
        layout.removeWidget(self.img_view)
        self.img_view.deleteLater()
        
        # Create new ImageView with PlotItem
        self.img_view = pg.ImageView(view=pg.PlotItem())
        
        # Add to layout at same position
        layout.insertWidget(index, self.img_view)

    def setup_2d_plot(self):

        self.plot_item = self.img_view.getView()

        self.plot_item.setLabel("bottom", "X", units="um")
        self.plot_item.setLabel("left", "Y", units="um")

        self.plot_item.showGrid(x=True, y=True, alpha=0.2)

        
        self.target = pg.TargetItem()
        self.plot_item.addItem(self.target)

        self.roi = pg.ROI(pos=(0, 0), size=(1, 1), resizable=True, rotatable=False)
        self.roi.addScaleHandle(pos=(1,1), center=(0,0))
        self.plot_item.addItem(self.roi)

        

    