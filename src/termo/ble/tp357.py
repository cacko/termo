import asyncio
from asyncio import BaseEventLoop
import logging
from queue import Queue
from typing import Any, Optional
from corethread import StoppableThread
from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak import BleakScanner

from termo.ui.models import NowData, Status, StatusChange


MAC = "c4:5a:11:b4:53:19"
ADDRESS = "E18B152D-E13D-4FB6-B1F6-72C620625F27"
UUID_WRITE = "00010203-0405-0607-0809-0a0b0c0d2b11"
UUID_READ = "00010203-0405-0607-0809-0a0b0c0d2b10"


class TP357Meta(type):

    __instance: Optional["TP357"] = None
    __ui_queue: Optional[Queue] = None
    __notifier: Optional[asyncio.Future] = None
    __thread: Optional[StoppableThread] = None

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
        if not cls.__notifier:
            loop: BaseEventLoop = asyncio.get_event_loop()

            def bleak_thread(loop: BaseEventLoop):
                asyncio.set_event_loop(loop)
                loop.run_forever()

            t = StoppableThread(target=bleak_thread, args=(loop,))
            t.start()
            cls.__notifier = asyncio.run_coroutine_threadsafe(
                cls().init_notify(), loop
            )
            return t

    def restart_notify(cls):
        loop = asyncio.get_event_loop()
        cls.__notifier = asyncio.run_coroutine_threadsafe(cls().init_notify(), loop)

    def stop_loop(cls):
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()


    def stop_notify(cls):
        try:
            assert cls.__notifier
            assert cls.__notifier.cancel()
            logging.info(f"STOP NOTIFY")
        except AssertionError:
            pass


def to_result(data: bytearray):
    temp = (data[3] + data[4] * 256) / 10
    humid = data[5]
    return NowData(temp=temp, humid=humid)


def notification_handler(sender: BleakGATTCharacteristic, data: bytearray):
    res = to_result(data)
    logging.debug(res)
    TP357.queue.put_nowait(res)


def disconnect_handler(client: BleakClient):
    logging.info(f"{client.address} disconnected")
    TP357.queue.put_nowait(StatusChange(status=Status.DISCONNECTED))


class TP357(object, metaclass=TP357Meta):

    @property
    async def device(self) -> BLEDevice:
        device: BLEDevice = None
        while not device:
            devices = await BleakScanner.discover()
            device = next(filter(lambda x: x.address == ADDRESS, devices), None)
        logging.info(f"found device {device.details}")
        return device

    async def init_notify(self):
        device = await self.device
        TP357.queue.put_nowait(StatusChange(status=Status.LOADING))
        async with BleakClient(
            device, disconnected_callback=disconnect_handler
        ) as client:
            logging.info(f"connected to {client.address}")
            read = client.services.get_characteristic(UUID_READ)
            await client.start_notify(read, callback=notification_handler)
            try:
                while client.is_connected:
                    await asyncio.sleep(0.5)
            except Exception as e:
                logging.exception(e)
                await client.stop_notify(read)
