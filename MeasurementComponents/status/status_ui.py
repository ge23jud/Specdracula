# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'status.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_StatusWidget(object):
    def setupUi(self, StatusWidget):
        if not StatusWidget.objectName():
            StatusWidget.setObjectName(u"StatusWidget")
        StatusWidget.resize(400, 270)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StatusWidget.sizePolicy().hasHeightForWidth())
        StatusWidget.setSizePolicy(sizePolicy)
        StatusWidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(StatusWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, 18, -1)
        self.line = QFrame(StatusWidget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 3))
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.groupBox = QGroupBox(StatusWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 50))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.Power_Label = QLabel(self.groupBox)
        self.Power_Label.setObjectName(u"Power_Label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Power_Label.sizePolicy().hasHeightForWidth())
        self.Power_Label.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.Power_Label.setFont(font)
        self.Power_Label.setStyleSheet(u"QLabel {\n"
"    background-color: white;\n"
"    color: black;\n"
"    font-size: 20pt;\n"
"    padding: 5px;\n"
"}")
        self.Power_Label.setTextFormat(Qt.TextFormat.RichText)
        self.Power_Label.setScaledContents(False)
        self.Power_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Power_Label.setMargin(0)

        self.verticalLayout_2.addWidget(self.Power_Label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_4)

        self.Temperature_Label = QLabel(self.groupBox)
        self.Temperature_Label.setObjectName(u"Temperature_Label")
        sizePolicy2.setHeightForWidth(self.Temperature_Label.sizePolicy().hasHeightForWidth())
        self.Temperature_Label.setSizePolicy(sizePolicy2)
        self.Temperature_Label.setFont(font)
        self.Temperature_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.Temperature_Label)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(StatusWidget)

        QMetaObject.connectSlotsByName(StatusWidget)
    # setupUi

    def retranslateUi(self, StatusWidget):
        StatusWidget.setWindowTitle(QCoreApplication.translate("StatusWidget", u"Form", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("StatusWidget", u"Power (mW)", None))
        self.Power_Label.setText(QCoreApplication.translate("StatusWidget", u"1.294", None))
        self.label_4.setText(QCoreApplication.translate("StatusWidget", u"Temperature (K)", None))
        self.Temperature_Label.setText(QCoreApplication.translate("StatusWidget", u"300", None))
    # retranslateUi

