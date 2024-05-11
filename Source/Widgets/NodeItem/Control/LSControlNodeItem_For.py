import ast

from Source import Globs
from PySide2.QtWidgets import *

from Source.Custom.Enums.LSPinEnum import PinFlow, LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSAstData import LSAstCodeFragmentName
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.NodeItem.Control.LSControlNodeItem import LSControlNodeItem
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source.Widgets.Pin.LSExecPin import LSExecPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSControlNodeItem_For(LSControlNodeItem):
    __LS_TYPE_NAME__ = "For"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.in_exec_pin = LSExecPin(PinFlow.In, title="exec", is_initialized=True)
        self.add_pin(
            self.in_exec_pin,
        )
        self.iterable_pin=self.add_pin(
            LSDataPin(PinFlow.In, title="iterable", attr_type=LSPinAttrType.object, is_initialized=True),
        )

        self.loop_body_pin=self.add_pin(
            LSExecPin(PinFlow.Out, title="loop body", is_initialized=True),
        )
        self.array_element_pin=self.add_pin(
            LSDataPin(PinFlow.Out, title="element", attr_type=LSPinAttrType.object, is_initialized=True),
        )
        self.array_index_pin=self.add_pin(
            LSDataPin(PinFlow.Out, title="index", attr_type=LSPinAttrType.int, is_initialized=True),
        )
        self.out_exec_pin = LSExecPin(PinFlow.Out, title="completed", is_initialized=True)
        self.add_pin(self.out_exec_pin)
        
        self.out_exec_pin.code_fragment=LSAstCodeFragmentName.last


        self.set_title("For Loop")

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
        self.title_icon.setPixmap(LSIcons.loop_svg)

    def to_ast(self):
        if self.iterable_pin.from_:
            iterable_ast = self.iterable_pin.from_[0].node.to_ast()
        else:
            iterable_ast = ast.Tuple(elts=[], ctx=ast.Load())
        body=[]
        if not self.loop_body_pin.is_out_connected:
            body=[ast.Pass()]


        return ast.For(
            target=ast.Name(id=self.array_element_pin.title, ctx=ast.Store()),
            iter=iterable_ast,
            body=body,
            orelse=[],
        )



if __name__ == '__main__':
    app=QApplication()
    window=LSControlNodeItem_For()
    window.show()
    app.exec_()
