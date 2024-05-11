from typing import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Source import Globs
from Source.Common.DataClass import LSPinConnectInfo
from Source.Common.Enums import LSNameField, LSNameMeta
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Common.Func import OS
from Source.Widgets.Pin.LSFlowPin import LSFlowPin
from Source.Widgets.NodeItem.LSItem import LSItem
from Source.Widgets.Common.LSPathItem import LSPathItem
from Source.Widgets.Pin.LSPin import LSPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSConnectableItem(LSItem, ):
    class CustomKeys(LSNameMeta):
        pos = LSNameField()

    CurHoverPin: Optional[LSPin] = None
    IsPressedPin = False
    IsPressed = False

    def init_attrs(self):
        super().init_attrs()
        self.pins: List[LSFlowPin] = []

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def destruct(self):
        super().destruct()
        self.disconnect_all_pins()
        for pin in self.pins:
            pin.destruct()

    def set_view(self, view):
        super().set_view(view)
        for pin in self.pins:
            pin.set_view(view)

        for pin in self.pins:
            pin.update_connected_line()
            pin.update_connection_style()

    def can_be_duplicated(self):
        return True

    def pin_at(self, cursor_pos: QPoint) -> Union[LSPin, None]:
        raise NotImplementedError

    def add_pin(self):
        raise NotImplementedError

    def connect_pin_by_pos(self, target_item: "LSConnectableItem", row, target_row):
        for pin in self.pins:
            if pin.get_flow() == PinFlow.Out and pin.row == row:
                for target_pin in target_item.pins:
                    if target_pin.get_flow() == PinFlow.In and target_pin.row == target_row:
                        pin.connect_pin(target_pin)
                        return True
        return False

    def connect_pin_by_uuid(self, to_node_uuid, pin_uuid, to_pin_uuid):
        my_pin = self.find_pin_by_uuid(pin_uuid)
        to_item = self.view.uuid_2_ls_item.get(to_node_uuid)
        if to_item:
            to_pin = to_item.find_pin_by_uuid(to_pin_uuid)
            if to_pin:
                my_pin.connect_pin(to_pin)

    def find_pin_by_uuid(self, pin_uuid):
        for pin in self.pins:
            if pin.uuid_== pin_uuid:
                return pin

        raise ValueError(f"can't find pin by uuid:{pin_uuid}")
    def get_pin_connect_info(self,flow=PinFlow.All):
        """
        返回pin的信息
        :return:
        """
        pin_connect_info = []
        pins = self.pins

        if flow==PinFlow.Out:
            pins=[pin for pin in pins if pin.get_flow() == PinFlow.Out]

        for pin in pins:
            pin: LSFlowPin
            flow = pin.get_flow()
            if flow == PinFlow.Out:
                for to_out_pin in pin.to_:
                    to_node: LSConnectableItem = to_out_pin.node
                    pin_connect_info.append(LSPinConnectInfo(self.uuid_, to_node.uuid_, pin.uuid_, to_out_pin.uuid_))
            elif flow == PinFlow.In:
                for from_in_pin in pin.from_:
                    from_node: LSConnectableItem = from_in_pin.node
                    pin_connect_info.append(LSPinConnectInfo(from_node.uuid_, self.uuid_, from_in_pin.uuid_, pin.uuid_))

            elif flow == PinFlow.Both:
                for to_out_pin in pin.to_:
                    to_node: LSConnectableItem = to_out_pin.node
                    pin_connect_info.append(LSPinConnectInfo(self.uuid_, to_node.uuid_, pin.uuid_, to_out_pin.uuid_))
                for from_in_pin in pin.from_:
                    from_node: LSConnectableItem = from_in_pin.node
                    pin_connect_info.append(LSPinConnectInfo(from_node.uuid_, self.uuid_, from_in_pin.uuid_, pin.uuid_))




        return pin_connect_info

    def disconnect_all_pins(self):
        for pin in self.pins:
            for from_pin in pin.from_:
                from_pin.disconnect_pin(pin)

            for to_pin in pin.to_:
                pin.disconnect_pin(to_pin)

    def _pin_line_released(self, sender_pin: LSFlowPin, cursor_pos: QPoint):
        """
        首先判断是什么类型的node
        然后判断是不是可以连接到这个pin
        :param cursor_pos:
        :return:
        """

        view_pos = self.view.mapFromGlobal(cursor_pos)
        items: Union[QGraphicsProxyWidget, QGraphicsItem] = self.view.items(view_pos)
        self.view.m_scene.prompt_label.hide()
        is_connected = False
        if items:
            item = items[0]
            if isinstance(item, QGraphicsProxyWidget):
                widget: QWidget = item.widget()
                if widget:
                    if isinstance(widget, LSConnectableItem):
                        connectable_item: LSConnectableItem = widget
                        pin:LSFlowPin = connectable_item.pin_at(cursor_pos)
                        if pin:
                            is_connected = sender_pin.connect_pin(pin)
                        else:
                            pass
            else:
                pass

        if not is_connected:
            sender_pin.temp_line.hide()

    def _pin_line_moved(self, sender_pin: LSFlowPin, cursor_pos: QPoint):
        """
        首先判断是什么类型的node
        然后判断是不是要高亮
        :param cursor_pos:
        :return:
        """
        view_pos = self.view.mapFromGlobal(cursor_pos)
        items: Union[QGraphicsProxyWidget, QGraphicsItem] = self.view.items(view_pos)
        self.view.scene().prompt_label.move(self.view.mapToScene(view_pos).toPoint() + QPoint(10, 10))
        if items:
            item = items[0]
            if isinstance(item, QGraphicsProxyWidget):
                widget: QWidget = item.widget()
                if widget:
                    if isinstance(widget, LSConnectableItem):
                        connectable_item = widget
                        pin = connectable_item.pin_at(cursor_pos)
                        if pin:
                            LSConnectableItem.CurHoverPin = pin
                            pin.set_hover_style()
                            self.view.scene().prompt_label.set_hover_pin_style(pin, sender_pin)
                        else:
                            self.view.scene().prompt_label.set_normal_style()
                            if LSConnectableItem.CurHoverPin:
                                LSConnectableItem.CurHoverPin.set_normal_style()
                                LSConnectableItem.CurHoverPin = None

                    elif isinstance(widget, type(self.view.scene().prompt_label)):
                        pass
            elif isinstance(item, LSPathItem):
                self.view.scene().prompt_label.set_normal_style()
                if LSConnectableItem.CurHoverPin:
                    LSConnectableItem.CurHoverPin.set_normal_style()
                    LSConnectableItem.CurHoverPin = None
        else:
            "如果没东西"
            self.view.scene().prompt_label.set_normal_style()
            if LSConnectableItem.CurHoverPin:
                LSConnectableItem.CurHoverPin.set_normal_style()
                LSConnectableItem.CurHoverPin = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """

        :param event:
        :return:
        """
        # 这个super的位置也不能动. 不然会导致move不了
        super().mousePressEvent(event)
        LSConnectableItem.IsPressed=True
        "如果没有这个 会继续传递给scene导致移动不了.."
        if event.button() == Qt.LeftButton:
            event.accept()
            pin = self.pin_at(QCursor.pos())
            if pin:
                LSConnectableItem.IsPressedPin = True
            else:
                LSConnectableItem.IsPressedPin = False
            self.setFocus()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        LSConnectableItem.IsPressed=False


    def moveEvent(self, event: QMoveEvent) -> None:
        # super().moveEvent(event)
        for pin in self.pins:
            pin.update_connected_line()

    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.setCursor(Qt.SizeAllCursor)

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.setCursor(Qt.ArrowCursor)


if __name__ == '__main__':
    app = QApplication()
    window = LSConnectableItem()
    window.show()
    app.exec_()
