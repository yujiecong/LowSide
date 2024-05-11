import ast

from PySide2.QtWidgets import *

from Source import Globs
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType

from Source.Custom.LSIcons import LSIcons
from Source.Widgets.NodeItem.LSAstNodeItem import LSAstNodeItem
from Source.Widgets.Pin.LSExecPin import LSExecPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSExecNodeItem(LSAstNodeItem):
    __NODE_ITEM_TYPE__ = LSNodeItemType.Stubs

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def init_pins_from_identifier(self):
        self.in_pin = self.add_pin(
            LSExecPin(flow=PinFlow.In),row=0,
        )
        self.out_pin = self.add_pin(
            LSExecPin(flow=PinFlow.Out),row=0,
        )

    def init_title_layout(self):
        super().init_title_layout()
        self.title_icon.setPixmap(LSIcons.blue_function_png)

    def init_style(self):
        super().init_style()

        self.setStyleSheet(self.styleSheet() + qss)





if __name__ == '__main__':
    app = QApplication()
    window = LSExecNodeItem(None)
    window.show()
    app.exec_()
