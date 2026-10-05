# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PowerCalibration.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_PowerCalibrationWidget(object):
    def setupUi(self, PowerCalibrationWidget):
        if not PowerCalibrationWidget.objectName():
            PowerCalibrationWidget.setObjectName(u"PowerCalibrationWidget")
        PowerCalibrationWidget.resize(1094, 780)
        self.verticalLayout = QVBoxLayout(PowerCalibrationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(PowerCalibrationWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_11 = QVBoxLayout(self.widget_4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
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
        self.NumMeasurements_Label = QLabel(self.widget_13)
        self.NumMeasurements_Label.setObjectName(u"NumMeasurements_Label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.NumMeasurements_Label.sizePolicy().hasHeightForWidth())
        self.NumMeasurements_Label.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.NumMeasurements_Label, 4, 1, 1, 1)

        self.PsStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.PsStart_DoubleSpinBox.setObjectName(u"PsStart_DoubleSpinBox")
        self.PsStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStart_DoubleSpinBox, 0, 1, 1, 2)

        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.StopPS_PushButton = QPushButton(self.widget_13)
        self.StopPS_PushButton.setObjectName(u"StopPS_PushButton")
        sizePolicy1.setHeightForWidth(self.StopPS_PushButton.sizePolicy().hasHeightForWidth())
        self.StopPS_PushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.StopPS_PushButton, 7, 0, 1, 3)

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

        self.label_13 = QLabel(self.widget_13)
        self.label_13.setObjectName(u"label_13")
        sizePolicy3.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_14 = QLabel(self.widget_13)
        self.label_14.setObjectName(u"label_14")
        sizePolicy3.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_8 = QLabel(self.widget_13)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_SettleTime = QLabel(self.widget_13)
        self.label_SettleTime.setObjectName(u"label_SettleTime")
        sizePolicy3.setHeightForWidth(self.label_SettleTime.sizePolicy().hasHeightForWidth())
        self.label_SettleTime.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_SettleTime, 3, 0, 1, 1)

        self.SettleTime_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.SettleTime_DoubleSpinBox.setObjectName(u"SettleTime_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.SettleTime_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.SettleTime_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.SettleTime_DoubleSpinBox.setMinimumSize(QSize(100, 10))
        self.SettleTime_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.SettleTime_DoubleSpinBox, 3, 1, 1, 2)

        self.label_AveragingTime = QLabel(self.widget_13)
        self.label_AveragingTime.setObjectName(u"label_AveragingTime")
        sizePolicy3.setHeightForWidth(self.label_AveragingTime.sizePolicy().hasHeightForWidth())
        self.label_AveragingTime.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_AveragingTime, 5, 0, 1, 1)

        self.AveragingTime_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.AveragingTime_DoubleSpinBox.setObjectName(u"AveragingTime_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.AveragingTime_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.AveragingTime_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.AveragingTime_DoubleSpinBox.setMinimumSize(QSize(100, 10))
        self.AveragingTime_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.AveragingTime_DoubleSpinBox, 5, 1, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)

        self.horizontalLayout_2.addWidget(self.widget_13)

        self.widget_2 = QWidget(self.SaveData)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.Filename_LineEdit = QLineEdit(self.widget_2)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout_2.addWidget(self.Filename_LineEdit, 1, 1, 1, 1)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.widget_2)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout_2.addWidget(self.Directory_LineEdit, 0, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widget_2)


        self.verticalLayout_11.addWidget(self.SaveData)


        self.horizontalLayout.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(PowerCalibrationWidget)

        QMetaObject.connectSlotsByName(PowerCalibrationWidget)
    # setupUi

    def retranslateUi(self, PowerCalibrationWidget):
        PowerCalibrationWidget.setWindowTitle(QCoreApplication.translate("PowerCalibrationWidget", u"Form", None))
        self.NumMeasurements_Label.setText(QCoreApplication.translate("PowerCalibrationWidget", u"45", None))
        self.PsStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("PowerCalibrationWidget", u"\u00b0", None))
        self.label_7.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Stop (\u00b0)", None))
        self.StopPS_PushButton.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Stop", None))
        self.PsStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("PowerCalibrationWidget", u"\u00b0", None))
        self.PsStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("PowerCalibrationWidget", u"\u00b0", None))
        self.StartPS_PushButton.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Start", None))
        self.label_13.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Start (\u00b0)", None))
        self.label_14.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Step (\u00b0)", None))
        self.label_8.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Measurements", None))
        self.label_SettleTime.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Settle Time (s)", None))
        self.SettleTime_DoubleSpinBox.setSuffix(QCoreApplication.translate("PowerCalibrationWidget", u"s", None))
        self.label_AveragingTime.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Averaging Time (s)", None))
        self.AveragingTime_DoubleSpinBox.setSuffix(QCoreApplication.translate("PowerCalibrationWidget", u"s", None))
        self.label.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Directory", None))
        self.label_2.setText(QCoreApplication.translate("PowerCalibrationWidget", u"Filename", None))
    # retranslateUi

