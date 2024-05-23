import asyncio
from asyncio import BaseEventLoop
from enum import StrEnum
import json
import logging
from queue import Queue
from typing import Any, Optional
from corethread import StoppableThread
import websockets

from termo.ui.models import NowData, Status, StatusChange


MAC = "c4:5a:11:b4:53:19"
ADDRESS = "E18B152D-E13D-4FB6-B1F6-72C620625F27"
UUID_WRITE = "00010203-0405-0607-0809-0a0b0c0d2b11"
UUID_READ = "00010203-0405-0607-0809-0a0b0c0d2b10"

class MessageModel(StrEnum):
    NOWDATA = "now_data"
    STATUSCHANGE = "status_change"

class ServiceMeta(type):

    __instance: Optional["Service"] = None
    __ui_queue: Optional[Queue] = None
    __notifier: Optional[asyncio.Future] = None


    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance

    def register(cls, ui_queue: Queue):
        cls.__ui_queue = ui_queue

    @property
    def queue(cls) -> Queue:
        return cls.__ui_queue

    def start_service(cls):
        loop: BaseEventLoop = asyncio.new_event_loop()

        def bleak_thread(loop: BaseEventLoop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        t = StoppableThread(target=bleak_thread, args=(loop,))
        t.start()
        cls.__notifier = asyncio.run_coroutine_threadsafe(
            cls().connect(), loop
        )
        return t


class Service(object, metaclass=ServiceMeta):

    async def connect(self):
        uri = "ws://127.0.0.1:23727/ws/"
        async for websocket in websockets.connect(uri):
            try:
                async for message in websocket:
                    data = json.loads(message)
                    model_type = MessageModel(data.get("model"))
                    del data["model"]
                    match model_type:
                        case MessageModel.NOWDATA:
                            self.__class__.queue.put_nowait(
                                NowData(**data)
                            )
                        case MessageModel.STATUSCHANGE:
                            self.__class__.queue.put_nowait(
                                StatusChange(**data)
                            )
            except websockets.ConnectionClosed:
                continue