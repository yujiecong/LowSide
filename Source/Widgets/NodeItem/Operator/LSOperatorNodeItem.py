
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Custom.LSIcons import LSIcons
from Source.Custom.LSObject import LSObject
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSOperatorNodeItem(LSNodeItem):
    __NODE_ITEM_TYPE__ = LSNodeItemType.Operator
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "如果有父了 就不要调用了"


    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.title_widget.deleteLater()

        self.display_label=QLabel(self)
        self.display_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        pixmap = QPixmap(LSIcons.add_svg).scaled(20,20)
        self.display_label.setPixmap(pixmap)
        self.display_label.setObjectName("display_label")
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setEnabled(False)
        "让这个label在中间"



    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_label.setGeometry(0,0,self.width(),self.height())





if __name__ == '__main__':
    app=QApplication()
    window=LSOperatorNodeItem()
    window.show()
    app.exec_()
