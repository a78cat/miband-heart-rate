import logging
import sys
import threading
from typing import Optional

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow, QMessageBox
from flask import Flask
from werkzeug.serving import make_server

from src.route.rt_index import register_index_routes
from src.view.ui_main import Ui_MainWindow

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# 常量定义
WINDOW_TITLE = "蓝牙test-v0.0.1"
HTTP_SERVER_PORT = 5001  # 假设FlaskServer使用5000端口，可根据实际调整


class FlaskServerThread(QThread):
    start_success = Signal()
    start_failed = Signal(str)
    stop_success = Signal()

    def __init__(self, app: Flask):
        super().__init__()
        self.is_server_running = False
        self.app = app
        self.server = make_server('127.0.0.1', HTTP_SERVER_PORT, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever)

    def run(self):
        """线程执行体：启动Flask服务"""
        try:
            self.thread.start()
            self.is_server_running = True
            self.start_success.emit()
            logger.info(f"HTTP服务启动成功，端口：{HTTP_SERVER_PORT}")
            # 阻塞线程直到服务停止
        except Exception as e:
            err_msg = f"HTTP服务启动失败：{str(e)}"
            logger.error(err_msg)
            self.start_failed.emit(err_msg)

    def stop_server(self):
        """停止Flask服务"""
        if self.server:
            try:
                self.server.shutdown()
                self.stop_success.emit()
                logger.info("HTTP服务停止成功")
            except Exception as e:
                logger.error(f"HTTP服务停止失败：{str(e)}")


class MainApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.init_slot()
        self.flask_thread: FlaskServerThread = None
        self.app = Flask(__name__)
        register_index_routes(self.app)

    def init_slot(self):
        # self.pushButton_connectDevice.clicked.connect(self)
        self.pushButton_openHttp.clicked.connect(self.slot_pushButton_openHttp)
        self.pushButton_closeHttp.clicked.connect(self.slot_pushButton_closeHttp)
        self.pushButton_quit.clicked.connect(self.slot_pushButton_quit)

    def slot_pushButton_openHttp(self):
        logger.info("点击了开启http按钮")
        print(self.flask_thread)

        # 防止重复启动
        if self.flask_thread is not None:
            print('ok1')
            if self.flask_thread.is_server_running:
                print('ok2')
                QMessageBox.warning(self, "提示", "HTTP服务已启动，请勿重复点击！")
                return

        self.flask_thread = FlaskServerThread(self.app)
        # 绑定线程信号
        self.flask_thread.start_success.connect(
            lambda: QMessageBox.information(self, "成功", "HTTP服务启动成功！")
        )
        self.flask_thread.start_failed.connect(
            lambda msg: QMessageBox.critical(self, "失败", msg)
        )
        self.flask_thread.start()

        print(self.flask_thread)
        print(self.flask_thread.isRunning())

    def slot_pushButton_closeHttp(self):
        logger.info("用户点击关闭http按钮")
        if self.flask_thread is None:
            logger.info("没有flask_thread")
            return
        if self.flask_thread.is_server_running:
            self.flask_thread.stop_server()
            self.flask_thread.quit()
            self.flask_thread.wait()
            self.flask_thread = None
            QMessageBox.information(self, "提示", "HTTP服务已关闭！")
            logger.info("关闭成功")
            return

    def slot_pushButton_quit(self):
        self.slot_pushButton_closeHttp()
        logger.info("程序正常退出,slot_pushButton_quit")
        sys.exit(0)

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.slot_pushButton_closeHttp()
        logger.info("程序正常退出,closeEvent")
        exit(0)
