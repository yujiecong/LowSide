from Source import Globs
from PySide2.QtWidgets import *

from Source.Custom.Enums.LSPinEnum import PinType, PinFlow, PinConnectionFlag
from Source.Common.Func import OS
from Source.Widgets.Pin.LSFlowPin import LSFlowPin
from Source.Widgets.PinIconWidget.LSBidirectionalPinIconWidget import LSBidirectionalPinWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSBidirectionalPin(LSFlowPin):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_attrs(self):
        super().init_attrs()
        self.is_in_connected = False
        self.is_out_connected = False

        self.temp_flow:PinFlow=None

    def init_properties(self):
        super().init_properties()
        self.set_normal_style()

    def init_body(self):
        pass

    def init_ui(self):
        super().init_ui()
        self.pin_layout.setContentsMargins(0, 0, 0, 0)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)
        # self.setStyleSheet("background-color:red;")

    def init_connection(self):
        super().init_connection()

    @property
    def pin_icon(self) -> LSBidirectionalPinWidget:
        return self._pin_icon

    @property
    def pin_icon_type(self):
        return LSBidirectionalPinWidget

    def get_type(self) -> PinType:
        return PinType.Exec

    def get_flow(self) -> PinFlow:
        """
        如果有界面的时候 根据鼠标位置判断
        没有界面的时候 就根据变量指定
        :return:
        """
        # if not self.view:
        # print("self.target_flow",self.target_flow)

        if self.temp_flow:
            return self.temp_flow

        return PinFlow.Both

        # cursor_pos = QCursor.pos()
        # view_pos = self.view.mapFromGlobal(cursor_pos)
        # mouse_scene_pos = self.view.mapToScene(view_pos)
        # left_pos = self.left_line_start_pos()
        # right_pos = self.right_line_start_pos()
        #
        # center: QPoint = (left_pos + right_pos) / 2
        #
        # if mouse_scene_pos.x() > center.x():
        #     fl = PinFlow.Out
        # else:
        #     fl= PinFlow.In
        #
        # return fl

    def set_disconnected_style(self):
        if not self.is_out_connected and not self.is_in_connected:
            self.pin_icon.set_disconnected_style()

    def update_connected_line(self):

        for idx,pin in enumerate(self.to_):
            self.out_lines[idx].update_path(self.right_line_start_pos(), pin.left_line_start_pos())

        for idx,pin in enumerate(self.from_):

            self.in_lines[idx].update_path(pin.right_line_start_pos(), self.left_line_start_pos())

    def can_be_connected(self, sender_pin: "LSFlowPin") -> PinConnectionFlag:
        if sender_pin is self:
            return PinConnectionFlag.IsSelfError

        sender_flow = sender_pin.get_flow()
        if sender_flow ==PinFlow.Out:
            self.temp_flow=PinFlow.In
        elif sender_flow ==PinFlow.In:
            self.temp_flow=PinFlow.Out
        elif sender_flow ==PinFlow.Both:
            self.temp_flow=PinFlow.In
        else:
            raise ValueError("flow error")
        result=super().can_be_connected(sender_pin)
        "用完之后要清空"
        self.temp_flow=None
        return result

    def connect_pin(self, other_pin: "LSFlowPin"):
        if other_pin.get_flow()==PinFlow.Out:
            flow=PinFlow.In
        elif other_pin.get_flow()==PinFlow.In:
            flow=PinFlow.Out
        elif other_pin.get_flow()==PinFlow.Both:
            flow=PinFlow.Out
        else:
            raise ValueError("flow error")

        self.temp_flow=flow
        LSFlowPin.connect_pin(self, other_pin, )
        self.temp_flow=None

    def __repr__(self):
        return f"LSBidirectionalPin pos={self.pos()}"


if __name__ == '__main__':
    app = QApplication()
    window = LSBidirectionalPin()
    window.show()
    app.exec_()
