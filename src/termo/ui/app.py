from queue import Empty, Queue
from threading import Thread
from typing import Optional, Any
import logging
from rumps import rumps
from termo.ble.tp357 import TP357
from termo.ui.icons import AnimatedIcon, Label, Symbol
from termo.ui.items.actions import ActionItem
from termo.ui.models import Command, NowData, Status


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

    def __init__(self):
        super(TermoApp, self).__init__(
            name="teRMo",
            menu=[
                ActionItem.quit,
            ],
            icon=Symbol.THERMOMETER_MEDIUM_SLASH.value,
            quit_button=None,
            template=True,
            nosleep=True,
        )
        # Device.register()
        self.__status = Status.LOADING
        # self.__initCommands = [
        #     (Command.LAST_ADDED, LastAdded),
        #     (Command.RECENTLY_PLAYED, RecentlyPlayed),
        #     (Command.MOST_PLAYED, MostPlayed),
        # ]
        self.__ui_queue = Queue()
        self.menu.setAutoenablesItems = False  # type: ignore
        # self.__playlist = UIPlaylist(Label.RANDOM.value, self)
        # self.__last_added = Albumlist(self, Label.LAST_ADDED.value)
        # self.__artist_albums = ArtistAlbumsList(self, Label.ARTIST.value)
        # self.__most_played = Albumlist(self, Label.MOST_PLAYED.value)
        # self.__recent = Albumlist(self, Label.RECENT.value)
        # ActionItem.next.hide()
        # ActionItem.restart.hide()
        # ActionItem.previous.hide()
        # self.__bpm = BPM(ui_queue=self.__ui_queue)
        # self.__bpm.start()
        # self.__threads.append(self.__bpm)
        # self.manager = Manager(
        #     ui_queue=self.__ui_queue,
        #     time_event=self.__bpm.time_event,
        # )
        # self.manager.start()
        # self.__threads.append(self.manager)
        # api_server = Server()
        # api_server.start(self.manager.commander, self._onLaMetricInit)
        # self.__threads.append(api_server)
        # fetcher = Fetcher.register(
        #     manager_queue=self.manager.commander,
        #     do_extract=app_config.get("beats", {}).get("extract", False)
        # )
        # fetcher.start()
        # self.__threads.append(fetcher)
        # for cmd, _ in self.__initCommands:
        #     self.manager.commander.put_nowait((cmd, None))
        TP357.register(self.__ui_queue)
        TP357.start_notify()

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
        if self.title != resp.temp_text:
            self.icon = resp.temp_icon.value
            self.title = resp.temp_text
        

    # def _onPlaystatus(self, resp: Playstatus):
    #     self.__status = resp.status
    #     match resp.status:
    #         case Status.PAUSED:
    #             self.icon = Symbol.PAUSE.value
    #         case Status.PLAYING:
    #             if len(self.__playlist):
    #                 ActionItem.next.show()
    #                 ActionItem.previous.show()
    #             ActionItem.restart.show()
    #         case Status.ERROR:
    #             self.icon = Symbol.ERROR.value
    #         case Status.STOPPED:
    #             self.icon = Symbol.STOPPED.value
    #             self.title = ""
    #             if len(self.__playlist):
    #                 ActionItem.next.show()
    #                 ActionItem.previous.show()
    #             else:
    #                 ActionItem.next.hide()
    #                 ActionItem.previous.hide()
    #             ActionItem.restart.hide()
    #         case Status.LOADING:
    #             self.icon = next(LoadingIcon).value
    #         case Status.EXIT:
    #             rumps.quit_application()

    @rumps.events.before_quit
    def terminate(self):
        # self._onPlaystatus(Playstatus(status=Status.STOPPED))
        # self.manager.commander.put_nowait((Command.QUIT, None))
    
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
