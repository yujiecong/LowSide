import ast

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Custom.LSObject import LSObject
from Source.Widgets.Pin.LSValueDataPin import LSValueDataPin
from Source.Widgets.Pin.LSPinLineEdit import LSPinLineEdit

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSLineEditDataPin(LSValueDataPin):
    @classmethod
    def deserialize(cls,new_item_instance, wrapper: "LSLineEditDataPin"):
        new_pin=super().deserialize(new_item_instance,wrapper)
        new_pin.set_text(wrapper.text)
        return new_pin

    def __init__(self,text="",*args,**kwargs):
        super().__init__(*args,**kwargs)
        with LSObject.Record(self, LSObject.RecordType.Duplicate | LSObject.RecordType.Serialize):
            self.text=text
        self.set_text(text)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.pin_layout.setContentsMargins(0, 0, 4, 0)
        self.pin_layout.setSpacing(5)
        self.value_layout.addWidget(self.lineedit)


    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()
        self.lineedit.editingFinished.connect(lambda :self.set_text(self.lineedit.text()))

    def init_body(self):
        super().init_body()
        if self.get_flow() == PinFlow.In:
            self.pin_layout.addWidget(self._pin_icon, 0, 0,2,1)
        else:
            self.pin_layout.addWidget(self._pin_icon,0,2)



        self.lineedit = LSPinLineEdit()
        self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)

        self.lineedit.setText(self.title)


    def set_text(self,text):
        self.text=text
        self.lineedit.setText(text)

    def to_ast(self):
        return ast.Constant(value=self.lineedit.text())

if __name__ == '__main__':
    app=QApplication()
    window=LSLineEditDataPin(flow=PinFlow.Out)
    window.show()
    app.exec_()
