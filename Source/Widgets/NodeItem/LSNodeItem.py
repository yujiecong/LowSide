import ast
import collections
import contextlib
import dataclasses
import functools
import logging
import pprint
import traceback
import typing

from PySide2.QtWidgets import *
from PySide2.QtCore import *

from Source import Globs
from Source.Common import Func
from Source.Common.Enums import LSCreateItemMode
from Source.Common.Logger import ls_print
from Source.Custom.Enums.LSPinEnum import PinColumn, PinFlow, LSPinAttrType, PinType
from Source.Common.Func import OS
from Source.Common.Obj import LSDictWrapper
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSObject import LSObject
from Source.Custom.LSAstData import LSAstFuncType, LSAstReturnData
from Source.Custom.LSItemData import LSRawAstItemData, LSRawData, LSRawClassMethodData
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSNodeSourceType
from Source.Widgets.LSPinWrapper import LSPinWrapper
from Source.Widgets.NodeItem.LSConnectableItem import LSConnectableItem
from Source.Widgets.Pin.LSDynamicArgsPin import LSDynamicArgsPin
from Source.Widgets.Pin.LSDynamicArgsSubPin import LSDynamicArgsSubPin
from Source.Widgets.Pin.LSDynamicKWArgsPin import LSDynamicKWArgsPin
from Source.Widgets.Pin.LSFlowPin import LSFlowPin
from Source.Widgets.NodeItem.LSItem import LSItem
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source.Widgets.Pin.LSLineEditDataPin import LSLineEditDataPin
from Source.Widgets.Pin.LSPin import LSPin
from Source.Widgets.Pin.LSValueDataPin import LSValueDataPin

# QWidget 使用自定义的样式表会出现bug
"""
    2023年11月21日20:56:13记录
    第一次set style sheet 是没问题的
    但是后来就不行了
    网上的方法是换成QFrame继承。难受
"""

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


