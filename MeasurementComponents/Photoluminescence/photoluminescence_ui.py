# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Photoluminescence.ui'
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
        self.pushButton_4 = QPushButton(self.widget_13)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 7, 3, 1, 1)

        self.pushButton_5 = QPushButton(self.widget_13)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 0, 3, 1, 1)

        self.pushButton_3 = QPushButton(self.widget_13)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 6, 3, 1, 1)

        self.pushButton_6 = QPushButton(self.widget_13)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout.addWidget(self.pushButton_6, 1, 3, 1, 1)

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

        self.label_8 = QLabel(self.widget_13)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.NumMeasurements_Label = QLabel(self.widget_13)
        self.NumMeasurements_Label.setObjectName(u"NumMeasurements_Label")
        sizePolicy3.setHeightForWidth(self.NumMeasurements_Label.sizePolicy().hasHeightForWidth())
        self.NumMeasurements_Label.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.NumMeasurements_Label, 4, 1, 1, 1)

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

        self.pushButton = QPushButton(self.widget_13)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 3)

        self.pushButton_2 = QPushButton(self.widget_13)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pushButton_2, 7, 0, 1, 3)

        self.PsStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.PsStart_DoubleSpinBox.setObjectName(u"PsStart_DoubleSpinBox")
        self.PsStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.PsStart_DoubleSpinBox, 0, 1, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

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

        self.lineEdit = QLineEdit(self.widget_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)


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


        self.retranslateUi(PhotoluminescenceWidget)

        QMetaObject.connectSlotsByName(PhotoluminescenceWidget)
    # setupUi

    def retranslateUi(self, PhotoluminescenceWidget):
        PhotoluminescenceWidget.setWindowTitle(QCoreApplication.translate("PhotoluminescenceWidget", u"Form", None))
        self.pushButton_4.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop Live PL", None))
        self.pushButton_5.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Snapshot", None))
        self.pushButton_3.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start Live PL", None))
        self.pushButton_6.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Save PL", None))
        self.label_13.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start (\u00b0)", None))
        self.label_7.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop (\u00b0)", None))
        self.label_14.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Step (\u00b0)", None))
        self.label_8.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Measurements", None))
        self.NumMeasurements_Label.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"45", None))
        self.PsStop_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.PsStep_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.pushButton.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Start", None))
        self.pushButton_2.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Stop", None))
        self.PsStart_DoubleSpinBox.setSuffix(QCoreApplication.translate("PhotoluminescenceWidget", u"\u00b0", None))
        self.label_2.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Filename", None))
        self.label.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Directory", None))
        self.xlabel_ComboBox.setItemText(0, QCoreApplication.translate("PhotoluminescenceWidget", u"Energy", None))
        self.xlabel_ComboBox.setItemText(1, QCoreApplication.translate("PhotoluminescenceWidget", u"Wavelength", None))

        self.label_23.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"Scale", None))
        self.label_24.setText(QCoreApplication.translate("PhotoluminescenceWidget", u"X-axis", None))
        self.yscale_ComboBox.setItemText(0, QCoreApplication.translate("PhotoluminescenceWidget", u"Linear", None))
        self.yscale_ComboBox.setItemText(1, QCoreApplication.translate("PhotoluminescenceWidget", u"Logarithmic", None))

    # retranslateUi

