from typing import *

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyState
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Common.Func import OS
from Source.Widgets.Pin.LSBidirectionalPin import LSBidirectionalPin

from Source.Widgets.NodeItem.LSConnectableItem import LSConnectableItem
from Source.Widgets.NodeItem.LSItem import LSItem
from Source.Widgets.Pin.LSPin import LSPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSBidirectionalItem(LSConnectableItem):
    def __init__(self,*args,**kwargs):
        self.pin=LSBidirectionalPin(flow=PinFlow.Both,is_initialized=True)
        super().__init__(*args,**kwargs)
        self.add_pin(self.pin)

    def init_attrs(self):
        super().init_attrs()
        self.state = PropertyState.Normal
        self.color=QColor(58,57,57,155)
        self.pins=[]

    def init_properties(self):
        super().init_properties()
        self.setObjectName(LSItem.__name__)

        # self.setFixedSize(LSTurningPointItem.FixedWidget,LSTurningPointItem.FixedHeight)

    def init_ui(self):
        super().init_ui()
        self.main_layout=QHBoxLayout(self)
        self.main_layout.setContentsMargins(10,10,10,10)
        self.main_layout.addWidget(self.pin)


    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

    def init_connection(self):
        super().init_connection()
        self.pin.lineMoved_signal.connect(self._pin_line_moved)
        self.pin.lineReleased_signal.connect(self._pin_line_released)

    def add_pin(self,pin):
        pin.node=self
        self.pins.append(pin)


    def pin_at(self, cursor_pos: QPoint) -> Union[LSPin, None]:
        pin_rect: QRectF = self.pin.rect()
        mapped_rect=QRect(self.pin.mapToGlobal(pin_rect.topLeft()), self.pin.mapToGlobal(pin_rect.bottomRight()))

        if mapped_rect.contains(cursor_pos):
            return self.pin

    def duplicate(self, *args, **kwargs) -> "LSBidirectionalItem":
        new_inst:LSBidirectionalItem = self.__class__()
        return new_inst


if __name__ == '__main__':
    app=QApplication()
    window=LSBidirectionalItem()
    window.show()
    app.exec_()
