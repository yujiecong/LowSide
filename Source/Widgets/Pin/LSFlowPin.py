import typing

from PySide2.QtCore import *
from PySide2.QtGui import QMouseEvent, QCursor

from Source import Globs
from PySide2.QtWidgets import *

from Source.Custom.Enums.LSPinEnum import PinType, PinFlow, LSPinAttrType, PinConnectionFlag
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Custom import LSCommand
from Source.Custom.LSColor import PinAttrTypeExternalColor, PinAttrTypeInternalColor
from Source.Widgets.Common.LSPathItem import LSPathItem
from Source.Widgets.Pin.LSPin import LSPin
from Source.Widgets.PinIconWidget.LSPinIconWidget import LSPinIconWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


# 多继承QObject对象好像会对pyside2不友好
# 多继承时调用repaint函数会崩溃,所以只能不多继承 用组合了
# https://www.lmlphp.com/user/151533/article/item/6106478/
class LSFlowPin(LSPin):

    def init_properties(self):
        super().init_properties()
        self.setToolTip(f"属性类型:{self.attr_type}")

    def init_ui(self):
        """
        data 的 pin 是画出来的 所以他的icon是一个特殊的
        :return:
        """
        super().init_ui()
        self.pin_layout = QGridLayout(self)
        self.icon_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.update_color()
        self._pin_icon: LSPinIconWidget = self.pin_icon_type(self, self.attr_type)
        self.init_body()

    def init_connection(self):
        super().init_connection()

    def init_body(self):
        # self.title_label = LSPinLabel(self.title)
        self.title_label = QLabel(self.title)
        # self.title_label = LSPinLineEdit(self.title)
        # self.title_label.setFixedWidth(5)
        # self.title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.title_label.setReadOnly(True)
        # self.title_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.title_label.setMouseTracking(False)
        if self.get_flow() == PinFlow.In:
            self.pin_layout.addWidget(self._pin_icon,0,0)
            self.pin_layout.addWidget(self.title_label,0,1)
            self.pin_layout.addItem(self.icon_spacer,0,2)

            self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)
            self.pin_layout.setContentsMargins(0, 0, 0, 0)
            # self.pin_layout.setSpacing(7)

        elif self.get_flow() == PinFlow.Out:
            self.pin_layout.addItem(self.icon_spacer,0,0)
            self.pin_layout.addWidget(self.title_label,0,1)
            self.pin_layout.addWidget(self._pin_icon,0,2)

            self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)
            self.pin_layout.setContentsMargins(5, 0, 0, 0)
            # self.pin_layout.setSpacing(3)

    def init_attrs(self):
        super().init_attrs()
        self.temp_line: LSPathItem = None

    @property
    def pin_icon(self) -> LSPinIconWidget:
        raise NotImplementedError

    @property
    def pin_icon_type(self):
        raise NotImplementedError

    def set_normal_style(self):
        self.pin_icon.set_normal_style()

    def set_hover_style(self):
        self.pin_icon.set_hover_style()

    def set_connected_style(self):
        self.pin_icon.set_connected_style()

    def set_disconnected_style(self):
        self.pin_icon.set_disconnected_style()



    def update_connection_style(self):
        if self.is_out_connected or self.is_in_connected:
            self.set_connected_style()
        else:
            self.set_disconnected_style()
        self.set_normal_style()

    def destoryed(self):
        self.destroyed_signal.emit()

    def destruct(self):
        super().destruct()
        for line in self.in_lines:
            line.destruct()
        for line in self.out_lines:
            line.destruct()
        self.in_lines.clear()
        self.out_lines.clear()

    def when_pin_released(self, event: QMouseEvent) -> None:
        "若是此次鼠标释放的位置在另一个pin上,则连接两个pin"
        "若不是,则删除这条线"
        cursor_pos = QCursor.pos()
        self.lineReleased_signal.emit(self, cursor_pos)
        for line in self.out_lines:
            line.set_normal_style()
        for line in self.in_lines:
            line.set_normal_style()
    def when_pin_moved(self, event: QMouseEvent) -> None:
        "下面就可以开始写拖拽线了,生成一条线"
        if LSPin.LMouseIsPressed:
            "这里面的是scene里的坐标系坐标"
            cursor_pos = QCursor.pos()
            view_pos = self.view.mapFromGlobal(cursor_pos)
            scene_pos = self.view.mapToScene(view_pos)
            self.update_temp_line(self.right_line_start_pos(), scene_pos)
            "如果这个时候落下到另一个pin 需要有弹窗,并且触发hover效果"
            "那么怎么才能触发到hover呢"
            "只能通过global的坐标 拿到,接着.判断这个坐标是否落在了某个pin上, 还有更好的办法吗"
            "因为触发不了 enterEvent 但是graphicview能触发鼠标移动事件"
            self.lineMoved_signal.emit(self, cursor_pos)

    def when_pin_pressed(self, event):
        super().mousePressEvent(event)
        "创建一条线"
        "在一个控件里就可以用accept来阻止事件冒泡 但是graphics view不行"
        "由于是当前控件的鼠标落下的位置 坐标系是当前icon控件 所以要转化成view的坐标系"
        "目前只想到的办法是转成全局再转回来"
        self.temp_line.show()
        self.update_temp_line(self.right_line_start_pos(), self.right_line_start_pos())

        self.view.scene().prompt_label.move(self.right_line_start_pos())
        self.view.scene().prompt_label.show()
        for line in self.out_lines:
            line.set_lowlight_style()
        for line in self.in_lines:
            line.set_lowlight_style()

    def update_temp_line(self, start: QPoint, end: QPoint):
        if self.get_flow() == PinFlow.In:
            self.temp_line.update_path(end, start)
        else:
            self.temp_line.update_path(start, end)

    def update_color(self):
        self.enabled_color = PinAttrTypeExternalColor(self.attr_type)
        self.current_color = self.enabled_color
        self.internal_color = PinAttrTypeInternalColor(self.attr_type)
        if self.temp_line:
            self.temp_line.set_color(self.current_color)

        for line in self.out_lines:
            line.update_pen_color()

        for line in self.in_lines:
            line.update_pen_color()

    def set_title(self, title: str):
        self.title = title
        self.title_label.setText(title)

    def set_attr_type(self, attr_type: str):
        self.attr_type = attr_type
        self.setToolTip(f"属性类型:{attr_type}")
        self.update_color()

    def set_view(self, view):
        super().set_view(view)
        self.temp_line = LSPathItem(color=self.current_color)
        self.temp_line.set_view(view)

        for line in self.out_lines:
            line.set_view(view)
        # self.temp_line.hide()

    def right_line_start_pos(self) -> QPoint:
        if self.get_flow() == PinFlow.In:
            pos = self.pin_icon.icon.left_pos()
        else:
            pos = self.pin_icon.icon.right_pos()

        "这里在未显示的时候 返回的坐标是错误的"
        # global_icon_pos = self.pin_icon.icon.mapToParent(right_pos)
        # global_icon_pos = self.pin_icon.mapToParent(global_icon_pos)
        # global_icon_pos = self.mapToParent(global_icon_pos)
        # global_icon_pos=self.node.mapToParent(global_icon_pos)
        global_icon_pos = self.pin_icon.icon.mapToGlobal(pos)
        if self.view:
            return self.view.mapToScene(
                self.view.mapFromGlobal(
                    global_icon_pos
                )
            ).toPoint()
        else:
            return QPoint()

    def left_line_start_pos(self) -> QPoint:
        global_icon_pos = self.pin_icon.icon.mapToGlobal(self.pin_icon.icon.left_pos())
        if self.view:
            return self.view.mapToScene(
                self.view.mapFromGlobal(
                    global_icon_pos
                )
            ).toPoint()
        else:
            return QPoint()

    def update_connected_line(self):
        if not self.view:
            return

        right_line_start_pos = self.right_line_start_pos()
        left_line_start_pos = self.left_line_start_pos()
        my_flow = self.get_flow()
        if my_flow == PinFlow.In:
            for idx, pin in enumerate(self.to_):
                to__left_line_start_pos = pin.left_line_start_pos()
                self.out_lines[idx].update_path(right_line_start_pos, to__left_line_start_pos)

            for pin in self.from_:
                for line in self.in_lines:
                    line.update_path(pin.right_line_start_pos(), left_line_start_pos)

        elif my_flow == PinFlow.Out:
            for idx, line in enumerate(self.out_lines):
                "此时 to_ 不一定有view  所以这里会报错"
                to__left_line_start_pos = self.to_[idx].left_line_start_pos()
                line.update_path(right_line_start_pos, to__left_line_start_pos)

            for pin in self.from_:
                for line in self.in_lines:
                    line.update_path(pin.right_line_start_pos(), left_line_start_pos)

    def can_be_connected(self, sender_pin: "LSFlowPin") -> PinConnectionFlag:
        """
        一旦检测到 sender pin 是已经链接了其他的pin的 那么就要说 这个是replace掉原来的pin的
        :param flow:
        :param sender_pin:
        :return:
        """
        flow = self.get_flow()
        # 如果我是 out exec pin 只能有一个输出
        if flow == PinFlow.In:
            "只允许一个exec pin 被一个exec pin"
            exec_condition1 = [self.is_in_connected, sender_pin.get_flow() == PinFlow.Out,
                              sender_pin.get_type() == PinType.Exec,self.get_type() == PinType.Exec]

            "只允许一个exec pin 出一个exec pin"
            exec_condition2 = [sender_pin.is_out_connected,sender_pin.get_flow() == PinFlow.Out,
                               sender_pin.get_type() == PinType.Exec,self.get_type() == PinType.Exec]

            data_condition = [self.is_in_connected, sender_pin.get_flow() == PinFlow.Out,
                              self.get_type() == PinType.Data]
            if all(exec_condition1):
                return PinConnectionFlag.ReplaceExecConnect
            elif all(exec_condition2):
                return PinConnectionFlag.OnlyOneExecConnect
            elif all(data_condition):
                return PinConnectionFlag.ReplaceDataConnect

        # 如果我是in data
        if self is sender_pin:
            return PinConnectionFlag.IsSelfError
        elif sender_pin.get_flow() == flow:
            return PinConnectionFlag.FlowError

        elif sender_pin.get_type() != self.get_type():
            return PinConnectionFlag.PinTypeError
        elif sender_pin.attr_type != self.attr_type:
            "object类型能接受任何类型的数据"
            if sender_pin.attr_type == LSPinAttrType.object or self.attr_type == LSPinAttrType.object:
                pass
            else:
                return PinConnectionFlag.AttrTypeError

        return PinConnectionFlag.CanConnect

    def connect_pin(self, other_pin: "LSFlowPin", ):
        my_flow = self.get_flow()
        if my_flow == PinFlow.In:
            self.in_pin_connect(other_pin)
        elif my_flow == PinFlow.Out:
            self.out_pin_connect(other_pin)
        elif my_flow == PinFlow.Both:
            self.out_pin_connect(other_pin)
        else:
            raise ValueError("flow error")

        self.connect_finished()
        other_pin.connect_finished()


    def disconnect_pin(self, other_pin: "LSFlowPin"):

        my_flow = self.get_flow()
        if my_flow == PinFlow.In:
            self._in_pin_disconnect(other_pin)
        else:
            if self.view:
                undo_stack = self.view.undo_stack
                undo_stack.push(LSCommand.LSPinDisconnectCommand(self,other_pin))
            self._out_pin_disconnect(other_pin)

        self.disconnect_finished()
        other_pin.disconnect_finished()

    def start_update(self):
        # self.update_item()
        QTimer.singleShot(10, self.update_item)

    def update_item(self):
        self.update_connected_line()
        self.update_connection_style()

    def disconnect_finished(self):
        if not self.from_:
            self.is_in_connected = False
        else:
            self.is_in_connected = True

        if not self.to_:
            self.is_out_connected = False
        else:
            self.is_out_connected = True

        self.pin_icon.icon.is_in_connected = self.is_in_connected
        self.pin_icon.icon.is_out_connected = self.is_out_connected

        self.pin_icon.is_in_connected = self.is_in_connected
        self.pin_icon.is_out_connected = self.is_out_connected

        self.start_update()

    def connect_finished(self):
        self.pin_icon.icon.is_in_connected = self.is_in_connected
        self.pin_icon.icon.is_out_connected = self.is_out_connected

        self.pin_icon.is_in_connected = self.is_in_connected
        self.pin_icon.is_out_connected = self.is_out_connected

        if self.view:
            undo_stack = self.view.undo_stack
            if self.to_ and self.get_flow() == PinFlow.Out:
                undo_stack.push(LSCommand.LSPinConnectCommand(self))
            self.start_update()


    def in_pin_connect(self, out_pin: "LSFlowPin"):
        """
            in pin 只允许被链接一次

        :param out_pin:
        :return:
        """
        out_pin.out_pin_connect(self)
        # if out_pin in self.from_:
        #     return True
        #
        # connect_type = self.can_be_connected(out_pin)
        # if connect_type in {ConnectType.CanConnect, ConnectType.ReplaceConnect}:
        #     if connect_type == ConnectType.ReplaceConnect:
        #         "要把之前链接的取消断掉"
        #         out_pin.disconnect_pin(self)
        #     new_line = self.view.create_line(self, out_pin)
        #
        #     self.from_.append(out_pin)
        #     self.temp_line.hide()
        #
        #     out_pin.to_ = self
        #     out_pin.out_line=new_line
        #
        #     self.in_lines.append(new_line)
        #
        #     self.is_in_connected=True
        #     out_pin.is_out_connected=True
        #
        # self.temp_line.hide()

    def out_pin_connect(self, in_pin: "LSFlowPin"):
        """
            out pin 只链接一次 in pin
            in pin 可以被多个out pin链接

        :param flow:
        :param in_pin:
        :return:
        """

        if in_pin in self.to_:
            return True
        connect_type = in_pin.can_be_connected(self)
        if connect_type in {PinConnectionFlag.CanConnect,
                            PinConnectionFlag.ReplaceExecConnect,
                            PinConnectionFlag.ReplaceDataConnect,
                            PinConnectionFlag.OnlyOneExecConnect,
                            }:
            if connect_type == PinConnectionFlag.ReplaceExecConnect:
                "exec pin 只允许连一个 要把之前链接的取消断掉"
                for from_pin in in_pin.from_:
                    from_pin.disconnect_pin(in_pin)
            elif connect_type==PinConnectionFlag.ReplaceDataConnect:
                for from_pin in in_pin.from_:
                    from_pin.disconnect_pin(in_pin)
            elif connect_type == PinConnectionFlag.OnlyOneExecConnect:
                self.disconnect_pin(self.to_[0])

            self.to_.append(in_pin)
            line_item = LSPathItem(color=self.current_color, in_pin=in_pin, out_pin=self)
            in_pin.from_.append(self)
            in_pin.in_lines.append(line_item)
            in_pin.is_in_connected = True

            self.is_out_connected = True
            self.out_lines.append(line_item)

            if self.view:
                line_item.set_view(self.view)

        else:
            ls_print(f"连接失败,{connect_type}")

    def _out_pin_disconnect(self, other_pin):
        """
        我是一个out pin
        如果直接调用 会导致style不能直接更新
        :return:
        """
        disconnect_pin_idx = self.to_.index(other_pin)
        line = self.out_lines[disconnect_pin_idx]

        other_pin.in_lines.remove(line)
        other_pin.from_.remove(self)

        if self.view:
            line.destruct()

        self.to_.remove(other_pin)
        self.out_lines.remove(line)

    def _in_pin_disconnect(self, out_pin: "LSFlowPin"):
        """
        我是一个 in pin
        取消两个pin的连接 得告诉当前pin具体是哪个pin
        :return:
        """
        return out_pin.disconnect_pin(self)

    def to_ast(self):
        raise NotImplementedError

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        LSPin.LMouseIsPressed=True
        event.accept()
        if event.button() == Qt.LeftButton:
            self.when_pin_pressed(event)
        self.is_double_clicked = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        event.accept()
        if LSPin.LMouseIsPressed:
            self.when_pin_moved(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_double_clicked=True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if LSPin.LMouseIsPressed:
            LSPin.LMouseIsPressed = False
            self.when_pin_released(event)

        if self.is_double_clicked:
            self.doubleClicked_signal.emit()
    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.set_hover_style()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.set_normal_style()




if __name__ == '__main__':
    app = QApplication()
    window = LSFlowPin()
    window.show()
    app.exec_()
