from enum import Enum
from pathlib import Path


class Label(Enum):
    QUIT = "Quit"


class Symbol(Enum):
    QUIT = "power"
    THERMOMETER_HIGH = "thermometer.high"
    THERMOMETER_MEDIUM = "thermometer.medium"
    THERMOMETER_LOW = "thermometer.low"
    THERMOMETER_MEDIUM_SLASH = "thermometer.medium.slash"
    HOURGLASS = "hourglass"
    HOURGLASS_BOTTOM = "hourglass.bottomhalf.filled"
    HOURGLASS_TOP = "hourglass.tophalf.filled"

class Icon(Enum):
    def __new__(cls, *args):
        icons_path = Path(__file__).parent / "icons"
        value = icons_path / args[0]
        obj = object.__new__(cls)
        obj._value_ = value.as_posix()
        return obj


class AnimatedIcon:

    __items: list[Symbol] = []
    __idx = 0
    __offset = 1

    def __init__(self, icons: list[Symbol]) -> None:
        self.__items = icons

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        res = self.__items[self.__idx]
        if self.__offset > 0 and self.__idx + self.__offset == len(self.__items):
            self.__offset = -1
        elif self.__idx == 0:
            self.__offset = 1

        self.__idx += self.__offset

        return res


class ProgressIcon:

    __items: list[Symbol] = []
    __idx = 0

    def __init__(self, icons: list[Symbol]) -> None:
        self.__items = icons

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        res = self.__items[self.__idx]
        self.__idx += 1
        if self.__idx == len(self.__items):
            self.__idx = 0
        return res
