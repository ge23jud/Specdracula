# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Photoluminescence.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_PhotoluminescenceWidget(object):
    def setupUi(self, PhotoluminescenceWidget):
        if not PhotoluminescenceWidget.objectName():
            PhotoluminescenceWidget.setObjectName(u"PhotoluminescenceWidget")
        PhotoluminescenceWidget.resize(1094, 780)
        self.verticalLayout = QVBoxLayout(PhotoluminescenceWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(PhotoluminescenceWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_11 = QVBoxLayout(self.widget_4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.Status_Label = QLabel(self.widget_4)
        self.Status_Label.setObjectName(u"Status_Label")
        self.Status_Label.setMaximumSize(QSize(16777215, 18))
        self.Status_Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_11.addWidget(self.Status_Label)

        self.plot_widget = PlotWidget(self.widget_4)
        self.plot_widget.setObjectName(u"plot_widget")
        self.plot_widget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)

        self.verticalLayout_11.addWidget(self.plot_widget)

        self.SaveData = QWidget(self.widget_4)
        self.SaveData.setObjectName(u"SaveData")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SaveData.sizePolicy().hasHeightForWidth())
        self.SaveData.setSizePolicy(sizePolicy1)
        self.SaveData.setMinimumSize(QSize(0, 0))
        self.SaveData.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.SaveData)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_13 = QWidget(self.SaveData)
        self.widget_13.setObjectName(u"widget_13")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_13.sizePolicy().hasHeightForWidth())
        self.widget_13.setSizePolicy(sizePolicy2)
        self.widget_13.setMinimumSize(QSize(0, 25))
        self.widget_13.setMaximumSize(QSize(16777215, 170))
        self.gridLayout = QGridLayout(self.widget_13)
        self.gridLayout.setObjectName(u"gridLayout")
        self.StopLivePL_PushButton = QPushButton(self.widget_13)
        self.StopLivePL_PushButton.setObjectName(u"StopLivePL_PushButton")

        self.gridLayout.addWidget(self.StopLivePL_PushButton, 7, 3, 1, 1)

        self.Snapshot_PushButton = QPushButton(self.widget_13)
        self.Snapshot_PushButton.setObjectName(u"Snapshot_PushButton")

        self.gridLayout.addWidget(self.Snapshot_PushButton, 0, 3, 1, 1)

        self.StartLivePL_PushButton = QPushButton(self.widget_13)
        self.StartLivePL_PushButton.setObjectName(u"StartLivePL_PushButton")

        self.gridLayout.addWidget(self.StartLivePL_PushButton, 6, 3, 1, 1)

        self.SavePL_PushButton = QPushButton(self.widget_13)
        self.SavePL_PushButton.setObjectName(u"SavePL_PushButton")

        self.gridLayout.addWidget(self.SavePL_PushButton, 1, 3, 1, 1)

        self.label_13 = QLabel(self.widget_13)
        self.label_13.setObjectName(u"label_13")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_14 = QLabel(self.widget_13)
        self.label_14.setObjectName(u"label_14")
        sizePolicy3.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)

        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)

        self.Settings_PushButton = QPushButton(self.widget_13)
        self.Settings_PushButton.setObjectName(u"Settings_PushButton")

        self.gridLayout.addWidget(self.Settings_PushButton, 3, 0, 1, 3)

        self.PsStop_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.PsStop_DoubleSpinBox.setObjectName(u"PsStop_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.PsStop_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PsStop_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.PsStop_DoubleSpinBox.setMinimumSize(QSize(100, 10))
        self.PsStop_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStop_DoubleSpinBox, 1, 1, 1, 2)

        self.PsStep_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.PsStep_DoubleSpinBox.setObjectName(u"PsStep_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.PsStep_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PsStep_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.PsStep_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.PsStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStep_DoubleSpinBox, 2, 1, 1, 2)

        self.StartPS_PushButton = QPushButton(self.widget_13)
        self.StartPS_PushButton.setObjectName(u"StartPS_PushButton")
        sizePolicy1.setHeightForWidth(self.StartPS_PushButton.sizePolicy().hasHeightForWidth())
        self.StartPS_PushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.StartPS_PushButton, 6, 0, 1, 3)

        self.StopPS_PushButton = QPushButton(self.widget_13)
        self.StopPS_PushButton.setObjectName(u"StopPS_PushButton")
        sizePolicy1.setHeightForWidth(self.StopPS_PushButton.sizePolicy().hasHeightForWidth())
        self.StopPS_PushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.StopPS_PushButton, 7, 0, 1, 3)

        self.PsStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.PsStart_DoubleSpinBox.setObjectName(u"PsStart_DoubleSpinBox")
        self.PsStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStart_DoubleSpinBox, 0, 1, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.horizontalLayout_2.addWidget(self.widget_13)

        self.widget_5 = QWidget(self.SaveData)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy5)
        self.gridLayout_4 = QGridLayout(self.widget_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 2, 0, 1, 1)

        self.MinEnergy_DoubleSpinBox = QDoubleSpinBox(self.widget_5)
        self.MinEnergy_DoubleSpinBox.setObjectName(u"MinEnergy_DoubleSpinBox")

        self.gridLayout_4.addWidget(self.MinEnergy_DoubleSpinBox, 1, 1, 1, 1)

        self.BandwidthSweepEnable_CheckBox = QCheckBox(self.widget_5)
        self.BandwidthSweepEnable_CheckBox.setObjectName(u"BandwidthSweepEnable_CheckBox")
        sizePolicy4.setHeightForWidth(self.BandwidthSweepEnable_CheckBox.sizePolicy().hasHeightForWidth())
        self.BandwidthSweepEnable_CheckBox.setSizePolicy(sizePolicy4)

        self.gridLayout_4.addWidget(self.BandwidthSweepEnable_CheckBox, 0, 0, 1, 1)

        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)

        self.MaxEnergy_DoubleSpinBox = QDoubleSpinBox(self.widget_5)
        self.MaxEnergy_DoubleSpinBox.setObjectName(u"MaxEnergy_DoubleSpinBox")

        self.gridLayout_4.addWidget(self.MaxEnergy_DoubleSpinBox, 2, 1, 1, 1)

        self.Overlap_DoubleSpinBox = QDoubleSpinBox(self.widget_5)
        self.Overlap_DoubleSpinBox.setObjectName(u"Overlap_DoubleSpinBox")

        self.gridLayout_4.addWidget(self.Overlap_DoubleSpinBox, 3, 1, 1, 1)

        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 3, 0, 1, 1)

        self.BSPowerMajor_CheckBox = QCheckBox(self.widget_5)
        self.BSPowerMajor_CheckBox.setObjectName(u"BSPowerMajor_CheckBox")

        self.gridLayout_4.addWidget(self.BSPowerMajor_CheckBox, 4, 0, 1, 2)


        self.horizontalLayout_2.addWidget(self.widget_5)

        self.widget_2 = QWidget(self.SaveData)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Filename_LineEdit = QLineEdit(self.widget_2)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout_2.addWidget(self.Filename_LineEdit, 1, 1, 1, 1)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.widget_2)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout_2.addWidget(self.Directory_LineEdit, 0, 1, 1, 1)

        self.horizontalLayout_2.addWidget(self.widget_2)


        self.verticalLayout_11.addWidget(self.SaveData)


        self.horizontalLayout.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(PhotoluminescenceWidget)

        QMetaObject.connectSlotsByName(PhotoluminescenceWidget)
    # setupUi

    def retranslateUi(self, PhotoluminescenceWidget):
        PhotoluminescenceWidget.setWindowTitle(QCoreApplication.translate("PhotoluminescenceWidget", u"Form", None))
        self.Status_Label.setText("")
        self.StopLivePL_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop Live PL", None))
        self.Snapshot_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Snapshot", None))
        self.StartLivePL_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start Live PL", None))
        self.SavePL_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Save PL", None))
        self.label_13.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start (\u00b0)", None))
        self.label_7.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop (\u00b0)", None))
        self.label_14.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Step (\u00b0)", None))
        self.Settings_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Settings...", None))
        self.PsStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.PsStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.StartPS_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start", None))
        self.StopPS_PushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop", None))
        self.PsStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.label_4.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Max Energy", None))
        self.BandwidthSweepEnable_CheckBox.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Bandwidth Seep Enable", None))
        self.label_3.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Min. Energy", None))
        self.label_5.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Overlap", None))
        self.BSPowerMajor_CheckBox.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Sweep Power-First (all windows per power step)", None))
        self.label_2.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Filename", None))
        self.label.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Directory", None))

    # retranslateUi

