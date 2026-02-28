import asyncio
import logging
import time

import requests
from PySide6.QtCore import Signal
from bleak import BleakScanner, BleakClient

# 心率服务和特征UUID
HEART_RATE_SERVICE_UUID = '0000180d-0000-1000-8000-00805f9b34fb'
HEART_RATE_MEASUREMENT_UUID = '00002a37-0000-1000-8000-00805f9b34fb'
DEVICE_NAME_UUID = '00002a00-0000-1000-8000-00805f9b34fb'
# 存储最新心率数据（线程安全，避免多请求冲突）
heart_rate_data = {
    'heart_rate': 0,  # 心率值（次/分钟）
    'timestamp': 0,  # 数据更新时间戳
    'device_id': '0'  # 设备ID（可选）
}
# data_lock = threading.Lock()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 数据处理回调函数
def _handle_heart_rate_notification(data1: str, data2: bytearray):
    print('处理心率数据中')
    heart_rate_data['heart_rate'] = data2[1]
    heart_rate_data['timestamp'] = int(time.time() * 1000)
    print(f'Heart Rate: {heart_rate_data["heart_rate"]} bpm')
    requests.post(
        'http://127.0.0.1:5001/api/heart_rate',
        json={'heart_rate': heart_rate_data['heart_rate'],
              'timestamp': heart_rate_data['timestamp'],
              'device_id': heart_rate_data['device_id']}
    )


class BluetoothDevicesProcess:
    # 定义信号
    # scan_finished = Signal(list)  # 扫描完成，传递设备列表[(name, address), ...]
    # scan_failed = Signal(str)  # 扫描失败
    # connect_success = Signal(str)  # 连接成功（设备名称）
    # connect_failed = Signal(str)  # 连接失败

    def __init__(self):
        self.is_scanning = False

    def disconnect_device(self):
        # TODO
        print(1)

    # 异步任务：获取心率通知
    async def connect_device(self, address: str):

        async with BleakClient(address) as client:
            logger.info('连接中')

            if not client.is_connected:
                logger.info('连接失败')
                return

            name = await client.read_gatt_char(DEVICE_NAME_UUID)
            heart_rate_data['device_id'] = name.decode()
            print(f'已连接到:{heart_rate_data["device_id"]}')

            await client.start_notify(HEART_RATE_MEASUREMENT_UUID,
                                      _handle_heart_rate_notification)
            logger.info('接收心率数据中')
            while client.is_connected:
                await asyncio.sleep(1)

    def scan_devices(self):
        """
        扫描到的蓝牙设备
        :return: 扫描到的蓝牙设备名称与地址
        """
        self.is_scanning = True
        try:
            # 异步扫描设备（过滤心率服务UUID）
            devices = asyncio.run(
                BleakScanner.discover(
                    timeout=10.0,
                    filters={"service_uuids": [HEART_RATE_SERVICE_UUID.lower()]}
                )
            )
            # 整理设备列表（名称+地址）
            device_list = []
            for d in devices:
                device_name = d.name if d.name else f"未知设备({d.address[:8]})"
                device_list.append((device_name, d.address))

            # self.scan_finished.emit(device_list)
            logger.info(f"蓝牙扫描完成，找到{len(device_list)}个心率设备")

        except Exception as e:
            err_msg = f"扫描失败：{str(e)}"

            logger.error(err_msg)
        finally:
            self.is_scanning = False
            return device_list


if __name__ == '__main__':
    bdp = BluetoothDevicesProcess()
    # devices = bdp.scan_devices()
    # for d in devices:
    #     print(d)
    # 正确写法：用 asyncio.run() 运行协程
    asyncio.run(bdp.connect_device(address='F7:1F:00:73:7F:67'))
    # try:
    #     asyncio.run(run_hr_monitor())
    # except KeyboardInterrupt:
    #     print('\nMonitoring stopped.')
