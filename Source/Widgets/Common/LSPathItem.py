from typing import *

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common import Func
from Source.Common.Enums import ItemZValue
from Source.Custom.LSColor import PinLineColor
from Source.Common.Func import OS, PainterPath
from Source.Common.Logger import ls_print
from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()

class PathItemSignalObject(QObject):
    lineDoubleClicked=Signal(object,object,object)
    def __init__(self):
        super().__init__()

class LSPathItem(QGraphicsPathItem, LSObject):

    NormalPenWidth = 3
    HoverPenWidth = 5

    def __init__(self,color=PinLineColor(),in_pin:"LSPin"=None, out_pin:"LSPin"=None,*args, **kwargs):
        self.view:Union[QGraphicsView]=None

        self.in_color = color
        self.out_color = color
        self.in_pin:AbsLSPin=in_pin
        self.out_pin:AbsLSPin=out_pin

        if in_pin:
            self.in_color = in_pin.current_color
        if out_pin:
            self.out_color = out_pin.current_color

        self.low_light_color = Func.lighten_color(color, 0.3)

        super().__init__(*args, **kwargs)
        LSObject.__init__(self, *args, **kwargs)

        if in_pin and out_pin:
            # self.init_pen()
            self.connected(in_pin,out_pin)


    def init_attrs(self):
        super().init_attrs()
        self.out_pin = None
        self.in_pin  = None
        self._path:QPainterPath=None
        self.signal_object=PathItemSignalObject()

    def init_properties(self):
        super().init_properties()
        self.setZValue(ItemZValue.Line)
        self.init_pen()
        "使用该类描边来检测鼠标是否落在线上"
        self.stroker = QPainterPathStroker()
        self.stroker.setWidth(LSPathItem.HoverPenWidth)

        self.setAcceptHoverEvents(True)

    def init_pen(self):
        self.pen = QPen()
        self.pen.setWidth(LSPathItem.NormalPenWidth)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.pen.setCosmetic(True)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.pen.setColor(self.out_color)
        self.setPen(self.pen)

    def init_ui(self):
        super().init_ui()

    def init_connection(self):
        super().init_connection()

    def destruct(self):
        self.view.scene().removeItem(self)


    def set_view(self,view):
        super().set_view(view)
        # self.signal_object.disconnect(view.create_bidirectional_node)
        self.signal_object.lineDoubleClicked.connect(view.create_bidirectional_item)
        self.view.scene().addItem(self)


    def set_hover_style(self):
        self.pen.setWidth(LSPathItem.HoverPenWidth)
        self.setPen(self.pen)

        "顺便让两个pin也变色"
        if self.out_pin:
            self.out_pin.set_hover_style()
        if self.in_pin:
            self.in_pin.set_hover_style()

        self.update_pen_color()

    def set_lowlight_style(self):
        self.pen.setWidth(LSPathItem.NormalPenWidth)
        self.pen.setColor(self.low_light_color)
        self.setPen(self.pen)
        self.update_pen_color()

    def set_normal_style(self):
        self.pen.setWidth(LSPathItem.NormalPenWidth)
        self.pen.setColor(self.out_color)
        self.setPen(self.pen)
        self.update_pen_color()
        "顺便让两个pin也变色"
        if self.out_pin:
            self.out_pin.set_normal_style()
        if self.in_pin:
            self.in_pin.set_normal_style()

    def connected(self, in_pin, out_pin):
        self.out_pin = out_pin
        self.in_pin = in_pin

    def disconnected(self):
        return self.out_pin.disconnect_pin(self.in_pin)

    def set_color(self, color):
        self.out_color = color
        self.in_color = color

    def update_path(self, p1: QPoint, p2: QPoint):
        """

        :param p1:
        :param p2:
        :return:
        """
        self._path = PainterPath.create_line(p1.toTuple(), p2.toTuple())
        self.setPath(self._path)
        self.update_pen_color()

    def update_pen_color(self,):
        if self.in_pin or self.out_pin:
            self.in_color = self.in_pin.current_color
            # if self.out_pin:
            self.out_color = self.out_pin.current_color

        # top_left = self.boundingRect().topLeft()
        # bottom_right = self.boundingRect().bottomRight()
        # gradient_color = QLinearGradient(top_left.x(), 0, bottom_right.x(), 0)

        # if self._path.elementAt(0).x<self._path.elementAt(self._path.elementCount()-1).x:
        #     gradient_color.setColorAt(0, self.out_color)
        #     gradient_color.setColorAt(0.5, self.out_color)
        #     gradient_color.setColorAt(0.5001, self.in_color)
        #     gradient_color.setColorAt(1, self.in_color)
        # else:
        #     gradient_color.setColorAt(0, self.in_color)
        #     gradient_color.setColorAt(0.5, self.in_color)
        #     gradient_color.setColorAt(0.5001, self.out_color)
        #     gradient_color.setColorAt(1, self.out_color)
        self.pen.setBrush(self.out_color)
        self.setPen(self.pen)

    def mouseDoubleClickEvent(self, event:QGraphicsSceneMouseEvent):
        """
        在这里创建一个 结点
        :param event:
        :return:
        """
        self.signal_object.lineDoubleClicked.emit(event.pos(),self.in_pin,self.out_pin)



    def hoverMoveEvent(self, event:QGraphicsSceneHoverEvent=...) -> None:
        stroked_path = self.stroker.createStroke(self._path)
        if stroked_path.contains(event.scenePos()):
            self.set_hover_style()
        else:
            self.set_normal_style()


    def hoverLeaveEvent(self, event:QGraphicsSceneHoverEvent) -> None:
        stroked_path = self.stroker.createStroke(self._path)
        if not stroked_path.contains(event.scenePos()):
            self.set_normal_style()

    def paint(self,
              painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: Optional[QWidget] = ...) -> None:
        painter.setRenderHint(QPainter.Antialiasing, True)
        super().paint(painter, option, widget)

    def mousePressEvent(self, event:QMouseEvent):
        key_event = QApplication.keyboardModifiers()
        if key_event&Qt.AltModifier:
            self.disconnected()
        elif event.button()==Qt.MiddleButton:
            self.disconnected()


    def __repr__(self):
        return f"{self.__class__.__name__} {self.out_pin} {self.in_pin}"

if __name__ == '__main__':
    app = QApplication()
    window = LSPathItem(None)
    window.show()
    app.exec_()
