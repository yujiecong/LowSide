import ast

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common import Func
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSPropertyType, LSNodeSourceType
from Source.Custom.Enums.LSPinEnum import LSPinAttrType, PinFlow
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSItemData import LSRawVariableData
from Source.Custom.LSObject import LSObject
from Source.Widgets.Pin.LSLineEditDataPin import LSLineEditDataPin
from Source.Widgets.Pin.LSUserClassPin import LSUserClassPin
from Source.Widgets.Pin.LSVariableDataPin import LSVariableDataPin
from Source.Widgets.NodeItem.LSVariableNodeItem import LSVariableNodeItem
from Source.Widgets.Pin.LSCheckboxDataPin import LSCheckboxDataPin
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source.Widgets.Pin.LSExecPin import LSExecPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSSetVariableNodeItem(LSVariableNodeItem):
    @staticmethod
    def register(new_name, attr_type, attr_name):
        return LSIdentifierData.register_variable(new_name, LSRawVariableData(name=new_name,
                                                                              instance_type=LSSetVariableNodeItem.__name__,
                                                                              node_type=LSNodeItemType.Variable,
                                                                              attr_type=attr_type,
                                                                              attr_name=attr_name,
                                                                              source=LSNodeSourceType.Variable,
                                                                              ),
                                                  type_=LSPropertyType.Set)

    @staticmethod
    def unregister(name):
        LSIdentifierData.unregister_variable(name, type_=LSPropertyType.Set)

    def finished_init(self):
        super().finished_init()
        self.set_attr(self.attr_type, self.attr_name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Set")

    def init_pins_from_identifier(self):
        with self.register_variable_pin_data():
            self.input_exec_pin = LSExecPin(flow=PinFlow.In)
            self.output_exec_pin = LSExecPin(flow=PinFlow.Out)
            self.input_data_pin = self.init_input_data_pin()
            self.output_data_pin = LSVariableDataPin(flow=PinFlow.Out, title=self.name, attr_type=self.attr_type)
        self.add_pin(self.input_exec_pin)
        self.add_pin(self.output_exec_pin)
        self.add_pin(self.input_data_pin)
        self.add_pin(self.output_data_pin)
        self.finished_init()

    def init_input_data_pin(self):
        if self.attr_type == LSPinAttrType.bool:
            self.input_data_pin = LSCheckboxDataPin(flow=PinFlow.In, title=self.name, attr_type=self.attr_type,
                                                    )

        elif self.attr_type in {LSPinAttrType.str, LSPinAttrType.int, LSPinAttrType.float}:
            self.input_data_pin = LSLineEditDataPin(flow=PinFlow.In, title=self.name, attr_type=self.attr_type,
                                                    )
        elif self.attr_type == LSPinAttrType.user_class:
            self.input_data_pin = LSUserClassPin(flow=PinFlow.In, title=self.name,
                                                 attr_type=self.attr_type,
                                                 attr_name=self.attr_name,
                                                 )
        else:
            # raise ValueError(f"attr_type {self.attr_type} is not supported")
            self.input_data_pin = LSDataPin(flow=PinFlow.In, title=self.name, attr_type=self.attr_type)
        return self.input_data_pin

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()
        self.title_icon.hide()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def update_background_color(self):
        color = Func.lighten_color(self.input_data_pin.current_color, 0.8)
        color2 = Func.lighten_color(self.input_data_pin.current_color, 0.4)
        style = """
        QWidget#main_widget{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.5,
        stop:0 rgba(%s),
        stop:0.503311 rgba(%s),
        stop:1 rgba(19, 19, 19, 155));
        }

        """ % (
            ",".join(list(map(str, [color2.red(), color2.green(), color2.blue(), 155]))),
            ",".join(list(map(str, [color.red(), color.green(), color.blue(), 155])))
        )
        self.setStyleSheet(self.styleSheet() + qss + style)

    def set_variable(self, name):
        self.identifier = LSIdentifierData.variable_property_path(name, LSPropertyType.Set)
        self.name = name
        self.input_data_pin.set_title(self.name)
        self.output_data_pin.set_title(self.name)

    def set_attr(self, attr_type: str, attr_name: str):
        if self.view:
            self.view.clear_selected()

        self.attr_name = attr_name
        if attr_type!=self.attr_type:
            self.attr_type = attr_type
            self.input_data_pin.destroyed_signal.emit()
            del self.input_data_pin
            with self.register_variable_pin_data():
                self.input_data_pin=self.init_input_data_pin()

            self.add_pin(self.input_data_pin)

        self.input_data_pin.set_attr_type(attr_type)
        self.output_data_pin.set_attr_type(attr_type)

        self.update_background_color()
        QTimer.singleShot(10, self.update_lines)

    def update_lines(self):

        self.input_exec_pin.update_connected_line()
        self.output_exec_pin.update_connected_line()
        self.output_data_pin.update_connected_line()
        self.input_data_pin.update_connected_line()

    def to_ast(self):
        in_ast_args, in_ast_kwargs = self.input_pin_to_ast()

        return ast.AnnAssign(
            annotation=ast.Name(id=self.attr_type, ctx=ast.Load()),
            target=[ast.Name(id=self.name, ctx=ast.Store())],
            value=in_ast_kwargs[0], simple=1
        )


if __name__ == '__main__':
    app = QApplication()
    window = LSSetVariableNodeItem(attr_type="str")
    window.show()
    app.exec_()
