import asyncio
import logging

from PySide6.QtCore import QThread, Signal
from bleak import BleakClient

logger = logging.getLogger(__name__)
# 心率服务和特征UUID
HEART_RATE_SERVICE_UUID = '0000180d-0000-1000-8000-00805f9b34fb'
HEART_RATE_MEASUREMENT_UUID = '00002a37-0000-1000-8000-00805f9b34fb'
DEVICE_NAME_UUID = '00002a00-0000-1000-8000-00805f9b34fb'


class ConnectBluetoothDeviceThread(QThread):
    signal_hart_rate_data = Signal(int)

    def __init__(self, address: str):
        super().__init__()
        self.address = address
        logger.info(address)

    def run(self):
        async def connect_device(address: str):
            logger.info("执行设备连接")
            async with BleakClient(address) as client:
                if not client.is_connected:
                    logger.info('连接失败')
                    self.quit()
                await client.start_notify(
                    HEART_RATE_MEASUREMENT_UUID,
                    lambda data1, data2: self.signal_hart_rate_data.emit(data2[1]))
                logger.info('接收心率数据中')
                while client.is_connected:
                    await asyncio.sleep(1)

        asyncio.run(connect_device(self.address))
