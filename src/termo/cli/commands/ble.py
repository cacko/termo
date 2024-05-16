import logging
from termo.cli.cli import cli
from typing_extensions import Annotated
import asyncio
from bluetooth_sensor_state_data import BluetoothData
from bleak import BleakClient
from home_assistant_bluetooth import BluetoothServiceInfo
from thermopro_ble.parser import ThermoProBluetoothDeviceData
from bleak import BleakScanner

mac = "c4:5a:11:b4:53:19"
address = "E18B152D-E13D-4FB6-B1F6-72C620625F27"
MODEL_NBR_UUID = "2A24"


TP357_S_2 = BluetoothServiceInfo(
    name="TP357S (5319)",
    manufacturer_data={
        61122: b'\x00)"\x0b\x01',
        60866: b'\x00)"\x0b\x01',
        60610: b'\x00)"\x0b\x01',
        60354: b'\x00("\x0b\x01',
        60098: b'\x00("\x0b\x01',
        59842: b'\x00)"\x0b\x01',
        59586: b'\x00("\x0b\x01',
        59330: b'\x00("\x0b\x01',
        59074: b'\x00("\x0b\x01',
        58818: b'\x00("\x0b\x01',
        58562: b"\x00'\"\x0b\x01",
        58306: b'\x00("\x0b\x01',
        58050: b'\x00("\x0b\x01',
        57794: b'\x00)"\x0b\x01',
        57538: b'\x00)"\x0b\x01',
        57282: b'\x00)"\x0b\x01',
        57026: b'\x00)"\x0b\x01',
        56770: b'\x00)"\x0b\x01',
        56514: b'\x00)"\x0b\x01',
        56258: b'\x00)"\x0b\x01',
        56002: b'\x00)"\x0b\x01',
        55746: b'\x00*"\x0b\x01',
        55490: b'\x00)"\x0b\x01',
        55234: b'\x00*"\x0b\x01',
        54978: b'\x00*"\x0b\x01',
        54722: b'\x00*"\x0b\x01',
        54466: b'\x00+"\x0b\x01',
        54210: b'\x00-"\x0b\x01',
        53954: b'\x00,"\x0b\x01',
        53698: b'\x00/"\x0b\x01',
        53442: b'\x001"\x0b\x01',
        53186: b'\x00."\x0b\x01',
        52930: b'\x00,"\x0b\x01',
        52674: b'\x00,"\x0b\x01',
        52418: b'\x00+"\x0b\x01',
        52162: b'\x00*"\x0b\x01',
        51906: b'\x00*"\x0b\x01',
        51650: b'\x00*"\x0b\x01',
        51394: b'\x00*"\x0b\x01',
        51138: b'\x00*"\x0b\x01',
        50882: b'\x00)"\x0b\x01',
    },
    service_uuids=[mac],
    address=address,
    rssi=-60,
    service_data={},
    source="local",
)


@cli.command()
def room():
    parser = ThermoProBluetoothDeviceData()
    res = parser.update(TP357_S_2)
    print(res)

    
@cli.command()
def open():
    async def main():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d.rssi)
            print(d.address)

    asyncio.run(main())