import asyncio
import logging
import threading

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QMessageBox
from flask import Flask
from werkzeug.serving import make_server

from src.route.rt_index import register_index_routes
from src.view.ui_main import Ui_MainWindow

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WINDOW_TITLE = "蓝牙test-v0.0.1"
HTTP_SERVER_IP = '127.0.0.1'
HTTP_SERVER_PORT = 5001


# 蓝牙设备连接线程
# class BluetoothConnectThread(QThread):
    # 定义信号：连接成功、失败、心率数据更新
    # connect_success = Signal(str)  # 传递设备名称
    # connect_failed = Signal(str)  # 传递失败原因
    # heart_rate_update = Signal(int)  # 传递心率值
    #
    # def __init__(self):
    #     super().__init__()
    #     self.is_running = False
    #
    # def run(self):
    #     """线程执行体：运行蓝牙异步任务"""
    #     self.is_running = True
    #     try:
    #         # 运行异步蓝牙监控函数
    #         asyncio.run(run_hr_monitor())
    #     except Exception as e:
    #         err_msg = f"设备连接失败：{str(e)}"
    #         self.connect_failed.emit(err_msg)
    #         self.is_running = False
    #
    # def stop(self):
    #     """停止蓝牙连接线程"""
    #     self.is_running = False
    #     self.quit()
    #     self.wait()


class FlaskServerThread(QThread):
    start_success = Signal()
    start_failed = Signal(str)
    stop_success = Signal()

    def __init__(self, app: Flask):
        super().__init__()
        self.is_server_running = False
        self.app = app
        self.server = make_server(HTTP_SERVER_IP, HTTP_SERVER_PORT, self.app)
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

        self.init_slot()
        self.flask_thread: FlaskServerThread = None
        # self.bluetooth_thread: BluetoothConnectThread = None
        self.app = Flask(__name__)
        register_index_routes(self.app)

    def init_slot(self):
        # self.pushButton_connectDevice.clicked.connect(self.slot_pushButton_connectDevice)
        self.pushButton_openHttp.clicked.connect(self.slot_pushButton_openHttp)
        self.pushButton_closeHttp.clicked.connect(self.slot_pushButton_closeHttp)

    def slot_pushButton_connectDevice(self):
        logger.info("用户点击了连接设备按钮")
        # # 防止重复连接
        # if self.bluetooth_thread is not None and self.bluetooth_thread.is_running:
        #     QMessageBox.warning(self, "提示", "设备正在连接中，请勿重复点击！")
        #     return
        #
        # # 初始化并启动蓝牙线程
        # self.bluetooth_thread = BluetoothConnectThread()
        # # 绑定蓝牙线程信号
        # self.bluetooth_thread.connect_success.connect(
        #     lambda dev_name: QMessageBox.information(self, "成功", f"已连接到设备：{dev_name}")
        # )
        # self.bluetooth_thread.connect_failed.connect(
        #     lambda msg: QMessageBox.critical(self, "失败", msg)
        # )
        # # （可选）绑定心率更新信号，用于UI显示心率
        # # self.bluetooth_thread.heart_rate_update.connect(self.update_heart_rate_ui)
        #
        # # 启动蓝牙线程
        # self.bluetooth_thread.start()
        # logger.info("蓝牙设备连接线程已启动，开始扫描设备...")

    def slot_pushButton_openHttp(self):
        logger.info("用户点击了开启http按钮")

        # 防止重复启动
        if self.flask_thread is not None:
            if self.flask_thread.is_server_running:
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

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.slot_pushButton_closeHttp()
        logger.info("程序正常退出,closeEvent")
        exit(0)
