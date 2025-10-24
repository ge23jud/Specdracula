# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QPushButton, QSizePolicy,
    QWidget)

class Ui_BennisModule(object):
    def setupUi(self, BennisModule):
        if not BennisModule.objectName():
            BennisModule.setObjectName(u"BennisModule")
        BennisModule.resize(400, 300)
        self.groupBox = QGroupBox(BennisModule)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(60, 110, 120, 80))
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(50, 30, 79, 24))

        self.retranslateUi(BennisModule)

        QMetaObject.connectSlotsByName(BennisModule)
    # setupUi

    def retranslateUi(self, BennisModule):
        BennisModule.setWindowTitle(QCoreApplication.translate("BennisModule", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("BennisModule", u"GroupBox", None))
        self.pushButton.setText(QCoreApplication.translate("BennisModule", u"PushButton", None))
    # retranslateUi

