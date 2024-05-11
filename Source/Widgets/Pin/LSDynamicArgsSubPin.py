
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from Source.Common.Func import OS
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.Pin.LSDynamicDataSubPin import LSDynamicDataSubPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDynamicArgsSubPin(LSDynamicDataSubPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.pin_layout.setSpacing(5)
        self.pin_layout.setContentsMargins(10, 0, 4, 0)

        self.remove_arg_btn=QPushButton()
        self.remove_arg_btn.setFixedSize(16,16)
        self.remove_arg_btn.setIcon(QIcon(LSIcons.remove_svg))
        self.pin_layout.addWidget(self.remove_arg_btn,0,2)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()
        self.remove_arg_btn.clicked.connect(self.destoryed)



if __name__ == '__main__':
    app=QApplication()
    window=LSDynamicArgsSubPin()
    window.show()
    app.exec_()
