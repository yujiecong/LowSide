from Source.Common.Func import OS

from Source.Widgets.Pin.LSDataPin import LSDataPin

from Source import Globs
from PySide2.QtWidgets import *

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDynamicDataSubPin(LSDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "不应该序列化"

    def init_attrs(self):
        super().init_attrs()
        self.is_dynamic=True

    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()


    def set_enabled(self,enable):
        self.is_enabled=enable
        if enable:
            self.current_color=self.enabled_color
        else:
            self.current_color=self.disabled_color
        self.update()




if __name__ == '__main__':
    app=QApplication()
    window=LSDynamicDataSubPin()
    window.show()
    app.exec_()
