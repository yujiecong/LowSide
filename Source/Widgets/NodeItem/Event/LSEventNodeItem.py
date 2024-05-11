from PySide2.QtWidgets import *

from Source import Globs
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.Pin.LSExecPin import LSExecPin
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSEventNodeItem(LSNodeItem):
    __NODE_ITEM_TYPE__ = LSNodeItemType.Event
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "一个view里只能存在一个event 节点"

    def init_pins_from_identifier(self):
        self.add_pin(
            LSExecPin(flow=PinFlow.Out),
        )

    def init_title_layout(self):
        super().init_title_layout()
        self.title_icon.setPixmap(LSIcons.event_svg)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def can_be_duplicated(self):
        return False

    def get_type(self):
        return

if __name__ == '__main__':
    app=QApplication()
    window=LSEventNodeItem()
    window.show()
    app.exec_()
