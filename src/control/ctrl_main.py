from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow

from src.view.view_main import Ui_MainWindow


class MainApp(QMainWindow, Ui_MainWindow):
    # 槽
    def init_slot(self):
        self.pushButton_connectDevice.clicked.connect(self.slot_pushButton_connectDevice)
        self.pushButton_openHttp.clicked.connect(self.slot_pushButton_openHttp)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('蓝牙test-v0.0.1')
        self.init_slot()

    def closeEvent(self, a0):
        super().closeEvent(a0)
        exit(0)

    def slot_pushButton_connectDevice(self):
        print(1)

    def slot_pushButton_openHttp(self):
        print(2)

    def add_log(self, status, message):
        """
        打印日志
        :param status: 状态信息
        :param message: 日志消息内容
        :return: None
        """
        color = 'black'
        if status == "SUCCESS":
            color = 'green'
        elif status == 'PROCESS':
            color = 'black'
        elif status == "ERROR":
            color = 'red'
        elif status == "WARNING":
            color = 'blue'
        # 获取当前时间
        current_time = QDateTime.currentDateTime().toString('HH:mm:ss')
        # 组装log信息
        log_message = f'<span style="color: {color};">{current_time} - {message}</span>'
        # 添加日志信息到 QTextBrowser
        self.textBrowser_log_show.append(log_message)