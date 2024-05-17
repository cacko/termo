from queue import Empty, Queue
from threading import Thread
from typing import Optional, Any
from rumps import rumps
from termo.ble.tp357 import TP357
from termo.ui.icons import AnimatedIcon, Label, Symbol
from termo.ui.items.actions import ActionItem
from termo.ui.models import NowData, Status


LoadingIcon = AnimatedIcon(
    [Symbol.HOURGLASS, Symbol.HOURGLASS_BOTTOM, Symbol.HOURGLASS_TOP]
)


class TermoAppMeta(type):
    _instance = None

    def __call__(self, *args, **kwds):
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)
        return self._instance

    def quit(cls):
        cls().terminate()


class TermoApp(rumps.App, metaclass=TermoAppMeta):

    __threads: list[Thread] = []
    __now_data: Optional[NowData] = None

    def __init__(self):
        super(TermoApp, self).__init__(
            name="teRMo",
            menu=[
                ActionItem.quit,
            ],
            icon=Symbol.THERMOMETER_MEDIUM_SLASH.value,
            quit_button=None,
            template=True,
            nosleep=False,
        )
        self.__status = Status.LOADING
        self.__ui_queue = Queue()
        self.menu.setAutoenablesItems = False  # type: ignore
        TP357.register(self.__ui_queue)
        self.__threads.append(TP357.start_notify())

    @property
    def threads(self):
        return self.__threads

    @rumps.clicked(Label.QUIT.value)
    def onQuit(self, sender):
        rumps.quit_application()
        # self.manager.commander.put_nowait((Command.QUIT, None))

    @rumps.events.on_screen_sleep
    def sleep(self):
        pass

    @rumps.events.on_screen_wake
    def wake(self):
        pass

    @rumps.timer(0.1)
    def process_ui_queue(self, sender):
        try:
            if self.__status == Status.LOADING:
                self.icon = next(LoadingIcon).value
            resp = self.__ui_queue.get_nowait()
            if resp:
                method = f"_on{resp.__class__.__name__}"
                if hasattr(self, method):
                    getattr(self, method)(resp)
                self.__ui_queue.task_done()
        except Empty:
            pass

    def _onNowData(self, resp: NowData):
        if self.__status == Status.LOADING:
            self.__status = Status.LOADED
        try:
            assert self.__now_data
            assert self.__now_data != resp
        except AssertionError:
            self.__now_data = resp
            self.title = self.__now_data.title
            self.icon = self.__now_data.temp_icon.value

    @rumps.events.before_quit
    def terminate(self):
        TP357.stop_notify()
        for th in self.__threads:
            try:
                th.stop()  # type: ignore
            except Exception:
                pass
        try:
            rumps.quit_application()
            # pid_file.unlink(missing_ok=True)
        except Exception:
            pass
