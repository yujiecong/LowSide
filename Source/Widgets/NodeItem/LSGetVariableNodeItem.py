import ast

from PySide2.QtCore import QTimer

from Source import Globs
from PySide2.QtWidgets import *

from Source.Common import Func
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSPropertyType, LSNodeSourceType
from Source.Custom.Enums.LSPinEnum import PinFlow, LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSItemData import LSRawVariableData
from Source.Widgets.NodeItem.LSVariableNodeItem import LSVariableNodeItem
from Source.Widgets.Pin.LSDataVariablePin import LSDataVariablePin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSGetVariableNodeItem(LSVariableNodeItem):
    @staticmethod
    def register(new_name, attr_type,attr_name):
        return LSIdentifierData.register_variable(new_name, LSRawVariableData(name=new_name,
                                                                              instance_type=LSGetVariableNodeItem.__name__,
                                                                              node_type=LSNodeItemType.Variable,
                                                                              attr_type=attr_type,
                                                                              attr_name=attr_name,
                                                                              source=LSNodeSourceType.Variable,
                                                                              ),
                                                  type_=LSPropertyType.Get)
    @staticmethod
    def unregister(name):
        LSIdentifierData.unregister_variable(name, type_=LSPropertyType.Get)

    # @classmethod
    # def deserialize(cls, wrapper: "LSGetVariableNodeItem") -> "LSGetVariableNodeItem":
    #     return super().deserialize(wrapper)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attr(self.attr_type,self.attr_name)
        self.set_variable(self.name)

    def init_pins_from_identifier(self):
        self.pin = LSDataVariablePin(flow=PinFlow.Out,
                                     title=self.name,
                                     attr_type=LSPinAttrType.object,
                                     )
        self.add_pin(self.pin)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()

    def init_title_layout(self):
        pass

    def init_body_layout(self):
        super().init_body_layout()
        self.body_layout.setContentsMargins(20, 6, 6, 6)
        # self.main_widget.paintEvent=lambda arg:self.main_paintEvent(self.main_widget,arg,self)

    def init_connection(self):
        super().init_connection()

    def init_pin(self):
        self.set_variable(self.name)

    def update_background_color(self):
        color = Func.lighten_color(self.pin.current_color, 0.8)
        color2 = Func.lighten_color(self.pin.current_color, 0.4)
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

    def set_title(self, *args):
        pass

    def set_variable(self,name):
        """
        由于存在 相同类型但是不同来源的类型
        :param name:
        :return:
        """
        self.name = name
        self.identifier= LSIdentifierData.variable_property_path(name, LSPropertyType.Get)
        self.pin.set_title(self.name)

        QTimer.singleShot(10, self.pin.update_connected_line)

    def set_attr(self, attr_type: str, attr_name:str):
        if self.view:
            self.view.clear_selected()
        self.attr_type=attr_type
        self.attr_name=attr_name
        self.pin.set_attr_type(attr_type)
        self.pin.update_color()
        self.update_background_color()
        self.pin.update_connected_line()


    def to_ast(self):
        return ast.Name(id=self.name)

    # def paintEvent(self, arg__1:QPaintEvent) -> None:
    #     super().paintEvent(arg__1)
    #     color = self.variable_pin.external_color.color
    #     self.setStyleSheet(qss +"""QWidget#main_widget{
    #     background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.5,
    #     stop:0 rgba(91,144,178, 255),
    #     stop:0.503311 rgba(%s),
    #     stop:1 rgba(19, 19, 19, 155));
    #     }"""%((",".join([str(i) for i in color]))))
    # @staticmethod
    # def main_paintEvent(self, arg__1:QPaintEvent,inst) -> None:
    #     QWidget.paintEvent(self,arg__1)
    #
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    #     _color = QLinearGradient(0, 0, 1, self.height())
    #     external_color=QColor(*inst.variable_pin.external_color.color)
    #     external_color.setAlpha(55)
    #     _color.setColorAt(0, Qt.transparent)
    #     _color.setColorAt(0.2, Func.lighten_color(external_color, 0.7))
    #     _color.setColorAt(0.5, Func.lighten_color(external_color, 0.4))
    #     _color.setColorAt(1, external_color)
    #     # _color.setColorAt(pos, QColor(22,22,22))
    #     self.brush = QBrush(_color)
    #
    #     painter.begin(self)
    #     painter.setBrush(self.brush)
    #     painter.setPen(QPen(Qt.transparent))
    #
    #     rect:QRect=self.rect()
    #     rect.setX(self.width()/6)
    #     rect.setWidth(self.width()*5/7)
    #     rect.setHeight(self.height()*4/5)
    #
    #     painter.drawRect(rect)
    #     painter.end()


if __name__ == '__main__':
    app = QApplication()
    window = LSGetVariableNodeItem()
    window.show()
    app.exec_()
