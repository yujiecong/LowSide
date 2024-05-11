import dataclasses
import pprint
from typing import *

from PySide2.QtCore import *

class LSDictWrapper:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getattr__(self, item):
        if item in self.dictionary:
            return self.dictionary[item]
        else:
            raise AttributeError(f"'DictWrapper' object has no attribute '{item}'")

    def __get__(self, instance, owner):
        return self.dictionary

    def __repr__(self):
        return f"LSDictWrapper({pprint.pformat(self.dictionary)})"
class LSEventFilter(QObject):
    enter_signal = Signal(QEvent)
    leave_signal = Signal(QEvent)
    grab_mouse_signal = Signal(QEvent)
    ungrab_mouse_signal = Signal(QEvent)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()
        # if event_type == QEvent.Leave:
        #     self.leave_signal.emit(event)
        # elif event_type == QEvent.Enter:
        #     self.enter_signal.emit(event)
        # elif event_type == QEvent.GrabMouse:
        #     self.grab_mouse_signal.emit(event)
        # elif event_type == QEvent.UngrabMouse:
        #     self.ungrab_mouse_signal.emit(event)

        return super().eventFilter(watched, event)

    @staticmethod
    def install(instance: Union[QObject]):
        if not issubclass(type(instance), QObject):
            raise TypeError("installed object must be a QObject")

        event_filter = LSEventFilter(instance)
        event_filter.grab_mouse_signal.connect(instance.mouseGrabEvent)
        event_filter.ungrab_mouse_signal.connect(instance.mouseUngrabEvent)
        instance.installEventFilter(event_filter)

        return instance


