import ast

from Source import Globs
from PySide2.QtWidgets import *
from Source.Common.Func import OS
from Source.Widgets.Pin.LSValueDataPin import LSValueDataPin


qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSCheckboxDataPin(LSValueDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.checkbox=QCheckBox()
        self.checkbox.setChecked(True)
        self.value_layout.addWidget(self.checkbox)
        self.pin_layout.addWidget(self.value_widget,self.pin_layout.rowCount()-2,self.pin_layout.columnCount())


    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def to_ast(self):
        return ast.Constant(value=self.checkbox.isChecked())


if __name__ == '__main__':
    app=QApplication()
    window=LSCheckboxDataPin()
    window.show()
    app.exec_()
