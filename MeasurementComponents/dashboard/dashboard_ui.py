# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QLabel, QLayout, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_DashboardWidget(object):
    def setupUi(self, DashboardWidget):
        if not DashboardWidget.objectName():
            DashboardWidget.setObjectName(u"DashboardWidget")
        DashboardWidget.resize(321, 648)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DashboardWidget.sizePolicy().hasHeightForWidth())
        DashboardWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(DashboardWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.scrollArea = QScrollArea(DashboardWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 284, 732))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy2)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_2.setCheckable(False)
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(5)
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_4.addWidget(self.label_18, 1, 0, 1, 1)

        self.CenterEnergy_DoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.CenterEnergy_DoubleSpinBox.setObjectName(u"CenterEnergy_DoubleSpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.CenterEnergy_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.CenterEnergy_DoubleSpinBox.setSizePolicy(sizePolicy3)
        self.CenterEnergy_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.CenterEnergy_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.CenterEnergy_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_4.addWidget(self.CenterEnergy_DoubleSpinBox, 2, 1, 1, 1)

        self.DirectInputSlit_DoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.DirectInputSlit_DoubleSpinBox.setObjectName(u"DirectInputSlit_DoubleSpinBox")
        self.DirectInputSlit_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_4.addWidget(self.DirectInputSlit_DoubleSpinBox, 5, 1, 1, 1)

        self.SideInputSlit_DoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.SideInputSlit_DoubleSpinBox.setObjectName(u"SideInputSlit_DoubleSpinBox")
        self.SideInputSlit_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_4.addWidget(self.SideInputSlit_DoubleSpinBox, 4, 1, 1, 1)

        self.CenterWavelength_DoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.CenterWavelength_DoubleSpinBox.setObjectName(u"CenterWavelength_DoubleSpinBox")
        sizePolicy3.setHeightForWidth(self.CenterWavelength_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.CenterWavelength_DoubleSpinBox.setSizePolicy(sizePolicy3)
        self.CenterWavelength_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.CenterWavelength_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.CenterWavelength_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_4.addWidget(self.CenterWavelength_DoubleSpinBox, 1, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_4.addWidget(self.label_19, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer, 0, 0, 1, 2)

        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_4.addWidget(self.label_22, 5, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy2.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy2)
        self.groupBox_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)

        self.IntegrationTime_DoubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.IntegrationTime_DoubleSpinBox.setObjectName(u"IntegrationTime_DoubleSpinBox")
        sizePolicy4.setHeightForWidth(self.IntegrationTime_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.IntegrationTime_DoubleSpinBox.setSizePolicy(sizePolicy4)
        self.IntegrationTime_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.IntegrationTime_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.IntegrationTime_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.IntegrationTime_DoubleSpinBox, 1, 1, 1, 1)

        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 2)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_7 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy2.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy2)
        self.groupBox_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.groupBox_7.setFlat(False)
        self.groupBox_7.setCheckable(False)
        self.gridLayout_5 = QGridLayout(self.groupBox_7)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        self.verticalSpacer_5 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 0, 0, 1, 2)

        self.label_CmosExposure = QLabel(self.groupBox_7)
        self.label_CmosExposure.setObjectName(u"label_CmosExposure")

        self.gridLayout_5.addWidget(self.label_CmosExposure, 1, 0, 1, 1)

        self.CmosExposureTime_DoubleSpinBox = QDoubleSpinBox(self.groupBox_7)
        self.CmosExposureTime_DoubleSpinBox.setObjectName(u"CmosExposureTime_DoubleSpinBox")
        sizePolicy4.setHeightForWidth(self.CmosExposureTime_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.CmosExposureTime_DoubleSpinBox.setSizePolicy(sizePolicy4)
        self.CmosExposureTime_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.CmosExposureTime_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.CmosExposureTime_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_5.addWidget(self.CmosExposureTime_DoubleSpinBox, 1, 1, 1, 1)

        self.label_CmosGain = QLabel(self.groupBox_7)
        self.label_CmosGain.setObjectName(u"label_CmosGain")

        self.gridLayout_5.addWidget(self.label_CmosGain, 2, 0, 1, 1)

        self.CmosGain_DoubleSpinBox = QDoubleSpinBox(self.groupBox_7)
        self.CmosGain_DoubleSpinBox.setObjectName(u"CmosGain_DoubleSpinBox")
        sizePolicy4.setHeightForWidth(self.CmosGain_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.CmosGain_DoubleSpinBox.setSizePolicy(sizePolicy4)
        self.CmosGain_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.CmosGain_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.CmosGain_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_5.addWidget(self.CmosGain_DoubleSpinBox, 2, 1, 1, 1)

        self.gridLayout_5.setColumnStretch(1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_7)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy2.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy2)
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 0, 0, 1, 4)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)

        self.PiezoUp_Button = QPushButton(self.groupBox_3)
        self.PiezoUp_Button.setObjectName(u"PiezoUp_Button")
        self.PiezoUp_Button.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.PiezoUp_Button, 4, 1, 1, 2)

        self.PiezoLeft_Button = QPushButton(self.groupBox_3)
        self.PiezoLeft_Button.setObjectName(u"PiezoLeft_Button")
        self.PiezoLeft_Button.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.PiezoLeft_Button, 5, 0, 1, 2)

        self.PiezoDown_Button = QPushButton(self.groupBox_3)
        self.PiezoDown_Button.setObjectName(u"PiezoDown_Button")
        self.PiezoDown_Button.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.PiezoDown_Button, 6, 1, 1, 2)

        self.PiezoRight_Button = QPushButton(self.groupBox_3)
        self.PiezoRight_Button.setObjectName(u"PiezoRight_Button")
        self.PiezoRight_Button.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.PiezoRight_Button, 5, 2, 1, 2)

        self.PiezoX_DoubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.PiezoX_DoubleSpinBox.setObjectName(u"PiezoX_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.PiezoX_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PiezoX_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.PiezoX_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.PiezoX_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.PiezoX_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.PiezoX_DoubleSpinBox, 1, 1, 1, 3)

        self.PiezoY_DoubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.PiezoY_DoubleSpinBox.setObjectName(u"PiezoY_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.PiezoY_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PiezoY_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.PiezoY_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.PiezoY_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.PiezoY_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.PiezoY_DoubleSpinBox, 2, 1, 1, 3)

        self.PiezoStep_DoubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.PiezoStep_DoubleSpinBox.setObjectName(u"PiezoStep_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.PiezoStep_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PiezoStep_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.PiezoStep_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.PiezoStep_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.PiezoStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.PiezoStep_DoubleSpinBox, 3, 1, 1, 3)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy2.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy2)
        self.groupBox_6.setMinimumSize(QSize(0, 0))
        self.groupBox_6.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(self.groupBox_6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(9, 9, -1, -1)
        self.label_ActiveLaser = QLabel(self.groupBox_6)
        self.label_ActiveLaser.setObjectName(u"label_ActiveLaser")
        self.label_ActiveLaser.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_ActiveLaser, 0, 0, 1, 1)

        self.ActiveLaser_ComboBox = QComboBox(self.groupBox_6)
        self.ActiveLaser_ComboBox.addItem("")
        self.ActiveLaser_ComboBox.addItem("")
        self.ActiveLaser_ComboBox.setObjectName(u"ActiveLaser_ComboBox")

        self.gridLayout_2.addWidget(self.ActiveLaser_ComboBox, 0, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox_6)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)

        self.HWPPos_DoubleSpinBox = QDoubleSpinBox(self.groupBox_6)
        self.HWPPos_DoubleSpinBox.setObjectName(u"HWPPos_DoubleSpinBox")
        self.HWPPos_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.HWPPos_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.HWPPos_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.HWPPos_DoubleSpinBox, 3, 1, 1, 1)

        self.Shutter_CheckBox = QCheckBox(self.groupBox_6)
        self.Shutter_CheckBox.setObjectName(u"Shutter_CheckBox")
        self.Shutter_CheckBox.setMinimumSize(QSize(0, 25))

        self.gridLayout_2.addWidget(self.Shutter_CheckBox, 2, 0, 1, 2)

        self.Laser2On_CheckBox = QCheckBox(self.groupBox_6)
        self.Laser2On_CheckBox.setObjectName(u"Laser2On_CheckBox")
        self.Laser2On_CheckBox.setMinimumSize(QSize(0, 25))

        self.gridLayout_2.addWidget(self.Laser2On_CheckBox, 4, 0, 1, 2)

        self.label_Laser2Power = QLabel(self.groupBox_6)
        self.label_Laser2Power.setObjectName(u"label_Laser2Power")
        self.label_Laser2Power.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_Laser2Power, 5, 0, 1, 1)

        self.Laser2Power_DoubleSpinBox = QDoubleSpinBox(self.groupBox_6)
        self.Laser2Power_DoubleSpinBox.setObjectName(u"Laser2Power_DoubleSpinBox")
        self.Laser2Power_DoubleSpinBox.setMinimumSize(QSize(0, 25))
        self.Laser2Power_DoubleSpinBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.Laser2Power_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.Laser2Power_DoubleSpinBox, 5, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 1, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.line = QFrame(DashboardWidget)
        self.line.setObjectName(u"line")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy5)
        self.line.setMinimumSize(QSize(0, 3))
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(DashboardWidget)

        QMetaObject.connectSlotsByName(DashboardWidget)
    # setupUi

    def retranslateUi(self, DashboardWidget):
        DashboardWidget.setWindowTitle(QCoreApplication.translate("DashboardWidget", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DashboardWidget", u"Spectrometer", None))
        self.label_8.setText(QCoreApplication.translate("DashboardWidget", u"Side Input Slit", None))
        self.label_18.setText(QCoreApplication.translate("DashboardWidget", u"Center Wavelength", None))
        self.CenterEnergy_DoubleSpinBox.setSuffix("")
        self.CenterWavelength_DoubleSpinBox.setSuffix("")
        self.label_19.setText(QCoreApplication.translate("DashboardWidget", u"Center Energy", None))
        self.label_22.setText(QCoreApplication.translate("DashboardWidget", u"Direct Input Slit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("DashboardWidget", u"Detector", None))
        self.IntegrationTime_DoubleSpinBox.setSuffix("")
        self.label.setText(QCoreApplication.translate("DashboardWidget", u"Integration Time", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("DashboardWidget", u"Fourier CMOS", None))
        self.CmosExposureTime_DoubleSpinBox.setSuffix("")
        self.label_CmosExposure.setText(QCoreApplication.translate("DashboardWidget", u"Exposure Time", None))
        self.CmosGain_DoubleSpinBox.setSuffix("")
        self.label_CmosGain.setText(QCoreApplication.translate("DashboardWidget", u"Gain", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("DashboardWidget", u"Piezo", None))
        self.label_6.setText(QCoreApplication.translate("DashboardWidget", u"Step", None))
        self.label_2.setText(QCoreApplication.translate("DashboardWidget", u"X-Position", None))
        self.label_3.setText(QCoreApplication.translate("DashboardWidget", u"Y-Position", None))
        self.PiezoUp_Button.setText(QCoreApplication.translate("DashboardWidget", u"Up", None))
        self.PiezoLeft_Button.setText(QCoreApplication.translate("DashboardWidget", u"Left", None))
        self.PiezoDown_Button.setText(QCoreApplication.translate("DashboardWidget", u"Down", None))
        self.PiezoRight_Button.setText(QCoreApplication.translate("DashboardWidget", u"Right", None))
        self.PiezoX_DoubleSpinBox.setSuffix("")
        self.PiezoY_DoubleSpinBox.setSuffix("")
        self.PiezoStep_DoubleSpinBox.setSuffix("")
        self.groupBox_6.setTitle(QCoreApplication.translate("DashboardWidget", u"Power Control", None))
        self.label_ActiveLaser.setText(QCoreApplication.translate("DashboardWidget", u"Active Laser", None))
        self.ActiveLaser_ComboBox.setItemText(0, QCoreApplication.translate("DashboardWidget", u"Laser 1 (HWP)", None))
        self.ActiveLaser_ComboBox.setItemText(1, QCoreApplication.translate("DashboardWidget", u"Laser 2 (KLS)", None))
        self.label_11.setText(QCoreApplication.translate("DashboardWidget", u"Power HWP Position", None))
        self.HWPPos_DoubleSpinBox.setSuffix("")
        self.Shutter_CheckBox.setText(QCoreApplication.translate("DashboardWidget", u"Shutter open", None))
        self.Laser2On_CheckBox.setText(QCoreApplication.translate("DashboardWidget", u"Laser On", None))
        self.label_Laser2Power.setText(QCoreApplication.translate("DashboardWidget", u"Laser 2 Power", None))
        self.Laser2Power_DoubleSpinBox.setSuffix("")
    # retranslateUi

