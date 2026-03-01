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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(652, 274)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tableWidget_devicesList = QTableWidget(self.groupBox_2)
        if (self.tableWidget_devicesList.columnCount() < 2):
            self.tableWidget_devicesList.setColumnCount(2)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tableWidget_devicesList.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tableWidget_devicesList.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget_devicesList.setObjectName(u"tableWidget_devicesList")
        self.tableWidget_devicesList.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_devicesList.horizontalHeader().setVisible(True)

        self.gridLayout_2.addWidget(self.tableWidget_devicesList, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.pushButton_scanDevice = QPushButton(self.centralwidget)
        self.pushButton_scanDevice.setObjectName(u"pushButton_scanDevice")

        self.verticalLayout.addWidget(self.pushButton_scanDevice)

        self.lineEdit_deviceAddress = QLineEdit(self.centralwidget)
        self.lineEdit_deviceAddress.setObjectName(u"lineEdit_deviceAddress")
        self.lineEdit_deviceAddress.setReadOnly(False)

        self.verticalLayout.addWidget(self.lineEdit_deviceAddress)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_connectDevice = QPushButton(self.centralwidget)
        self.pushButton_connectDevice.setObjectName(u"pushButton_connectDevice")

        self.horizontalLayout_3.addWidget(self.pushButton_connectDevice)

        self.pushButton_disconnectDevice = QPushButton(self.centralwidget)
        self.pushButton_disconnectDevice.setObjectName(u"pushButton_disconnectDevice")

        self.horizontalLayout_3.addWidget(self.pushButton_disconnectDevice)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.pushButton_openHttp = QPushButton(self.centralwidget)
        self.pushButton_openHttp.setObjectName(u"pushButton_openHttp")

        self.verticalLayout.addWidget(self.pushButton_openHttp)

        self.pushButton_closeHttp = QPushButton(self.centralwidget)
        self.pushButton_closeHttp.setObjectName(u"pushButton_closeHttp")

        self.verticalLayout.addWidget(self.pushButton_closeHttp)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser_log = QTextBrowser(self.groupBox)
        self.textBrowser_log.setObjectName(u"textBrowser_log")

        self.gridLayout.addWidget(self.textBrowser_log, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u5217\u8868", None))
        ___qtablewidgetitem = self.tableWidget_devicesList.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tableWidget_devicesList.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u5730\u5740", None));
        self.pushButton_scanDevice.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u9644\u8fd1\u5fc3\u7387\u8bbe\u5907", None))
        self.lineEdit_deviceAddress.setInputMask("")
        self.lineEdit_deviceAddress.setText("")
        self.lineEdit_deviceAddress.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u84dd\u7259\u8bbe\u5907\u5730\u5740", None))
        self.pushButton_connectDevice.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u8bbe\u5907", None))
        self.pushButton_disconnectDevice.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00\u8bbe\u5907", None))
        self.pushButton_openHttp.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542fhttp\u670d\u52a1", None))
        self.pushButton_closeHttp.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95edhttp\u670d\u52a1", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\u6846", None))
    # retranslateUi

