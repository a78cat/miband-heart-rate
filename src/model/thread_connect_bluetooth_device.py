import asyncio
import logging

from PySide6.QtCore import QThread, Signal
from bleak import BleakClient, BleakScanner

logger = logging.getLogger(__name__)
# 心率服务和特征UUID
HEART_RATE_SERVICE_UUID = '0000180d-0000-1000-8000-00805f9b34fb'
HEART_RATE_MEASUREMENT_UUID = '00002a37-0000-1000-8000-00805f9b34fb'
DEVICE_NAME_UUID = '00002a00-0000-1000-8000-00805f9b34fb'


class ScanBluetoothDevicesThread(QThread):
    signal_devices_list = Signal(list)

    def run(self):
        logger.info("执行扫描蓝牙设备")
        device_list = []
        try:
            # 异步扫描设备, 获取带有心率服务UUID的设备
            devices = asyncio.run(
                BleakScanner.discover(
                    timeout=3.0,
                    filters={"service_uuids": [HEART_RATE_SERVICE_UUID.lower()]}
                )
            )

            # 整理设备列表（名称, 地址）
            for d in devices:
                device_name = d.name if d.name else f"未知设备({d.address[:8]})"
                device_list.append((device_name, d.address))

            logger.info(f"蓝牙扫描完成，找到{len(device_list)}个心率设备")

        except Exception as e:
            err_msg = f"扫描失败：{str(e)}"
            logger.error(err_msg)
        finally:
            self.signal_devices_list.emit(device_list)


class ConnectBluetoothDeviceThread(QThread):
    signal_hart_rate_data = Signal(int)
    signal_status = Signal(str)

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
                    self.signal_hart_rate_data.emit(0)
                    logger.info('设备断开连接')

            except Exception as e:
                err_msg = f"连接/接收数据异常：{str(e)}"
                logger.error(err_msg)
                self.signal_status.emit(err_msg)

        asyncio.run(connect_device())

    def stop(self):
        """外部调用此方法，优雅停止线程"""
        logger.info("开始停止蓝牙连接线程")
        self.is_running = False  # 置为False，让循环退出
        # 等待线程结束（最多等3秒，避免卡死）
        self.quit()
        # self.wait()
        logger.info("蓝牙连接线程已停止")
