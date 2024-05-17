from .baseitem import MenuItem
from termo.ui.icons import Label, Symbol


class ActionItemMeta(type):

    _instances: dict[str, 'ActionItem'] = {}

    def __call__(cls, title, *args, **kwds):
        if title not in cls._instances:
            cls._instances[title] = super().__call__(title, *args, **kwds)
        return cls._instances[title]



    @property
    def quit(cls) -> "ActionItem":
        return cls(Label.QUIT.value, icon=Symbol.QUIT.value)


class ActionItem(MenuItem, metaclass=ActionItemMeta):
    def __init__(
        self, title, callback=None, key=None, icon=None, dimensions=None, template=None
    ):
        template = True
        super().__init__(title, callback, key, icon, dimensions, template)

    def setAvailability(self, enabled: bool):
        self._menuitem.setEnabled_(enabled)
