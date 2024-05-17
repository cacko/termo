from calendar import c
import logging
from re import A

import rich
from termo.cli.cli import cli
from typing_extensions import Annotated
import asyncio

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak import BleakScanner


mac = "c4:5a:11:b4:53:19"
ADDRESS = "E18B152D-E13D-4FB6-B1F6-72C620625F27"
uuid_write = "00010203-0405-0607-0809-0a0b0c0d2b11"
uuid_read  = "00010203-0405-0607-0809-0a0b0c0d2b10"

@cli.command()
def scan():
    pass
    
def to_result(data: bytearray):
    temp = (data[3] + data[4] * 256) / 10
    humid = data[5]
    rich.print([temp, humid])    
    
def notification_handler(sender: BleakGATTCharacteristic, data: bytearray):
    to_result(data)


    
@cli.command()
def room():
    async def main():
        device: BLEDevice = None
        while not device:
            devices = await BleakScanner.discover()
            device = next(filter(lambda x: x.address == ADDRESS, devices), None)
        async with BleakClient(device) as client:
            read = client.services.get_characteristic(uuid_read)
            write = client.services.get_characteristic(uuid_write)
            await client.start_notify(read, callback=notification_handler)
            try: 
                while True:
                    await asyncio.sleep(0.5)
            except KeyboardInterrupt:
                await client.stop_notify(read)

    asyncio.run(main())