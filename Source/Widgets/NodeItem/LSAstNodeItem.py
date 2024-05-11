import ast
import dataclasses
import functools
import pprint
import typing

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Custom.Enums.LSItemEnum import LSNodeItemType
from Source.Custom.Enums.LSPinEnum import PinFlow, PinType
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSItemData import LSRawAstItemData, LSRawClassMethodData, LSRawData
from Source.Custom.LSObject import LSObject
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source.Widgets.Pin.LSDynamicArgsPin import LSDynamicArgsPin
from Source.Widgets.Pin.LSDynamicArgsSubPin import LSDynamicArgsSubPin
from Source.Widgets.Pin.LSDynamicKWArgsPin import LSDynamicKWArgsPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSAstNodeItem(LSNodeItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.init_serialize_ast()

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


    def init_serialize_ast(self):
        self.args_info = self.ast_data.args_info
        self.return_info = self.ast_data.return_info
        self.func_type = self.ast_data.func_type

    def check_ast_data_equal(self,new_data):
        # 这里要注意 new_data.args_info 当前的数据是一个orderdict
        condition = [
            str(self.ast_data.args_info) == str(dict(new_data.args_info)),
            str(self.ast_data.return_info) == str(dataclasses.asdict(new_data.return_info)),
            str(self.ast_data.func_type) == str(new_data.func_type),
            str(self.ast_data.node_type) == str(new_data.node_type),
        ]
        if all(condition):
            return True
        return False

    def update_ast(self):
        # 重新刷新当前的item
        new_data = LSIdentifierData.get(self.identifier)
        if self.check_ast_data_equal(new_data):
            ls_print(f"{self.identifier}的数据没有变化")
        else:
            ls_print(f"{self.identifier}的数据发生了变化")

            self.ast_data:LSRawAstItemData=new_data
            self.remove_all_pins()
            self.init_ast_data()
            self.init_initialize_pins()
            self.init_pins_from_ast(self.ast_data)
            self.init_serialize_ast()

    def to_ast(self):
        """
        根据自己的data pin参数生成
        :return:
        """

        in_ast_args, in_ast_kwargs = self.input_pin_to_ast()
        rt_ast_names=[]
        rt_ast_types=[]
        output_pins=[]
        for pin in self.pins:
            if pin.get_flow() == PinFlow.Out and pin.get_type()==PinType.Data:
                rt_ast_names.append(ast.Name(id=pin.title, ctx=ast.Load()))
                rt_ast_types.append(ast.Name(id=pin.title, ctx=ast.Load()))
                output_pins.append(pin)

        if len(rt_ast_names)>1:
            target=ast.Tuple(elts=rt_ast_names, ctx=ast.Store())
            return ast.Assign(
                targets=target,
                value=ast.Call(
                    func=ast.Name(id=self.title, ctx=ast.Load()),
                    args=in_ast_args,
                    keywords=in_ast_kwargs,
                    ctx=ast.Load()
                )
            )
        else:
            target=ast.Name(id=output_pins[0].title, ctx=ast.Store())

            return ast.AnnAssign(
                target=target,
                annotation=ast.Name(id=output_pins[0].attr_type, ctx=ast.Load()),
                value=ast.Call(
                    func=ast.Name(id=self.title, ctx=ast.Load()),
                    args=in_ast_args,
                    keywords=in_ast_kwargs,
                    ctx=ast.Load()
                ),simple=1
            )

if __name__ == '__main__':
    app=QApplication()
    window=LSAstNodeItem()
    window.show()
    app.exec_()
