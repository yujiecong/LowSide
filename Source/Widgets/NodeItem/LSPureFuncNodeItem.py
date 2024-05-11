from PySide2.QtWidgets import *

from Source import Globs
from Source.Common.Func import OS

from Source.Custom.LSIcons import LSIcons
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()

class LSPureFuncNodeItem(LSNodeItem):


    def init_ui(self):
        super().init_ui()

    def init_title_layout(self):
        super().init_title_layout()
        self.title_icon.setPixmap(LSIcons.green_function_svg)

    def init_style(self):
        super().init_style()
        extend_qss = self.styleSheet()+qss
        self.setStyleSheet(extend_qss)
        
    def init_connection(self):
        super().init_connection()

if __name__ == '__main__':
    app=QApplication()
    window=LSPureFuncNodeItem()
    window.show()
    app.exec_()
