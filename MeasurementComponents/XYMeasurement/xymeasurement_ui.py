# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'XYMeasurement.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_XYMeasurementWidget(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1094, 780)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 10)
        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 15))
        self.label_6.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_4.addWidget(self.label_6)

        self.comboBox = QComboBox(self.widget_3)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_4.addWidget(self.comboBox)

        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 15))

        self.verticalLayout_4.addWidget(self.label_7)

        self.comboBox_2 = QComboBox(self.widget_3)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.verticalLayout_4.addWidget(self.comboBox_2)

        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_8 = QWidget(self.widget_6)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(100, 0))
        self.widget_8.setMaximumSize(QSize(120, 200))
        self.verticalLayout_5 = QVBoxLayout(self.widget_8)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textEdit_4 = QTextEdit(self.widget_8)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.textEdit_4)

        self.textEdit_5 = QTextEdit(self.widget_8)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.textEdit_5)

        self.textEdit_6 = QTextEdit(self.widget_8)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.textEdit_6)

        self.textEdit_7 = QTextEdit(self.widget_8)
        self.textEdit_7.setObjectName(u"textEdit_7")
        self.textEdit_7.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.textEdit_7)

        self.textEdit_8 = QTextEdit(self.widget_8)
        self.textEdit_8.setObjectName(u"textEdit_8")
        self.textEdit_8.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.textEdit_8)


        self.horizontalLayout_3.addWidget(self.widget_8)

        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(0, 0))
        self.widget_7.setMaximumSize(QSize(110, 200))
        self.verticalLayout_6 = QVBoxLayout(self.widget_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.widget_7)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_6.addWidget(self.label_8)

        self.label_9 = QLabel(self.widget_7)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_6.addWidget(self.label_9)

        self.label_10 = QLabel(self.widget_7)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_6.addWidget(self.label_10)

        self.label_11 = QLabel(self.widget_7)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAutoFillBackground(False)
        self.label_11.setTextFormat(Qt.TextFormat.AutoText)
        self.label_11.setWordWrap(False)

        self.verticalLayout_6.addWidget(self.label_11)

        self.label_12 = QLabel(self.widget_7)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_6.addWidget(self.label_12)


        self.horizontalLayout_3.addWidget(self.widget_7)


        self.verticalLayout_4.addWidget(self.widget_6)

        self.widget_9 = QWidget(self.widget_3)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.widget_9)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_9)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_4.addWidget(self.pushButton_2)


        self.verticalLayout_4.addWidget(self.widget_9)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_11 = QVBoxLayout(self.widget_4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.widget_11 = QWidget(self.widget_4)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setMaximumSize(QSize(16777215, 60))
        self.verticalLayout_12 = QVBoxLayout(self.widget_11)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_13 = QLabel(self.widget_11)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(100, 16777215))
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_13)

        self.comboBox_3 = QComboBox(self.widget_11)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setMaximumSize(QSize(100, 16777215))
        self.comboBox_3.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.comboBox_3.setFrame(False)

        self.verticalLayout_12.addWidget(self.comboBox_3)


        self.verticalLayout_11.addWidget(self.widget_11)

        self.widget_10 = QWidget(self.widget_4)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setEnabled(True)

        self.verticalLayout_11.addWidget(self.widget_10)

        self.widget_12 = QWidget(self.widget_4)
        self.widget_12.setObjectName(u"widget_12")
        self.widget_12.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_5 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.widget_12)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_5.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.widget_12)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.widget_12)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.verticalLayout_11.addWidget(self.widget_12)


        self.horizontalLayout.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)

        self.SaveData = QWidget(Form)
        self.SaveData.setObjectName(u"SaveData")
        self.SaveData.setMaximumSize(QSize(16777215, 150))
        self.horizontalLayout_2 = QHBoxLayout(self.SaveData)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_2 = QWidget(self.SaveData)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 15))

        self.verticalLayout_2.addWidget(self.label)

        self.textEdit = QTextEdit(self.widget_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.textEdit)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 15))

        self.verticalLayout_2.addWidget(self.label_2)

        self.textEdit_2 = QTextEdit(self.widget_2)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.textEdit_2)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 15))

        self.verticalLayout_2.addWidget(self.label_3)

        self.textEdit_3 = QTextEdit(self.widget_2)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.textEdit_3)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.widget_5 = QWidget(self.SaveData)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_3 = QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.textBrowser = QTextBrowser(self.widget_5)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.textBrowser_2 = QTextBrowser(self.widget_5)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_3.addWidget(self.textBrowser_2)


        self.horizontalLayout_2.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.SaveData)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Sweep Parameter", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Power HWP Position", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"Measurement Parameter", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"Photoluminescence", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"Power", None))

        self.label_8.setText(QCoreApplication.translate("Form", u"Start (\u00b0)", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Stop (\u00b0)", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Step (\u00b0)", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Measurements", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Integration Time (s)", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Scale", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"Linear", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"Logarithmic", None))

        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PL Snapshot", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"Real Time PL", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.label.setText(QCoreApplication.translate("Form", u"Directory", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"File Name", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"File Number", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Next File", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Displayed File", None))
    # retranslateUi

