# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(277, 104)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_connectDevice = QPushButton(self.centralwidget)
        self.pushButton_connectDevice.setObjectName(u"pushButton_connectDevice")

        self.verticalLayout.addWidget(self.pushButton_connectDevice)

        self.pushButton_openHttp = QPushButton(self.centralwidget)
        self.pushButton_openHttp.setObjectName(u"pushButton_openHttp")

        self.verticalLayout.addWidget(self.pushButton_openHttp)

        self.pushButton_closeHttp = QPushButton(self.centralwidget)
        self.pushButton_closeHttp.setObjectName(u"pushButton_closeHttp")

        self.verticalLayout.addWidget(self.pushButton_closeHttp)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_connectDevice.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u5fc3\u7387\u8bbe\u5907", None))
        self.pushButton_openHttp.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542fhttp\u670d\u52a1", None))
        self.pushButton_closeHttp.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95edhttp\u670d\u52a1", None))
    # retranslateUi

