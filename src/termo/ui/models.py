from enum import StrEnum
from termo.ui.icons import Symbol
from pydantic import BaseModel


class Status(StrEnum):
    LOADING = "loading"
    DISCONNECTED = "disconnected"
    LOADED = "loaded"


class Command(StrEnum):
    TOGGLE = "toggle"
    PLAY = "play"
    STOP = "stop"
    NEXT = "next"
    PREVIOUS = "previous"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    MUTE = "mute"
    RANDOM = "random"
    LAST_ADDED = "last_added"
    QUIT = "quit"
    RESTART = "restart"
    ALBUM = "album"
    COVER_ART = "cover_art"
    RECENTLY_PLAYED = "recent"
    SONG = "song"
    SEARCH = "search"
    ALBUMSONG = "albumsong"
    ARTIST = "artist"
    ARTIST_ALBUMS = "artist_albums"
    RANDOM_ALBUM = "random_album"
    RESCAN = "rescan"
    MOST_PLAYED = "most_played"
    LOAD_LASTPLAYLIST = "load_lastplaylist"
    PLAYLIST = "playlist"
    CURRENT_ARTIST = "current_artist"
    CURRENT_ALBUM = "current_album"
    PLAY_LAST_ADDED = "play_last_added"
    PLAY_MOST_PLAYED = "play_most_played"
    ANNOUNCE = "announce"
    PLAYER_RESPONSE = "player_response"
    SHARE = "share"


class NowData(BaseModel):
    temp: float
    humid: float

    @property
    def temp_text(self) -> str:
        return f"{self.temp}℃"

    @property
    def temp_icon(self) -> Symbol:
        temp = self.temp
        match temp:
            case temp if temp > 25:
                return Symbol.THERMOMETER_HIGH
            case temp if temp > 15:
                return Symbol.THERMOMETER_MEDIUM
            case _:
                return Symbol.THERMOMETER_LOW
