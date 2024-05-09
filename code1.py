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


async def get_services(address):
    '''
    获取设备服务和特性的UUIDs
    :param address:
    :return:
    '''
    async with BleakClient(address) as client:
        # 连接到指定的BLE设备
        await client.connect()
        print(f'Connected to:{address}')
        # 获取并打印所有服务和特性的UUID
        services = await client.get_services()
        print("Services and characteristics found:")
        for service in services:
            print(f"Service {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic {char.uuid}")


async def connect_to_known_device(address):
    client = BleakClient(address)
    try:
        await client.connect()
        print(f"Connected to {address}")
        # 获取并打印所有服务和特性的UUID
        services = await client.get_services()
        print("Services and characteristics found:")
        for service in services:
            print(f"Service {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic {char.uuid}")
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

# loop.run_until_complete(get_services('FF:6E:90:6E:62:3D'))

known_addresses = [bootloader_device_list[0]['device_address']]
loop.run_until_complete(connect_to_devices(known_addresses))
