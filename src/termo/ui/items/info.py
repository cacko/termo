import logging
from typing import Any

from termo.ui.models import NowData
from .baseitem import BaseMenuItem
from termo.ui.icons import Label


class InfoItemMeta(type):

    instances: dict[str, "BaseMenuItem"] = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        k = cls.__name__
        if k not in cls.instances:
            logging.warning(f"Create new {k}")
            cls.instances[k] = super().__call__(title=k, *args, **kwds)
        return cls.instances[k]

class OutdoorItem(BaseMenuItem, metaclass=InfoItemMeta):

    def setAvailability(self, enabled: bool):
        self._menuitem.setEnabled_(enabled)
        
    def update_data(self, data: NowData):
        self.title = f"Outdoor: {data.title}"
