import logging
from PySide6.QtCore import QThread, Signal

from src.model.connectDevice import scan_devices

logger = logging.getLogger(__name__)


class ScanBluetoothDevicesThread(QThread):
    signal_devices_list = Signal(list)

    def run(self):
        logger.info("执行扫描蓝牙设备")
        device_list = scan_devices()
        self.signal_devices_list.emit(device_list)
