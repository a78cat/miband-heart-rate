import asyncio
import threading
import time

import requests
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


# 异步任务：扫描设备并订阅心率通知
async def run_hr_monitor():
    print('扫描设备中...')
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: HEART_RATE_SERVICE_UUID.lower() in ad.service_uuids, timeout=100.0)

    if not device:
        print('连接超时,没有找到设备')
        return

    print(f'发现{device.name},地址{device.address}')

    async with BleakClient(device.address) as client:
        print('连接中...')

        if not client.is_connected:
            print('连接失败')
            return

        name = await client.read_gatt_char(DEVICE_NAME_UUID)
        heart_rate_data['device_id'] = name.decode()
        print(f'已连接到:{heart_rate_data["device_id"]}')

        await client.start_notify(HEART_RATE_MEASUREMENT_UUID, handle_heart_rate_notification)
        print('接收心率数据中')
        while client.is_connected:
            await asyncio.sleep(1)


# 数据处理回调函数
def handle_heart_rate_notification(data1: str, data2: bytearray):
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


if __name__ == '__main__':
    try:
        asyncio.run(run_hr_monitor())
    except KeyboardInterrupt:
        print('\nMonitoring stopped.')
