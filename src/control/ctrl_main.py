import logging

from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel
from flask import Flask

from src.model.thread_connect_bluetooth_device import ConnectBluetoothDeviceThread, ScanBluetoothDevicesThread
from src.model.thread_flask_server import FlaskServerThread
from src.route.rt_index import register_index_routes
from src.view.ui_main import Ui_MainWindow

WINDOW_TITLE = "蓝牙test-v0.0.1"
logger = logging.getLogger(__name__)


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(self.size())

        # tableWidget_devicesList
        self.tableWidget_devicesList.verticalHeader().setVisible(False)
        self.tableWidget_devicesList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_devicesList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # pushbutton 按钮绑定
        self.pushButton_scanDevice.clicked.connect(self.slot_pushButton_scanDevice)
        self.pushButton_connectDevice.clicked.connect(self.slot_pushButton_connectDevice)
        self.pushButton_disconnectDevice.clicked.connect(self.slot_pushButton_disconnectDevice)
        self.pushButton_openHttp.clicked.connect(self.slot_pushButton_openHttp)
        self.pushButton_closeHttp.clicked.connect(self.slot_pushButton_closeHttp)
        # 初始化线程
        self.thread_flask: FlaskServerThread = None
        self.thread_scan_bluetooth_devices: ScanBluetoothDevicesThread = None
        self.thread_connect_device: ConnectBluetoothDeviceThread = None

    def slot_pushButton_scanDevice(self):
        logger.info("用户点击了按钮-扫描设备")
        self.textBrowser_log.append('扫描中，等待3秒')

        def devices_list_process(data: list):
            # self.tableWidget_devicesList.resizeColumnsToContents()
            for i in data:
                logger.info(i[0] + ' ' + i[1])
                row = self.tableWidget_devicesList.rowCount()
                self.tableWidget_devicesList.insertRow(row)
                self.tableWidget_devicesList.setItem(row, 0, QTableWidgetItem(i[0]))
                self.tableWidget_devicesList.setItem(row, 1, QTableWidgetItem(i[1]))
            self.textBrowser_log.append(f'扫描完成，找到{self.tableWidget_devicesList.rowCount()}个设备')

        self.tableWidget_devicesList.setRowCount(0)
        self.thread_scan_bluetooth_devices = ScanBluetoothDevicesThread()
        self.thread_scan_bluetooth_devices.start()
        self.thread_scan_bluetooth_devices.signal_devices_list.connect(devices_list_process)

    def slot_pushButton_connectDevice(self):
        logger.info("用户点击了按钮-连接设备")
        self.textBrowser_log.append(f'连接中')

        self.thread_connect_device = ConnectBluetoothDeviceThread(self.lineEdit_deviceAddress.text())

        self.thread_connect_device.signal_hart_rate_data.connect(
            lambda data: self.statusBar_heartRate.showMessage(f'当前心率: {str(data)}')
        )
        self.thread_connect_device.signal_status.connect(
            lambda data: self.textBrowser_log.append(str(data))
        )
        self.thread_connect_device.start()

    def slot_pushButton_disconnectDevice(self):
        logger.info("用户点击了按钮-断开设备")
        self.textBrowser_log.append(f'断开连接中...')

        if self.thread_connect_device and self.thread_connect_device.isRunning():
            self.thread_connect_device.stop()
            self.textBrowser_log.append("已停止接收心率数据")
        else:
            self.textBrowser_log.append("当前无正在运行的蓝牙连接")

    def slot_pushButton_openHttp(self):
        logger.info("用户点击了开启http按钮")

        # 防止重复启动
        if self.thread_flask is not None:
            if self.thread_flask.is_server_running:
                self.textBrowser_log.append("HTTP服务已启动，请勿重复点击！")
                return

        app = Flask(__name__)
        # 新开一个线程 以免卡死
        self.thread_flask = FlaskServerThread(app=app)
        # 绑定http路由
        register_index_routes(app)
        # 绑定线程信号
        # self.thread_flask.signal_status.connect(
        #     lambda data: self.textBrowser_log.append(str(data))
        # )
        self.thread_flask.signal_status.connect(self.textBrowser_log.append)
        self.thread_flask.start()

    def slot_pushButton_closeHttp(self):
        logger.info("用户点击关闭http按钮")
        if self.thread_flask is None:
            self.textBrowser_log.append("没有正在运行的http服务")
            return
        if self.thread_flask.is_server_running:
            self.thread_flask.stop_server()
            self.thread_flask.quit()
            self.thread_flask.wait()
            self.thread_flask = None
            logger.info("关闭成功")
            self.textBrowser_log.append("关闭成功")
            return

    def closeEvent(self, a0):
        self.slot_pushButton_disconnectDevice()
        self.slot_pushButton_closeHttp()
        super().closeEvent(a0)
        logger.info("程序退出")
        exit(0)
