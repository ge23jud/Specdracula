# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Polarization.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtWidgets import (QAbstractSpinBox, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_PolarizationWidget(object):
    def setupUi(self, PolarizationWidget):
        if not PolarizationWidget.objectName():
            PolarizationWidget.setObjectName(u"PolarizationWidget")
        PolarizationWidget.resize(1094, 780)
        self.verticalLayout = QVBoxLayout(PolarizationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Status_Label = QLabel(PolarizationWidget)
        self.Status_Label.setObjectName(u"Status_Label")
        self.Status_Label.setMaximumSize(QSize(16777215, 18))
        self.Status_Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.Status_Label)

        self.plot_widget = PlotWidget(PolarizationWidget)
        self.plot_widget.setObjectName(u"plot_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.plot_widget)

        self.Controls = QWidget(PolarizationWidget)
        self.Controls.setObjectName(u"Controls")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Controls.sizePolicy().hasHeightForWidth())
        self.Controls.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.Controls)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SweepWidget = QWidget(self.Controls)
        self.SweepWidget.setObjectName(u"SweepWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SweepWidget.sizePolicy().hasHeightForWidth())
        self.SweepWidget.setSizePolicy(sizePolicy2)
        self.gridLayout = QGridLayout(self.SweepWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_start = QLabel(self.SweepWidget)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout.addWidget(self.label_start, 0, 0, 1, 1)

        self.AngleStart_DoubleSpinBox = QDoubleSpinBox(self.SweepWidget)
        self.AngleStart_DoubleSpinBox.setObjectName(u"AngleStart_DoubleSpinBox")
        self.AngleStart_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.AngleStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.AngleStart_DoubleSpinBox, 0, 1, 1, 1)

        self.label_stop = QLabel(self.SweepWidget)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout.addWidget(self.label_stop, 1, 0, 1, 1)

        self.AngleStop_DoubleSpinBox = QDoubleSpinBox(self.SweepWidget)
        self.AngleStop_DoubleSpinBox.setObjectName(u"AngleStop_DoubleSpinBox")
        self.AngleStop_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.AngleStop_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.AngleStop_DoubleSpinBox, 1, 1, 1, 1)

        self.label_step = QLabel(self.SweepWidget)
        self.label_step.setObjectName(u"label_step")

        self.gridLayout.addWidget(self.label_step, 2, 0, 1, 1)

        self.AngleStep_DoubleSpinBox = QDoubleSpinBox(self.SweepWidget)
        self.AngleStep_DoubleSpinBox.setObjectName(u"AngleStep_DoubleSpinBox")
        self.AngleStep_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.AngleStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.AngleStep_DoubleSpinBox, 2, 1, 1, 1)

        self.Settings_PushButton = QPushButton(self.SweepWidget)
        self.Settings_PushButton.setObjectName(u"Settings_PushButton")

        self.gridLayout.addWidget(self.Settings_PushButton, 3, 0, 1, 2)

        self.StartSeries_PushButton = QPushButton(self.SweepWidget)
        self.StartSeries_PushButton.setObjectName(u"StartSeries_PushButton")

        self.gridLayout.addWidget(self.StartSeries_PushButton, 4, 0, 1, 2)

        self.StopSeries_PushButton = QPushButton(self.SweepWidget)
        self.StopSeries_PushButton.setObjectName(u"StopSeries_PushButton")

        self.gridLayout.addWidget(self.StopSeries_PushButton, 5, 0, 1, 2)

        self.Snapshot_PushButton = QPushButton(self.SweepWidget)
        self.Snapshot_PushButton.setObjectName(u"Snapshot_PushButton")

        self.gridLayout.addWidget(self.Snapshot_PushButton, 0, 2, 1, 1)

        self.Save_PushButton = QPushButton(self.SweepWidget)
        self.Save_PushButton.setObjectName(u"Save_PushButton")

        self.gridLayout.addWidget(self.Save_PushButton, 1, 2, 1, 1)

        self.StartLive_PushButton = QPushButton(self.SweepWidget)
        self.StartLive_PushButton.setObjectName(u"StartLive_PushButton")

        self.gridLayout.addWidget(self.StartLive_PushButton, 4, 2, 1, 1)

        self.StopLive_PushButton = QPushButton(self.SweepWidget)
        self.StopLive_PushButton.setObjectName(u"StopLive_PushButton")

        self.gridLayout.addWidget(self.StopLive_PushButton, 5, 2, 1, 1)


        self.horizontalLayout.addWidget(self.SweepWidget)

        self.SaveWidget = QWidget(self.Controls)
        self.SaveWidget.setObjectName(u"SaveWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.SaveWidget.sizePolicy().hasHeightForWidth())
        self.SaveWidget.setSizePolicy(sizePolicy3)
        self.gridLayout_2 = QGridLayout(self.SaveWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.SaveWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.SaveWidget)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout_2.addWidget(self.Directory_LineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.SaveWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.Filename_LineEdit = QLineEdit(self.SaveWidget)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout_2.addWidget(self.Filename_LineEdit, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.SaveWidget)


        self.verticalLayout.addWidget(self.Controls)


        self.retranslateUi(PolarizationWidget)

        QMetaObject.connectSlotsByName(PolarizationWidget)
    # setupUi

    def retranslateUi(self, PolarizationWidget):
        PolarizationWidget.setWindowTitle(QCoreApplication.translate("PolarizationWidget", u"Form", None))
        self.Status_Label.setText("")
        self.label_start.setText(QCoreApplication.translate("PolarizationWidget", u"Start (°)", None))
        self.AngleStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("PolarizationWidget", u"°", None))
        self.label_stop.setText(QCoreApplication.translate("PolarizationWidget", u"Stop (°)", None))
        self.AngleStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("PolarizationWidget", u"°", None))
        self.label_step.setText(QCoreApplication.translate("PolarizationWidget", u"Step (°)", None))
        self.AngleStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("PolarizationWidget", u"°", None))
        self.Settings_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Settings...", None))
        self.StartSeries_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Start", None))
        self.StopSeries_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Stop", None))
        self.Snapshot_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Snapshot", None))
        self.Save_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Save Snapshot", None))
        self.StartLive_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Start Live", None))
        self.StopLive_PushButton.setText(QCoreApplication.translate("PolarizationWidget", u"Stop Live", None))
        self.label.setText(QCoreApplication.translate("PolarizationWidget", u"Directory", None))
        self.label_2.setText(QCoreApplication.translate("PolarizationWidget", u"Filename", None))
    # retranslateUi

