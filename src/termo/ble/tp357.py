import asyncio
import logging
from queue import Queue
from threading import Thread
from typing import Any, Optional
from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak import BleakScanner

from termo.ui.models import NowData



MAC = "c4:5a:11:b4:53:19"
ADDRESS = "E18B152D-E13D-4FB6-B1F6-72C620625F27"
UUID_WRITE = "00010203-0405-0607-0809-0a0b0c0d2b11"
UUID_READ  = "00010203-0405-0607-0809-0a0b0c0d2b10"


class TP357Meta(type):
    
    __instance: Optional['TP357'] = None
    __ui_queue: Optional[Queue] = None
    
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance
    
    def register(cls, ui_queue: Queue):
        cls.__ui_queue = ui_queue
    
    @property
    def queue(cls) -> Queue:
        return cls.__ui_queue
    
    def start_notify(cls):
        loop = asyncio.get_event_loop()
        def bleak_thread(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        t = Thread(target=bleak_thread, args=(loop,))
        t.start()
        asyncio.run_coroutine_threadsafe(cls().init_notify(), loop)
    
    
def to_result(data: bytearray):
    temp = (data[3] + data[4] * 256) / 10
    humid = data[5]
    return NowData(
        temp=temp,
        humid=humid
    )
    
def notification_handler(sender: BleakGATTCharacteristic, data: bytearray):
    res = to_result(data)
    logging.debug(res)
    TP357.queue.put_nowait(res)


    
class TP357(object, metaclass=TP357Meta):

    async def init_notify(self):
        device: BLEDevice = None
        while not device:
            devices = await BleakScanner.discover()
            device = next(filter(lambda x: x.address == ADDRESS, devices), None)
        logging.info(f"found device {device.details}")
        async with BleakClient(device) as client:
            logging.info(f"connected to {client.address}")
            read = client.services.get_characteristic(UUID_READ)
            await client.start_notify(read, callback=notification_handler)
            try: 
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                await client.stop_notify(read)