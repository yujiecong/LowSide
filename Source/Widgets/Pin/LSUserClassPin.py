import ast

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.Pin.LSValueDataPin import LSValueDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSUserClassPin(LSValueDataPin):
    def __init__(self,attr_name,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.attr_name=attr_name
        
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

    def to_ast(self):
        if self.from_:
            return self.from_[0].node.to_ast()
        else:
            return ast.Name(id=self.title)

if __name__ == '__main__':
    app=QApplication()
    window=LSUserClassPin()
    window.show()
    app.exec_()
