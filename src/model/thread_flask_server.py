import logging
import threading

from PySide6.QtCore import QThread, Signal
from flask import Flask
from werkzeug.serving import make_server

HTTP_SERVER_IP = '127.0.0.1'
HTTP_SERVER_PORT = 5001
logger = logging.getLogger(__name__)


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
