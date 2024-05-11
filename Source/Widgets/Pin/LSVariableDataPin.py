
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.Pin.LSDataPin import LSDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSVariableDataPin(LSDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title_label.hide()
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
    window=LSVariableDataPin()
    window.show()
    app.exec_()
