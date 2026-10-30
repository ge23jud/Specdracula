# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FourFPump.ui'
##
## Written by hand to match FourFPump.ui (pyside6-uic is broken in this env).
## Keep both files in sync when changing the form.
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtWidgets import (QAbstractSpinBox, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

from pyqtgraph import ImageView, PlotWidget

class Ui_FourFPumpWidget(object):
    def setupUi(self, FourFPumpWidget):
        if not FourFPumpWidget.objectName():
            FourFPumpWidget.setObjectName(u"FourFPumpWidget")
        FourFPumpWidget.resize(1094, 787)
        self.verticalLayout = QVBoxLayout(FourFPumpWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Status_Label = QLabel(FourFPumpWidget)
        self.Status_Label.setObjectName(u"Status_Label")
        self.Status_Label.setMaximumSize(QSize(16777215, 18))
        self.Status_Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.Status_Label)

        self.Plots = QWidget(FourFPumpWidget)
        self.Plots.setObjectName(u"Plots")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Plots.sizePolicy().hasHeightForWidth())
        self.Plots.setSizePolicy(sizePolicy)
        self.horizontalLayout_plots = QHBoxLayout(self.Plots)
        self.horizontalLayout_plots.setObjectName(u"horizontalLayout_plots")
        self.horizontalLayout_plots.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = PlotWidget(self.Plots)
        self.plot_widget.setObjectName(u"plot_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy1)

        self.horizontalLayout_plots.addWidget(self.plot_widget)

        self.img_view = ImageView(self.Plots)
        self.img_view.setObjectName(u"img_view")
        sizePolicy1.setHeightForWidth(self.img_view.sizePolicy().hasHeightForWidth())
        self.img_view.setSizePolicy(sizePolicy1)

        self.horizontalLayout_plots.addWidget(self.img_view)


        self.verticalLayout.addWidget(self.Plots)

        self.Controls = QWidget(FourFPumpWidget)
        self.Controls.setObjectName(u"Controls")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Controls.sizePolicy().hasHeightForWidth())
        self.Controls.setSizePolicy(sizePolicy2)
        self.horizontalLayout_controls = QHBoxLayout(self.Controls)
        self.horizontalLayout_controls.setObjectName(u"horizontalLayout_controls")
        self.Scan = QWidget(self.Controls)
        self.Scan.setObjectName(u"Scan")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Scan.sizePolicy().hasHeightForWidth())
        self.Scan.setSizePolicy(sizePolicy3)
        self.gridLayout_scan = QGridLayout(self.Scan)
        self.gridLayout_scan.setObjectName(u"gridLayout_scan")
        self.label_range = QLabel(self.Scan)
        self.label_range.setObjectName(u"label_range")

        self.gridLayout_scan.addWidget(self.label_range, 0, 1, 1, 1)

        self.label_step = QLabel(self.Scan)
        self.label_step.setObjectName(u"label_step")

        self.gridLayout_scan.addWidget(self.label_step, 0, 2, 1, 1)

        self.label_x = QLabel(self.Scan)
        self.label_x.setObjectName(u"label_x")

        self.gridLayout_scan.addWidget(self.label_x, 1, 0, 1, 1)

        self.XRange_SpinBox = QSpinBox(self.Scan)
        self.XRange_SpinBox.setObjectName(u"XRange_SpinBox")
        self.XRange_SpinBox.setMinimumSize(QSize(100, 25))
        self.XRange_SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.XRange_SpinBox.setMaximum(100000)

        self.gridLayout_scan.addWidget(self.XRange_SpinBox, 1, 1, 1, 1)

        self.XStep_SpinBox = QSpinBox(self.Scan)
        self.XStep_SpinBox.setObjectName(u"XStep_SpinBox")
        self.XStep_SpinBox.setMinimumSize(QSize(100, 25))
        self.XStep_SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.XStep_SpinBox.setMinimum(1)
        self.XStep_SpinBox.setMaximum(100000)

        self.gridLayout_scan.addWidget(self.XStep_SpinBox, 1, 2, 1, 1)

        self.label_y = QLabel(self.Scan)
        self.label_y.setObjectName(u"label_y")

        self.gridLayout_scan.addWidget(self.label_y, 2, 0, 1, 1)

        self.YRange_SpinBox = QSpinBox(self.Scan)
        self.YRange_SpinBox.setObjectName(u"YRange_SpinBox")
        self.YRange_SpinBox.setMinimumSize(QSize(100, 25))
        self.YRange_SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.YRange_SpinBox.setMaximum(100000)

        self.gridLayout_scan.addWidget(self.YRange_SpinBox, 2, 1, 1, 1)

        self.YStep_SpinBox = QSpinBox(self.Scan)
        self.YStep_SpinBox.setObjectName(u"YStep_SpinBox")
        self.YStep_SpinBox.setMinimumSize(QSize(100, 25))
        self.YStep_SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.YStep_SpinBox.setMinimum(1)
        self.YStep_SpinBox.setMaximum(100000)

        self.gridLayout_scan.addWidget(self.YStep_SpinBox, 2, 2, 1, 1)

        self.label_settle = QLabel(self.Scan)
        self.label_settle.setObjectName(u"label_settle")

        self.gridLayout_scan.addWidget(self.label_settle, 3, 0, 1, 1)

        self.SettleTime_DoubleSpinBox = QDoubleSpinBox(self.Scan)
        self.SettleTime_DoubleSpinBox.setObjectName(u"SettleTime_DoubleSpinBox")
        self.SettleTime_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.SettleTime_DoubleSpinBox.setDecimals(3)
        self.SettleTime_DoubleSpinBox.setMaximum(60.000000000000000)

        self.gridLayout_scan.addWidget(self.SettleTime_DoubleSpinBox, 3, 1, 1, 1)

        self.ReturnToCenter_CheckBox = QCheckBox(self.Scan)
        self.ReturnToCenter_CheckBox.setObjectName(u"ReturnToCenter_CheckBox")

        self.gridLayout_scan.addWidget(self.ReturnToCenter_CheckBox, 3, 2, 1, 1)

        self.label_measurements = QLabel(self.Scan)
        self.label_measurements.setObjectName(u"label_measurements")

        self.gridLayout_scan.addWidget(self.label_measurements, 4, 0, 1, 1)

        self.NumMeasurements_Label = QLabel(self.Scan)
        self.NumMeasurements_Label.setObjectName(u"NumMeasurements_Label")

        self.gridLayout_scan.addWidget(self.NumMeasurements_Label, 4, 1, 1, 1)

        self.label_window = QLabel(self.Scan)
        self.label_window.setObjectName(u"label_window")

        self.gridLayout_scan.addWidget(self.label_window, 5, 0, 1, 1)

        self.WindowMin_DoubleSpinBox = QDoubleSpinBox(self.Scan)
        self.WindowMin_DoubleSpinBox.setObjectName(u"WindowMin_DoubleSpinBox")
        self.WindowMin_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.WindowMin_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.WindowMin_DoubleSpinBox.setDecimals(2)
        self.WindowMin_DoubleSpinBox.setMaximum(10000.000000000000000)

        self.gridLayout_scan.addWidget(self.WindowMin_DoubleSpinBox, 5, 1, 1, 1)

        self.WindowMax_DoubleSpinBox = QDoubleSpinBox(self.Scan)
        self.WindowMax_DoubleSpinBox.setObjectName(u"WindowMax_DoubleSpinBox")
        self.WindowMax_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.WindowMax_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.WindowMax_DoubleSpinBox.setDecimals(2)
        self.WindowMax_DoubleSpinBox.setMaximum(10000.000000000000000)

        self.gridLayout_scan.addWidget(self.WindowMax_DoubleSpinBox, 5, 2, 1, 1)

        self.StartScan_PushButton = QPushButton(self.Scan)
        self.StartScan_PushButton.setObjectName(u"StartScan_PushButton")

        self.gridLayout_scan.addWidget(self.StartScan_PushButton, 6, 1, 1, 1)

        self.StopScan_PushButton = QPushButton(self.Scan)
        self.StopScan_PushButton.setObjectName(u"StopScan_PushButton")

        self.gridLayout_scan.addWidget(self.StopScan_PushButton, 6, 2, 1, 1)


        self.horizontalLayout_controls.addWidget(self.Scan)

        self.Acquire = QWidget(self.Controls)
        self.Acquire.setObjectName(u"Acquire")
        sizePolicy3.setHeightForWidth(self.Acquire.sizePolicy().hasHeightForWidth())
        self.Acquire.setSizePolicy(sizePolicy3)
        self.verticalLayout_acquire = QVBoxLayout(self.Acquire)
        self.verticalLayout_acquire.setObjectName(u"verticalLayout_acquire")
        self.Snapshot_PushButton = QPushButton(self.Acquire)
        self.Snapshot_PushButton.setObjectName(u"Snapshot_PushButton")

        self.verticalLayout_acquire.addWidget(self.Snapshot_PushButton)

        self.StartLive_PushButton = QPushButton(self.Acquire)
        self.StartLive_PushButton.setObjectName(u"StartLive_PushButton")

        self.verticalLayout_acquire.addWidget(self.StartLive_PushButton)

        self.StopLive_PushButton = QPushButton(self.Acquire)
        self.StopLive_PushButton.setObjectName(u"StopLive_PushButton")

        self.verticalLayout_acquire.addWidget(self.StopLive_PushButton)


        self.horizontalLayout_controls.addWidget(self.Acquire)

        self.SaveData = QWidget(self.Controls)
        self.SaveData.setObjectName(u"SaveData")
        sizePolicy2.setHeightForWidth(self.SaveData.sizePolicy().hasHeightForWidth())
        self.SaveData.setSizePolicy(sizePolicy2)
        self.gridLayout_save = QGridLayout(self.SaveData)
        self.gridLayout_save.setObjectName(u"gridLayout_save")
        self.label_directory = QLabel(self.SaveData)
        self.label_directory.setObjectName(u"label_directory")

        self.gridLayout_save.addWidget(self.label_directory, 0, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.SaveData)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout_save.addWidget(self.Directory_LineEdit, 0, 1, 1, 1)

        self.label_filename = QLabel(self.SaveData)
        self.label_filename.setObjectName(u"label_filename")

        self.gridLayout_save.addWidget(self.label_filename, 1, 0, 1, 1)

        self.Filename_LineEdit = QLineEdit(self.SaveData)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout_save.addWidget(self.Filename_LineEdit, 1, 1, 1, 1)

        self.label_xaxis = QLabel(self.SaveData)
        self.label_xaxis.setObjectName(u"label_xaxis")

        self.gridLayout_save.addWidget(self.label_xaxis, 2, 0, 1, 1)

        self.xlabel_ComboBox = QComboBox(self.SaveData)
        self.xlabel_ComboBox.addItem("")
        self.xlabel_ComboBox.addItem("")
        self.xlabel_ComboBox.setObjectName(u"xlabel_ComboBox")

        self.gridLayout_save.addWidget(self.xlabel_ComboBox, 2, 1, 1, 1)

        self.label_scale = QLabel(self.SaveData)
        self.label_scale.setObjectName(u"label_scale")

        self.gridLayout_save.addWidget(self.label_scale, 3, 0, 1, 1)

        self.yscale_ComboBox = QComboBox(self.SaveData)
        self.yscale_ComboBox.addItem("")
        self.yscale_ComboBox.addItem("")
        self.yscale_ComboBox.setObjectName(u"yscale_ComboBox")

        self.gridLayout_save.addWidget(self.yscale_ComboBox, 3, 1, 1, 1)


        self.horizontalLayout_controls.addWidget(self.SaveData)


        self.verticalLayout.addWidget(self.Controls)


        self.retranslateUi(FourFPumpWidget)

        QMetaObject.connectSlotsByName(FourFPumpWidget)
    # setupUi

    def retranslateUi(self, FourFPumpWidget):
        FourFPumpWidget.setWindowTitle(QCoreApplication.translate("FourFPumpWidget", u"Form", None))
        self.Status_Label.setText("")
        self.label_range.setText(QCoreApplication.translate("FourFPumpWidget", u"Range ± (steps)", None))
        self.label_step.setText(QCoreApplication.translate("FourFPumpWidget", u"Step (steps)", None))
        self.label_x.setText(QCoreApplication.translate("FourFPumpWidget", u"X", None))
        self.label_y.setText(QCoreApplication.translate("FourFPumpWidget", u"Y", None))
        self.label_settle.setText(QCoreApplication.translate("FourFPumpWidget", u"Settle (s)", None))
        self.ReturnToCenter_CheckBox.setText(QCoreApplication.translate("FourFPumpWidget", u"Return to center", None))
        self.label_measurements.setText(QCoreApplication.translate("FourFPumpWidget", u"Measurements", None))
        self.NumMeasurements_Label.setText(QCoreApplication.translate("FourFPumpWidget", u"0", None))
        self.label_window.setText(QCoreApplication.translate("FourFPumpWidget", u"Window (nm)", None))
        self.StartScan_PushButton.setText(QCoreApplication.translate("FourFPumpWidget", u"Start Scan", None))
        self.StopScan_PushButton.setText(QCoreApplication.translate("FourFPumpWidget", u"Stop Scan", None))
        self.Snapshot_PushButton.setText(QCoreApplication.translate("FourFPumpWidget", u"Snapshot", None))
        self.StartLive_PushButton.setText(QCoreApplication.translate("FourFPumpWidget", u"Start Live", None))
        self.StopLive_PushButton.setText(QCoreApplication.translate("FourFPumpWidget", u"Stop Live", None))
        self.label_directory.setText(QCoreApplication.translate("FourFPumpWidget", u"Directory", None))
        self.label_filename.setText(QCoreApplication.translate("FourFPumpWidget", u"Filename", None))
        self.label_xaxis.setText(QCoreApplication.translate("FourFPumpWidget", u"X-axis", None))
        self.xlabel_ComboBox.setItemText(0, QCoreApplication.translate("FourFPumpWidget", u"Energy", None))
        self.xlabel_ComboBox.setItemText(1, QCoreApplication.translate("FourFPumpWidget", u"Wavelength", None))
        self.label_scale.setText(QCoreApplication.translate("FourFPumpWidget", u"Scale", None))
        self.yscale_ComboBox.setItemText(0, QCoreApplication.translate("FourFPumpWidget", u"Linear", None))
        self.yscale_ComboBox.setItemText(1, QCoreApplication.translate("FourFPumpWidget", u"Logarithmic", None))
    # retranslateUi
