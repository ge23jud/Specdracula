# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Map.ui'
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

from pyqtgraph import ImageView

class Ui_MapWidget(object):
    def setupUi(self, MapWidget):
        if not MapWidget.objectName():
            MapWidget.setObjectName(u"MapWidget")
        MapWidget.resize(1094, 787)
        self.verticalLayout = QVBoxLayout(MapWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(MapWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_11 = QVBoxLayout(self.widget_4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.img_view = ImageView(self.widget_4)
        self.img_view.setObjectName(u"img_view")
        self.img_view.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_view.sizePolicy().hasHeightForWidth())
        self.img_view.setSizePolicy(sizePolicy)

        self.verticalLayout_11.addWidget(self.img_view)

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
        self.label_4 = QLabel(self.widget_13)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)

        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.Stop_Button = QPushButton(self.widget_13)
        self.Stop_Button.setObjectName(u"Stop_Button")

        self.gridLayout.addWidget(self.Stop_Button, 6, 3, 1, 1)

        self.YStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.YStart_DoubleSpinBox.setObjectName(u"YStart_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.YStart_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.YStart_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.YStart_DoubleSpinBox.setMinimumSize(QSize(100, 10))
        self.YStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.YStart_DoubleSpinBox, 2, 1, 1, 2)

        self.label_3 = QLabel(self.widget_13)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.NumMeasurements_Label = QLabel(self.widget_13)
        self.NumMeasurements_Label.setObjectName(u"NumMeasurements_Label")
        sizePolicy3.setHeightForWidth(self.NumMeasurements_Label.sizePolicy().hasHeightForWidth())
        self.NumMeasurements_Label.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.NumMeasurements_Label, 5, 1, 1, 1)

        self.XStop_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.XStop_DoubleSpinBox.setObjectName(u"XStop_DoubleSpinBox")

        self.gridLayout.addWidget(self.XStop_DoubleSpinBox, 1, 3, 1, 1)

        self.YStop_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.YStop_DoubleSpinBox.setObjectName(u"YStop_DoubleSpinBox")
        self.YStop_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.YStop_DoubleSpinBox, 2, 3, 1, 1)

        self.label_13 = QLabel(self.widget_13)
        self.label_13.setObjectName(u"label_13")
        sizePolicy3.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_8 = QLabel(self.widget_13)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.Start_Button = QPushButton(self.widget_13)
        self.Start_Button.setObjectName(u"Start_Button")

        self.gridLayout.addWidget(self.Start_Button, 6, 1, 1, 2)

        self.XStart_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.XStart_DoubleSpinBox.setObjectName(u"XStart_DoubleSpinBox")
        self.XStart_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.XStart_DoubleSpinBox, 1, 1, 1, 2)

        self.XStep_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.XStep_DoubleSpinBox.setObjectName(u"XStep_DoubleSpinBox")
        sizePolicy2.setHeightForWidth(self.XStep_DoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.XStep_DoubleSpinBox.setSizePolicy(sizePolicy2)
        self.XStep_DoubleSpinBox.setMinimumSize(QSize(100, 25))
        self.XStep_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.XStep_DoubleSpinBox, 1, 4, 1, 1)

        self.YStep_DoubleSpinBox = QDoubleSpinBox(self.widget_13)
        self.YStep_DoubleSpinBox.setObjectName(u"YStep_DoubleSpinBox")

        self.gridLayout.addWidget(self.YStep_DoubleSpinBox, 2, 4, 1, 1)

        self.label_14 = QLabel(self.widget_13)
        self.label_14.setObjectName(u"label_14")
        sizePolicy3.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_14, 0, 4, 1, 1)

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


        self.verticalLayout_11.addWidget(self.SaveData)


        self.horizontalLayout.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(MapWidget)

        QMetaObject.connectSlotsByName(MapWidget)
    # setupUi

    def retranslateUi(self, MapWidget):
        MapWidget.setWindowTitle(QCoreApplication.translate("MapWidget", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("MapWidget", u"Stop", None))
        self.label_7.setText(QCoreApplication.translate("MapWidget", u"Y", None))
        self.Stop_Button.setText(QCoreApplication.translate("MapWidget", u"Stop", None))
        self.YStart_DoubleSpinBox.setSuffix("")
        self.label_3.setText(QCoreApplication.translate("MapWidget", u"Start", None))
        self.NumMeasurements_Label.setText(QCoreApplication.translate("MapWidget", u"45", None))
        self.label_13.setText(QCoreApplication.translate("MapWidget", u"X", None))
        self.label_8.setText(QCoreApplication.translate("MapWidget", u"Measurements", None))
        self.Start_Button.setText(QCoreApplication.translate("MapWidget", u"Start", None))
        self.XStart_DoubleSpinBox.setSuffix("")
        self.XStep_DoubleSpinBox.setSuffix("")
        self.label_14.setText(QCoreApplication.translate("MapWidget", u"Step", None))
        self.label_2.setText(QCoreApplication.translate("MapWidget", u"Filename", None))
        self.label.setText(QCoreApplication.translate("MapWidget", u"Directory", None))
    # retranslateUi

