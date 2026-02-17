# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'xymeasurement.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_XYMeasurementWidget(object):
    def setupUi(self, XYMeasurementWidget):
        if not XYMeasurementWidget.objectName():
            XYMeasurementWidget.setObjectName(u"XYMeasurementWidget")
        XYMeasurementWidget.resize(1094, 780)
        self.verticalLayout = QVBoxLayout(XYMeasurementWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(XYMeasurementWidget)
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
        self.label_8 = QLabel(self.widget_13)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)

        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName(u"label_7")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)

        self.SweepStep_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.SweepStep_DoubleSpinBox.setObjectName(u"SweepStep_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.SweepStep_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.SweepStep_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.SweepStep_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.SweepStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.SweepStep_DoubleSpinBox, 2, 2, 1, 2)

        self.SweepStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.SweepStart_DoubleSpinBox.setObjectName(u"SweepStart_DoubleSpinBox")
        self.SweepStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.SweepStart_DoubleSpinBox, 0, 2, 1, 2)

        self.label_14 = QLabel(self.widget_13)
        self.label_14.setObjectName(u"label_14")
        sizePolicy4.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.label_14, 2, 1, 1, 1)

        self.SweepStop_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.SweepStop_DoubleSpinBox.setObjectName(u"SweepStop_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.SweepStop_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.SweepStop_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.SweepStop_DoubleSpinBox.setMinimumSize(QSize(100, 10))
        self.SweepStop_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.SweepStop_DoubleSpinBox, 1, 2, 1, 2)

        self.label_13 = QLabel(self.widget_13)
        self.label_13.setObjectName(u"label_13")
        sizePolicy4.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.label_13, 0, 1, 1, 1)

        self.NumMeasurements_Label = QLabel(self.widget_13)
        self.NumMeasurements_Label.setObjectName(u"NumMeasurements_Label")
        sizePolicy4.setHeightForWidth(self.NumMeasurements_Label.sizePolicy().hasHeightForWidth())
        self.NumMeasurements_Label.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.NumMeasurements_Label, 4, 2, 1, 1)

        self.label_3 = QLabel(self.widget_13)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.SweepParameter_ComboBox = QComboBox(self.widget_13)
        self.SweepParameter_ComboBox.addItem("")
        self.SweepParameter_ComboBox.addItem("")
        self.SweepParameter_ComboBox.addItem("")
        self.SweepParameter_ComboBox.setObjectName(u"SweepParameter_ComboBox")

        self.gridLayout.addWidget(self.SweepParameter_ComboBox, 1, 0, 1, 1)

        self.label_4 = QLabel(self.widget_13)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.MeasuredParameter_ComboBox = QComboBox(self.widget_13)
        self.MeasuredParameter_ComboBox.addItem("")
        self.MeasuredParameter_ComboBox.addItem("")
        self.MeasuredParameter_ComboBox.setObjectName(u"MeasuredParameter_ComboBox")

        self.gridLayout.addWidget(self.MeasuredParameter_ComboBox, 4, 0, 1, 1)

        self.Start_Button = QPushButton(self.widget_13)
        self.Start_Button.setObjectName(u"Start_Button")
        sizePolicy1.setHeightForWidth(self.Start_Button.sizePolicy().hasHeightForWidth())
        self.Start_Button.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.Start_Button, 6, 0, 1, 4)

        self.Stop_Button = QPushButton(self.widget_13)
        self.Stop_Button.setObjectName(u"Stop_Button")
        sizePolicy1.setHeightForWidth(self.Stop_Button.sizePolicy().hasHeightForWidth())
        self.Stop_Button.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.Stop_Button, 7, 0, 1, 4)

        self.gridLayout.setColumnStretch(0, 1)

        self.horizontalLayout_2.addWidget(self.widget_13)

        self.widget_2 = QWidget(self.SaveData)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.Directory_LineEdit = QLineEdit(self.widget_2)
        self.Directory_LineEdit.setObjectName(u"Directory_LineEdit")

        self.gridLayout_2.addWidget(self.Directory_LineEdit, 0, 1, 1, 1)

        self.Filename_LineEdit = QLineEdit(self.widget_2)
        self.Filename_LineEdit.setObjectName(u"Filename_LineEdit")

        self.gridLayout_2.addWidget(self.Filename_LineEdit, 1, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.SaveData)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy5)
        self.widget_3.setMinimumSize(QSize(200, 0))
        self.gridLayout_3 = QGridLayout(self.widget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.xlabel_ComboBox = QComboBox(self.widget_3)
        self.xlabel_ComboBox.addItem("")
        self.xlabel_ComboBox.addItem("")
        self.xlabel_ComboBox.setObjectName(u"xlabel_ComboBox")
        self.xlabel_ComboBox.setMinimumSize(QSize(150, 0))
        self.xlabel_ComboBox.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.xlabel_ComboBox, 3, 1, 1, 1)

        self.label_23 = QLabel(self.widget_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_23, 2, 0, 1, 1)

        self.label_24 = QLabel(self.widget_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_24, 3, 0, 1, 1)

        self.yscale_ComboBox = QComboBox(self.widget_3)
        self.yscale_ComboBox.addItem("")
        self.yscale_ComboBox.addItem("")
        self.yscale_ComboBox.setObjectName(u"yscale_ComboBox")
        self.yscale_ComboBox.setMinimumSize(QSize(150, 0))
        self.yscale_ComboBox.setMaximumSize(QSize(100, 16777215))
        self.yscale_ComboBox.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.yscale_ComboBox.setFrame(True)

        self.gridLayout_3.addWidget(self.yscale_ComboBox, 2, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widget_3)


        self.verticalLayout_11.addWidget(self.SaveData)


        self.horizontalLayout.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(XYMeasurementWidget)

        QMetaObject.connectSlotsByName(XYMeasurementWidget)
    # setupUi

    def retranslateUi(self, XYMeasurementWidget):
        XYMeasurementWidget.setWindowTitle(QCoreApplication.translate("XYMeasurementWidget", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("XYMeasurementWidget", u"Measurements", None))
        self.label_7.setText(QCoreApplication.translate("XYMeasurementWidget", u"Stop (\u00b0)", None))
        self.SweepStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("XYMeasurementWidget", u"\u00b0", None))
        self.SweepStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("XYMeasurementWidget", u"\u00b0", None))
        self.label_14.setText(QCoreApplication.translate("XYMeasurementWidget", u"Step (\u00b0)", None))
        self.SweepStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("XYMeasurementWidget", u"\u00b0", None))
        self.label_13.setText(QCoreApplication.translate("XYMeasurementWidget", u"Start (\u00b0)", None))
        self.NumMeasurements_Label.setText(QCoreApplication.translate("XYMeasurementWidget", u"45", None))
        self.label_3.setText(QCoreApplication.translate("XYMeasurementWidget", u"Sweep Parameter", None))
        self.SweepParameter_ComboBox.setItemText(0, QCoreApplication.translate("XYMeasurementWidget", u"Power HWP Position", None))
        self.SweepParameter_ComboBox.setItemText(1, QCoreApplication.translate("XYMeasurementWidget", u"Piezo X", None))
        self.SweepParameter_ComboBox.setItemText(2, QCoreApplication.translate("XYMeasurementWidget", u"Piezo Y", None))

        self.label_4.setText(QCoreApplication.translate("XYMeasurementWidget", u"Measured Parameter", None))
        self.MeasuredParameter_ComboBox.setItemText(0, QCoreApplication.translate("XYMeasurementWidget", u"Photoluminescence", None))
        self.MeasuredParameter_ComboBox.setItemText(1, QCoreApplication.translate("XYMeasurementWidget", u"Power", None))

        self.Start_Button.setText(QCoreApplication.translate("XYMeasurementWidget", u"Start", None))
        self.Stop_Button.setText(QCoreApplication.translate("XYMeasurementWidget", u"Stop", None))
        self.label_2.setText(QCoreApplication.translate("XYMeasurementWidget", u"Filename", None))
        self.label.setText(QCoreApplication.translate("XYMeasurementWidget", u"Directory", None))
        self.xlabel_ComboBox.setItemText(0, QCoreApplication.translate("XYMeasurementWidget", u"Energy", None))
        self.xlabel_ComboBox.setItemText(1, QCoreApplication.translate("XYMeasurementWidget", u"Wavelength", None))

        self.label_23.setText(QCoreApplication.translate("XYMeasurementWidget", u"Scale", None))
        self.label_24.setText(QCoreApplication.translate("XYMeasurementWidget", u"X-axis", None))
        self.yscale_ComboBox.setItemText(0, QCoreApplication.translate("XYMeasurementWidget", u"Linear", None))
        self.yscale_ComboBox.setItemText(1, QCoreApplication.translate("XYMeasurementWidget", u"Logarithmic", None))

    # retranslateUi

