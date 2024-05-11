import ast
import pprint

from PySide2.QtWidgets import *

from Source import Globs
from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType
from Source.Custom.LSIcons import LSIcons
from Source.Custom.LSObject import LSObject
from Source.Widgets.NodeItem.LSAstNodeItem import LSAstNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSMagicMethodNodeItem(LSAstNodeItem):
    __NODE_ITEM_TYPE__ = LSNodeItemType.ClassMagicMethod
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # self.identifier_label.setText(f"目标是{self.class_name}")
    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_title_layout(self):
        super().init_title_layout()
        self.title_icon.setPixmap(LSIcons.class_func_svg)

        # self.identifier_label=QLabel()
        # self.identifier_label.setObjectName("identifier_label")
        # self.title_layout.addWidget(self.identifier_label,1,1)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def init_serialize_ast(self):
        super().init_serialize_ast()
        "这个函数与序列化有关 记得不要乱弄"
        self.func_name = self.ast_data.func_name
        self.class_name = self.ast_data.class_name

    def to_ast(self):
        if self.func_name== "__init__":
            in_ast_args, in_ast_kwargs = self.input_pin_to_ast()
            expr = ast.Call(func=ast.Name(id=self.class_name, ctx=ast.Load()),
                           args=in_ast_args,
                           keywords=in_ast_kwargs,
                           ctx=ast.Load()
                           )
            return expr
        else:    
            raise ValueError
    
if __name__ == '__main__':
    app=QApplication()
    window=LSMagicMethodNodeItem()
    window.show()
    app.exec_()
