
from Source import Globs
from PySide2.QtWidgets import *

from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSControlNodeItem(LSNodeItem):
    __NODE_ITEM_TYPE__ = LSNodeItemType.Control

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
        pass
if __name__ == '__main__':
    app=QApplication()
    window=LSControlNodeItem()
    window.show()
    app.exec_()
