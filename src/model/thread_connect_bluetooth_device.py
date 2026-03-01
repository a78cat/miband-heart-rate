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
        self.is_running = True
        self.client = None
        logger.info(address)

    def run(self):
        async def connect_device():
            logger.info(f'执行设备连接')
            self.client = BleakClient(self.address)
            try:
                await self.client.connect()
                if not self.client.is_connected:
                    logger.info('连接失败')
                    return

                await self.client.start_notify(
                    HEART_RATE_MEASUREMENT_UUID,
                    lambda _, data: self.signal_hart_rate_data.emit(data[1]))
                logger.info('接收心率数据中')

                while self.is_running and self.client.is_connected:
                    await asyncio.sleep(1)

                # 设备连接断开
                if self.client.is_connected:
                    await self.client.stop_notify(HEART_RATE_MEASUREMENT_UUID)
                    await self.client.disconnect()
                    self.signal_hart_rate_data.emit(-1)
                    logger.info('设备断开连接')

            except Exception as e:
                err_msg = f"连接/接收数据异常：{str(e)}"
                logger.error(err_msg)
                self.signal_connect_status.emit(err_msg)

        asyncio.run(connect_device())

    def stop(self):
        """外部调用此方法，优雅停止线程"""
        logger.info("开始停止蓝牙连接线程")
        self.is_running = False  # 置为False，让循环退出
        # 等待线程结束（最多等3秒，避免卡死）
        self.quit()
        # self.wait()
        logger.info("蓝牙连接线程已停止")
