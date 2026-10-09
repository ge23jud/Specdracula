# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FourierCMOS.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtWidgets import (QAbstractSpinBox, QCheckBox, QDoubleSpinBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from pyqtgraph import ImageView

class Ui_FourierCMOSWidget(object):
    def setupUi(self, FourierCMOSWidget):
        if not FourierCMOSWidget.objectName():
            FourierCMOSWidget.setObjectName(u"FourierCMOSWidget")
        FourierCMOSWidget.resize(800, 700)
        self.verticalLayout = QVBoxLayout(FourierCMOSWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ButtonsLayout = QHBoxLayout()
        self.ButtonsLayout.setObjectName(u"ButtonsLayout")
        self.On_Button = QPushButton(FourierCMOSWidget)
        self.On_Button.setObjectName(u"On_Button")

        self.ButtonsLayout.addWidget(self.On_Button)

        self.Off_Button = QPushButton(FourierCMOSWidget)
        self.Off_Button.setObjectName(u"Off_Button")

        self.ButtonsLayout.addWidget(self.Off_Button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ButtonsLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.ButtonsLayout)

        self.img_view = ImageView(FourierCMOSWidget)
        self.img_view.setObjectName(u"img_view")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.img_view.sizePolicy().hasHeightForWidth())
        self.img_view.setSizePolicy(sizePolicy)
        self.img_view.setMinimumSize(QSize(0, 300))

        self.verticalLayout.addWidget(self.img_view)

        self.PowerSeries = QWidget(FourierCMOSWidget)
        self.PowerSeries.setObjectName(u"PowerSeries")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PowerSeries.sizePolicy().hasHeightForWidth())
        self.PowerSeries.setSizePolicy(sizePolicy1)
        self.PowerSeries.setMaximumSize(QSize(16777215, 160))
        self.gridLayout = QGridLayout(self.PowerSeries)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_13 = QLabel(self.PowerSeries)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)

        self.PsStart_DoubleSpinBox = QDoubleSpinBox(self.PowerSeries)
        self.PsStart_DoubleSpinBox.setObjectName(u"PsStart_DoubleSpinBox")
        self.PsStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStart_DoubleSpinBox, 0, 1, 1, 1)

        self.label_7 = QLabel(self.PowerSeries)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)

        self.PsStop_DoubleSpinBox = QDoubleSpinBox(self.PowerSeries)
        self.PsStop_DoubleSpinBox.setObjectName(u"PsStop_DoubleSpinBox")
        self.PsStop_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStop_DoubleSpinBox, 0, 3, 1, 1)

        self.label_14 = QLabel(self.PowerSeries)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)

        self.PsStep_DoubleSpinBox = QDoubleSpinBox(self.PowerSeries)
        self.PsStep_DoubleSpinBox.setObjectName(u"PsStep_DoubleSpinBox")
        self.PsStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStep_DoubleSpinBox, 1, 1, 1, 1)

        self.SavePng_CheckBox = QCheckBox(self.PowerSeries)
        self.SavePng_CheckBox.setObjectName(u"SavePng_CheckBox")

        self.gridLayout.addWidget(self.SavePng_CheckBox, 1, 2, 1, 2)

        self.label = QLabel(self.PowerSeries)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.PowerSeries)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout.addWidget(self.Directory_LineEdit, 2, 1, 1, 3)

        self.label_2 = QLabel(self.PowerSeries)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.Filename_LineEdit = QLineEdit(self.PowerSeries)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout.addWidget(self.Filename_LineEdit, 3, 1, 1, 3)

        self.buttonsRow = QHBoxLayout()
        self.buttonsRow.setObjectName(u"buttonsRow")
        self.StartPS_PushButton = QPushButton(self.PowerSeries)
        self.StartPS_PushButton.setObjectName(u"StartPS_PushButton")

        self.buttonsRow.addWidget(self.StartPS_PushButton)

        self.StopPS_PushButton = QPushButton(self.PowerSeries)
        self.StopPS_PushButton.setObjectName(u"StopPS_PushButton")

        self.buttonsRow.addWidget(self.StopPS_PushButton)

        self.Save_PushButton = QPushButton(self.PowerSeries)
        self.Save_PushButton.setObjectName(u"Save_PushButton")

        self.buttonsRow.addWidget(self.Save_PushButton)

        self.LoadBackground_PushButton = QPushButton(self.PowerSeries)
        self.LoadBackground_PushButton.setObjectName(u"LoadBackground_PushButton")

        self.buttonsRow.addWidget(self.LoadBackground_PushButton)

        self.ClearBackground_PushButton = QPushButton(self.PowerSeries)
        self.ClearBackground_PushButton.setObjectName(u"ClearBackground_PushButton")
        self.ClearBackground_PushButton.setEnabled(False)

        self.buttonsRow.addWidget(self.ClearBackground_PushButton)


        self.gridLayout.addLayout(self.buttonsRow, 4, 0, 1, 4)


        self.verticalLayout.addWidget(self.PowerSeries)

        self.verticalLayout.setStretch(0, 0)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 0)

        self.retranslateUi(FourierCMOSWidget)

        QMetaObject.connectSlotsByName(FourierCMOSWidget)
    # setupUi

    def retranslateUi(self, FourierCMOSWidget):
        FourierCMOSWidget.setWindowTitle(QCoreApplication.translate("FourierCMOSWidget", u"Form", None))
        self.On_Button.setText(QCoreApplication.translate("FourierCMOSWidget", u"On", None))
        self.Off_Button.setText(QCoreApplication.translate("FourierCMOSWidget", u"Off", None))
        self.label_13.setText(QCoreApplication.translate("FourierCMOSWidget", u"Start (°)", None))
        self.PsStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("FourierCMOSWidget", u"°", None))
        self.label_7.setText(QCoreApplication.translate("FourierCMOSWidget", u"Stop (°)", None))
        self.PsStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("FourierCMOSWidget", u"°", None))
        self.label_14.setText(QCoreApplication.translate("FourierCMOSWidget", u"Step (°)", None))
        self.PsStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("FourierCMOSWidget", u"°", None))
        self.SavePng_CheckBox.setText(QCoreApplication.translate("FourierCMOSWidget", u"Save png", None))
        self.label.setText(QCoreApplication.translate("FourierCMOSWidget", u"Directory", None))
        self.label_2.setText(QCoreApplication.translate("FourierCMOSWidget", u"Filename", None))
        self.StartPS_PushButton.setText(QCoreApplication.translate("FourierCMOSWidget", u"Start", None))
        self.StopPS_PushButton.setText(QCoreApplication.translate("FourierCMOSWidget", u"Stop", None))
        self.Save_PushButton.setText(QCoreApplication.translate("FourierCMOSWidget", u"Save", None))
        self.LoadBackground_PushButton.setText(QCoreApplication.translate("FourierCMOSWidget", u"Load background", None))
        self.ClearBackground_PushButton.setText(QCoreApplication.translate("FourierCMOSWidget", u"Clear BG", None))
    # retranslateUi
