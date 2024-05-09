'''
将crazyflie处于bootloader模式，通过运行该代码，可以打印nrf51822提供的所有服务
其中Service 00000201-1c7f-4f9e-947b-43b7c00a9a08  该服务为与nrf-bootloader中对应的crazyflie的服务

#define UUID_CRAZYFLIE_SERVICE   0x0201  # 这个是服务
#define UUID_CRAZYFLIE_CRTP      0x0202  # 这个是特性
#define UUID_CRAZYFLIE_CRTP_UP   0x0203
#define UUID_CRAZYFLIE_CRTP_DOWN 0x0204

通过运行该代码，可以看到有如下
Service 00000201-1c7f-4f9e-947b-43b7c00a9a08
  Characteristic 00000202-1c7f-4f9e-947b-43b7c00a9a08
  Characteristic 00000203-1c7f-4f9e-947b-43b7c00a9a08
  Characteristic 00000204-1c7f-4f9e-947b-43b7c00a9a08
'''
# UUID_CRAZYFLIE_SERVICE = '0x0201'
# UUID_CRAZYFLIE_CRTP = '0x0202'
# UUID_CRAZYFLIE_CRTP_UP = '0x0203'
# UUID_CRAZYFLIE_CRTP_DOWN = '0x0204'

UUID_CRAZYFLIE_CRTP_UUID = '00000202-1c7f-4f9e-947b-43b7c00a9a08'

import asyncio
from bleak import BleakScanner, BleakClient

bootloader_device_list = []


async def scan():
    # 使用BleakScanner扫描BLE设备
    print('----Scanning for devices----')
    devices = await BleakScanner.discover(timeout=5)
    for device in devices:
        # print(f"Device {device.name}: {device.address}")
        if device.name == 'Crazyflie':  # 设备正常运行时的蓝牙
            print(f"Device {device.name}: {device.address}")
        elif device.name == 'Crazyflie Loader':
            print(f"Device {device.name}: {device.address}")
            bootloader_device_list.append({'device_name': device.name, 'device_address': device.address})


async def connect_to_known_device(address):
    client = BleakClient(address,timeout=30)
    try:
        # 连接设备
        await client.connect()
        print(f"Connected to {address}")
        # 发送数据
        data_to_send = bytes([0x01, 0x02, 0x03, 0x04])  # 示例数据
        # 写入数据到指定的特性
        try:
            await client.write_gatt_char(UUID_CRAZYFLIE_CRTP_UUID, data_to_send)
            print("Data written to characteristic")
        except Exception as e:
            print(print(f"Failed to send data to {address}: {e}"))
    except Exception as e:
        print(f"Failed to connect to {address}: {e}")


async def connect_to_devices(device_addresses):
    tasks = [connect_to_known_device(addr) for addr in device_addresses]
    await asyncio.gather(*tasks)


# 启动扫描过程
loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
# quit()
# loop.run_until_complete(get_services(bootloader_device_list[0]['device_address']))


known_addresses = [bootloader_device_list[0]['device_address']]
loop.run_until_complete(connect_to_devices(known_addresses))
