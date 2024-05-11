import ast

from Source import Globs
from PySide2.QtWidgets import *

from Source.Custom.Enums.LSPinEnum import PinFlow, LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSAstData import LSAstCodeFragmentName
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.NodeItem.Control.LSControlNodeItem import LSControlNodeItem
from Source.Widgets.Pin.LSCheckboxDataPin import LSCheckboxDataPin
from Source.Widgets.Pin.LSExecPin import LSExecPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSControlNodeItem_If(LSControlNodeItem):
    __LS_TYPE_NAME__ = "If"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.in_exec_pin=self.add_pin(
            LSExecPin(PinFlow.In,is_initialized=True),
        )

        self.condition_pin=LSCheckboxDataPin(PinFlow.In, title="Condition", attr_type=LSPinAttrType.bool, is_initialized=True)
        self.add_pin(self.condition_pin)

        self.out_true_pin=self.add_pin(
            LSExecPin(PinFlow.Out, title="True", is_initialized=True),
        )
        self.out_false_pin=LSExecPin(PinFlow.Out, title="False", is_initialized=True)
        self.add_pin(self.out_false_pin)

        self.out_false_pin.code_fragment=LSAstCodeFragmentName.orelse

        self.set_title("branch")
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
        
    def init_title_layout(self):
        super().init_title_layout()
        self.title_icon.setPixmap(LSIcons.branch_png)

    def to_ast(self):
        if self.condition_pin.from_:
            condition=self.condition_pin.from_[0].node.to_ast()
        else:
            condition = self.condition_pin.to_ast()
        return ast.If(
            test=condition,
            body=[],
            orelse=[],
        )

if __name__ == '__main__':
    app=QApplication()
    window=LSControlNodeItem_If()
    window.show()
    app.exec_()