# noinspection PyTypeChecker
class LSNodeItem(LSConnectableItem, ):
    __NODE_ITEM_TYPE__ = LSNodeItemType.Undefined

    @classmethod
    def get_identifier(cls):
        return Func.ls_joinPaths(cls.__NODE_ITEM_TYPE__, cls.__LS_TYPE_NAME__)

    @classmethod
    def deserialize(cls, data_wrapper: "LSNodeItem") -> "LSNodeItem":
        item = cls.from_serial_data(data_wrapper)
        item.move(*data_wrapper.item_pos)
        item.finished_deserialize()
        return item

    def finished_deserialize(self):
        for idx, pin in enumerate(self.pins):
            pin:LSPin
            pin.finished_init()
        self.finished_init()

    def finished_init(self):
        pass

    @classmethod
    def from_identifier(cls, identifier, *, uuid_=None) -> "LSNodeItem":
        ast_data: LSRawAstItemData = LSIdentifierData.get(identifier)
        "这里怎么重写成  把wrapper data放进来"
        # new_item_instance = LSObject.registered_classes[ast_data.instance_type](identifier=identifier,
        #                                                                         title=ast_data.title,
        #                                                                         uuid_=uuid_, ast_data=ast_data)
        constructor = cls._curry_constructor(identifier, data_wrapper=ast_data, uuid_=uuid_)
        new_item_instance: "LSNodeItem" = cls._create_curry_instance(constructor, ast_data,LSCreateItemMode.Identifier)

        if ast_data.source == LSNodeSourceType.Ast:
            new_item_instance.init_pins_from_ast(ast_data)

        return new_item_instance

    @classmethod
    def from_serial_data(cls, data_wrapper) -> "LSNodeItem":
        identifier = data_wrapper.identifier
        uuid_ = data_wrapper.uuid_
        constructor = cls._curry_constructor(identifier, data_wrapper, uuid_=uuid_)
        new_item_instance: "LSNodeItem" = cls._create_curry_instance(constructor, data_wrapper, LSCreateItemMode.Serial)
        # new_item_instance.init_pins_from_ast(data_wrapper.pins_serialized)
        new_item_instance.pins_from_serial_data(new_item_instance, data_wrapper)

        if data_wrapper.source == LSNodeSourceType.Ast:
            pass
            # 这里改动东西会影响 保存时的ast数据受影响
            # data_wrapper.return_info = LSDictWrapper(data_wrapper.return_info)
            # new_item_instance.init_pins_from_ast(data_wrapper)
            # data_wrapper.return_info = data_wrapper.return_info.dictionary
        return new_item_instance

    def pins_from_serial_data(self, new_item_instance, data_wrapper:"LSNodeItem"):
        pins_serialized:typing.List[dict]=data_wrapper.pins_serialized
        self.variable_pins_data= data_wrapper.variable_pins_data

        for pin_sdata in pins_serialized:
            pin_wrapper_data = LSDictWrapper(pin_sdata)
            pin_type: LSPin = LSObject.registered_classes[pin_wrapper_data.class_name]
            pin = pin_type.deserialize(new_item_instance, pin_wrapper_data)
            self.add_pin(pin)
            for variable_pin_name,variable_pin_uuid_ in self.variable_pins_data.items():
                if pin.uuid_==variable_pin_uuid_:
                    setattr(self, variable_pin_name, pin)
                    break

    @staticmethod
    def _curry_constructor(identifier, data_wrapper, uuid_):
        return functools.partial(LSObject.registered_classes[data_wrapper.instance_type],
                                 identifier=identifier,
                                 title=data_wrapper.title,
                                 uuid_=uuid_,
                                 ast_data=data_wrapper)

    @staticmethod
    def _create_curry_instance(constructor, data_wrapper,create_mode):
        return constructor(create_mode=create_mode)

    def init_pins_from_identifier(self):
        pass

    def init_pins_from_ast(self, ast_data):
        for idx, item in enumerate(ast_data.args_info.items()):
            arg_name, arg_type = item
            if arg_name.startswith("**"):
                data_pin: LSDynamicKWArgsPin = self.add_pin(LSDynamicKWArgsPin(flow=PinFlow.In,
                                                                               title=arg_name,
                                                                               attr_type=arg_type,
                                                                               ))

            elif arg_name.startswith("*"):
                data_pin: LSDynamicArgsPin = self.add_pin(LSDynamicArgsPin(flow=PinFlow.In,
                                                                           title=arg_name,
                                                                           attr_type=arg_type,
                                                                           ))
            else:
                if arg_type == LSPinAttrType.str:
                    self.add_pin(LSLineEditDataPin(flow=PinFlow.In, attr_type=arg_type, title=arg_name))
                else:
                    self.add_pin(LSDataPin(flow=PinFlow.In, attr_type=arg_type, title=arg_name))

        return_info: LSAstReturnData = ast_data.return_info
        for return_name in return_info.return_names:
            return_pin = self.add_pin(LSDataPin(flow=PinFlow.Out,
                                                title=return_name,
                                                attr_type=return_info.attr_type, ))

    def __init__(self, ast_data: typing.Union[LSRawAstItemData, LSRawClassMethodData] = LSRawData(),
                 create_mode=LSCreateItemMode.Default,
                 identifier="",
                 title="anonymous", *args, **kwargs):
        # identifier=identifier or Func.joinPaths(type(self).__name__,title)
        with LSObject.Record(self, LSObject.RecordType.Duplicate | LSObject.RecordType.Serialize):
            self.title = title
            self.identifier = identifier
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.instance_type = self.__class__.__name__
            self.variable_pins_data:typing.Dict[str,str] = {}

        with LSObject.Record(self, LSObject.RecordType.Duplicate):
            self.ast_data = ast_data
        self.create_mode=create_mode

        self.init_ast_data()
        super().__init__(*args, **kwargs)
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.item_pos = lambda: self.pos().toTuple()
            self.pins_serialized = self.serialize_pins
            self.pin_connect_info = lambda: [dataclasses.asdict(data) for data in
                                             self.get_pin_connect_info(flow=PinFlow.Out)]
            self.type_name = self.__class__.__name__

        self.set_title(title)

        if create_mode==LSCreateItemMode.Identifier:
            self.init_pins_from_identifier()

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()
        self.init_main_layout()
        self.init_title_layout()
        self.init_body_layout()

    def init_attrs(self):
        super().init_attrs()



    def init_connection(self):
        super().init_connection()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_body_layout(self):
        self.body_widget = QWidget()
        self.body_widget.setObjectName("body_widget")

        # self.body_widget.setStyleSheet("background-color:yellow;")

        self.body_layout = QGridLayout(self.body_widget)
        # self.body_layout.setSizeConstraint(QLayout.SetFixedSize)

        # self.body_vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.body_layout.addItem(self.body_vertical_spacer)
        self.body_layout.setContentsMargins(6, 6, 6, 6)
        self.body_layout.setSpacing(5)
        self.main_layout.addWidget(self.body_widget, 1, 0)

    def init_title_layout(self):

        self.title_widget = QWidget()
        self.title_widget.setObjectName("title_widget")
        self.title_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.title_layout = QGridLayout(self.title_widget)

        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("title_label")

        self.title_icon = QLabel()
        self.title_icon.setScaledContents(True)
        self.title_icon.setFixedSize(16, 16)

        self.title_layout.setContentsMargins(3, 5, 5, 5)
        self.title_layout.setSpacing(3)
        self.title_layout.setHorizontalSpacing(3)
        self.title_layout.setVerticalSpacing(3)

        self.title_layout.addWidget(self.title_icon, 0, 0)
        self.title_layout.addWidget(self.title_label, 0, 1)
        self.main_layout.addWidget(self.title_widget, 0, 0)

    def init_main_layout(self):

        self.main_widget = QWidget()
        self.main_layout = QGridLayout(self.main_widget)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(0)

        self.main_widget.setObjectName("main_widget")

        self.core_layout = QHBoxLayout(self)
        self.core_layout.setContentsMargins(2, 2, 2, 2)
        self.core_layout.setSpacing(0)
        self.core_layout.addWidget(self.main_widget)
        # self.main_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 这个widget加入scene之后 边框样式会失效，所以不能用它直接去做边框
        # 要用一个子widget去做

        self.setObjectName(LSItem.__name__)
    def init_ast_data(self):
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.node_type = self.ast_data.node_type
            self.source = self.ast_data.source

    @contextlib.contextmanager
    def register_variable_pin_data(self):
        locals1 = list(self.__dict__.keys())
        yield
        locals2 = list(self.__dict__.keys())
        diff = set(locals2) - set(locals1)
        for pin_var_name in diff:
            pin:LSPin=self.__dict__[pin_var_name]
            self.variable_pins_data[pin_var_name]=pin.uuid_

    def serialize_pins(self):
        data = []
        for pin in self.pins:
            data.append(pin.serialize())
        return data

    def set_title(self, title):
        self.title = title
        self.title_label.setText(title)



    def update_layout(self):
        """

        :return:
        """
        "更新弹簧"
        # self.body_layout.addItem(self.body_vertical_spacer, self.body_layout.rowCount() + 1, 0)
        # self.body_widget.adjustSize()
        # self.body_widget.updateGeometry()

        "重排一次"
        self.update_pin_row()
        for pin in self.pins:
            pin_column = PinColumn.In if pin.get_flow() == PinFlow.In else PinColumn.Out
            self.body_layout.addWidget(pin.wrapper, pin.row, pin_column)
        self.updateGeometry()
        self.adjustSize()

    def pin_at(self, cursor_pos: QPoint) -> typing.Union[LSPin, None]:
        """
        在这之前,得有一个查询的表, 判断pos在哪个pin里
        :param cursor_pos:
        :return:
        """
        pin_2_global_rect = self._get_pin_2_global_rect()
        for pin, global_rect in pin_2_global_rect.items():
            if global_rect.contains(cursor_pos):
                return pin

    def _get_pin_2_global_rect(self) -> typing.Dict[LSPin, QRect]:
        """
        获得当前所有pin的pos for循环 效率很低 但没办法
        :return:
        """
        pin_2_rect = {}
        for pin in self.pins:
            rect: QRectF = pin.rect()
            pin_2_rect[pin] = QRect(pin.mapToGlobal(rect.topLeft()), pin.mapToGlobal(rect.bottomRight()))
        return pin_2_rect

    def update_pins(self):
        for pin in self.pins:
            pin.update_connected_line()
            pin.update_connection_style()

    def update_pin_row(self):
        for col in range(self.body_layout.columnCount()):
            valid_row = 0
            valid_items = []
            for row in range(self.body_layout.rowCount()):
                item = self.body_layout.itemAtPosition(row, col)
                if item:
                    valid_row += 1
                    valid_items.append(item)

            for v_row in range(valid_row):
                valid_item = valid_items[v_row]
                widget = valid_item.widget()
                pin_wrapper: LSPinWrapper = widget
                pin_wrapper.pin.set_row(row=v_row)

    def remove_all_pins(self):
        self.disconnect_all_pins()
        for _ in range(len(self.pins)):
            self.pins[0].destroyed_signal.emit()

    def remove_pin(self, ):
        pin: LSFlowPin = self.sender()
        for to_pin in pin.to_:
            pin.disconnect_pin(to_pin)
        for from_pin in pin.from_:
            pin.disconnect_pin(from_pin)
        pin_wrapper=pin.wrapper
        self.body_layout.takeAt(self.body_layout.indexOf(pin_wrapper))
        pin_wrapper.hide()
        pin_wrapper.setParent(None)
        pin_wrapper.deleteLater()
        self.pins.remove(pin)
        self.update_layout()

    def add_pin(self, pin: LSPin, row=None):
        is_insert = False
        is_in = pin.get_flow() == PinFlow.In
        is_out = pin.get_flow() == PinFlow.Out
        pin_column = PinColumn.In if is_in else PinColumn.Out
        if row:
            body_row = row
            item = self.body_layout.itemAtPosition(row, pin_column)
            if item is not None:
                is_insert = True
        else:
            body_row = self.body_layout.rowCount()
            for ever_row in range(self.body_layout.rowCount()):
                item = self.body_layout.itemAtPosition(ever_row, pin_column)
                if item is None:
                    body_row = ever_row
                    break

        if self.view:
            pin.set_view(self.view)

        pin.node = self
        pin.lineMoved_signal.connect(self._pin_line_moved)
        pin.lineReleased_signal.connect(self._pin_line_released)
        pin.destroyed_signal.connect(self.remove_pin)

        if is_insert:
            # 如果是插入的话 没办法 下面的全部移动
            last_replaced_pin: LSPinWrapper = self.body_layout.itemAtPosition(body_row, pin_column).widget()
            self.pins.insert(self.pins.index(last_replaced_pin.pin), pin)
            self.body_layout.removeWidget(last_replaced_pin)
            last_replaced_pin.setParent(None)
            self.body_layout.addWidget(pin.wrapper, body_row, pin_column)
            for replaced_row in range(body_row + 1, self.body_layout.rowCount() + 1):
                item = self.body_layout.itemAtPosition(replaced_row, pin_column)
                if item is None:
                    "到底了"
                    self.body_layout.addWidget(last_replaced_pin, replaced_row, pin_column)
                    break
                else:
                    cur_replaced_pin: LSPinWrapper = item.widget()
                    self.body_layout.removeWidget(last_replaced_pin)
                    last_replaced_pin.setParent(None)
                    self.body_layout.addWidget(last_replaced_pin, replaced_row, pin_column)
                    last_replaced_pin = cur_replaced_pin

        else:
            self.body_layout.addWidget(pin.wrapper, body_row, pin_column)
            self.pins.append(pin)

        self.update_layout()
        return pin

    def duplicate(self, *args, **kwargs) -> "LSNodeItem":
        node_construct_data = {}
        for key in self.constructor_keywords:
            node_construct_data[key] = getattr(self, key)

        dup_inst: LSNodeItem = self.__class__(**node_construct_data,create_mode=LSCreateItemMode.Duplicate)
        uuid_2_variable_pin_name = {v:k for k,v in self.variable_pins_data.items()}
        dup_variable_pins_data={}
        for pin in self.pins:
            pin_construct_data = {}
            for k in LSObject.ConstructorKeywords[pin.__class__.__name__]:
                pin_construct_data[k] = getattr(pin, k)

            dup_pin = pin.duplicate(dup_inst, **pin_construct_data)
            dup_pin = dup_inst.add_pin(dup_pin, row=pin.row)
            dup_pin.duplicate_finished(pin)

            if pin.uuid_ in uuid_2_variable_pin_name:
                variable_pin_name = uuid_2_variable_pin_name[pin.uuid_]
                dup_variable_pins_data[variable_pin_name]= dup_pin.uuid_
                setattr(dup_inst, variable_pin_name, dup_pin)
        dup_inst.variable_pins_data=dup_variable_pins_data
        return dup_inst

    def input_pin_to_ast(self):
        in_ast_args = []
        in_ast_kwargs = []
        for pin in self.pins:
            if pin.get_flow() == PinFlow.In and pin.get_type() == PinType.Data:
                "如果这个pin 是*arg 或者 **kwargs"
                if len(pin.from_) > 1:
                    raise Exception("一个节点的输入参数不能有多个连接")
                if pin.from_:
                    if not pin.is_enabled:
                        continue
                    pin_from = pin.from_[0]
                    pin_from_node = pin_from.node
                    if pin_from_node.node_type in {LSNodeItemType.PureFunc, LSNodeItemType.ClassMagicMethod}:
                        pin_ast = pin_from_node.to_ast()
                    else:
                        pin_ast = pin_from.to_ast()

                    if isinstance(pin, LSDynamicArgsSubPin):
                        in_ast_args.append(pin_ast)
                    elif isinstance(pin, LSDynamicArgsPin):
                        in_ast_args.append(ast.Starred(value=pin_ast))
                    elif isinstance(pin, LSDynamicKWArgsPin):
                        in_ast_kwargs.append(ast.keyword(value=pin_ast))
                    elif isinstance(pin, LSDataPin):
                        in_ast_kwargs.append(ast.keyword(arg=pin.title, value=pin_ast))
                    else:
                        raise ValueError(f"pin type {pin} is not supported")
                else:
                    "这种才会有初始值"
                    if isinstance(pin, LSValueDataPin):
                        in_ast_kwargs.append(pin.to_ast())
        return in_ast_args, in_ast_kwargs

    def to_ast(self):
        raise NotImplementedError

    def showEvent(self, event) -> None:
        super().showEvent(event)
        "这个很重要 有学到了"
        if self.core_layout.sizeConstraint() != QLayout.SetFixedSize:
            self.core_layout.setSizeConstraint(QLayout.SetFixedSize)


if __name__ == '__main__':
    app = QApplication()
    window = LSNodeItem(None)
    window.show()
    app.exec_()
