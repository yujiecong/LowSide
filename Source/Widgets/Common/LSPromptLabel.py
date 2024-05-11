from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Custom.LSIcons import LSIcons
from Source.Custom.Enums.LSPinEnum import PinConnectionFlag
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class PromptState:
    Normal = 0
    CanBeConnected = 1
    CanNotBeConnected = 2


class _PromptLabelIcon(QLabel, LSObject):
    NormalFixedWidth = 14
    NormalFixedHeight = 14

    TITLE_HEIGHT=NormalFixedWidth/3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self)

    def init_properties(self):
        super().init_properties()
        self.setObjectName("_PromptLabelIcon")
        self.setScaledContents(True)
        self.pen.setWidth(1)
        self.brush.setStyle(Qt.SolidPattern)
        self.setFixedSize(_PromptLabelIcon.NormalFixedWidth, _PromptLabelIcon.NormalFixedHeight)

    def init_attrs(self):
        super().init_attrs()
        self.state = PromptState.Normal
        self.pen = QPen()
        self.brush = QBrush()
        self.color1 = QColor(131, 131, 131)
        self.color2 = QColor(217, 217, 217)


    def set_can_not_be_connected_style(self):
        self.setPixmap(LSIcons.false_svg)
        # self.setFixedSize(32, 32)
        self.state = PromptState.CanNotBeConnected


    def set_can_be_connected_style(self):
        self.setPixmap(LSIcons.right_svg)
        self.state = PromptState.CanBeConnected
        # self.setFixedSize(32, 32)


    def set_normal_style(self):
        self.state=PromptState.Normal
        # self.setFixedSize(_PromptLabelIcon.NormalFixedWidth, _PromptLabelIcon.NormalFixedHeight)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.state == PromptState.Normal:
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
            self.pen.setColor(self.color1)
            self.brush.setColor(self.color1)
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawRect(0, 0, _PromptLabelIcon.NormalFixedWidth, _PromptLabelIcon.TITLE_HEIGHT)
            self.pen.setColor(self.color2)
            self.brush.setColor(self.color2)
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawRect(0, _PromptLabelIcon.TITLE_HEIGHT, _PromptLabelIcon.NormalFixedWidth,
                             _PromptLabelIcon.NormalFixedHeight)
        else:
            super().paintEvent(event)


class LSPromptLabel(QFrame, LSObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self, *args, **kwargs)

    def init_attrs(self):
        super().init_attrs()

        self.icon = _PromptLabelIcon()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)

    def init_properties(self):
        super().init_properties()
        self.setObjectName("LSPromptLabel")
        self.set_normal_style()
        # self.main_layout.setSpacing(0)

    def init_ui(self):
        super().init_ui()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.icon)
        self.main_layout.addWidget(self.label)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def set_normal_style(self):
        self.icon.state = PromptState.Normal
        self.label.show()
        self.label.setText("放置一个新节点.")
        self.main_layout.setContentsMargins(12, 5, 5, 5)
        self.resize(100,25)


    def set_hover_pin_style(self, pin,sender_pin):
        connected_flag=pin.can_be_connected(sender_pin)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.hide()
        self.resize(25,25)
        self.show()
        if connected_flag==PinConnectionFlag.CanConnect:
            self.label.setText(f"")
            self.label.hide()
            self.icon.set_can_be_connected_style()
        elif connected_flag in {PinConnectionFlag.ReplaceExecConnect,
                                PinConnectionFlag.ReplaceDataConnect,
                                PinConnectionFlag.OnlyOneExecConnect}:
            self.label.setText(f"替换{pin.get_type()}节点")
            self.label.show()
            self.icon.set_can_be_connected_style()
        else:

            if connected_flag==PinConnectionFlag.PinTypeError:
                self.label.setText(f"{sender_pin._type}与{pin._type}不兼容.")

            elif connected_flag == PinConnectionFlag.AttrTypeError:
                self.label.setText(f"{sender_pin.attr_type}与{pin.attr_type}不兼容.")
            elif connected_flag == PinConnectionFlag.FlowError:
                self.label.setText("连接方向不匹配")
            elif connected_flag == PinConnectionFlag.IsSelfError:
                self.label.setText("不允许自己连自己啊")

            else:
                raise ValueError(f"你别管,就是不行,{connected_flag} 还没实现")


            self.label.show()
            self.icon.set_can_not_be_connected_style()


if __name__ == '__main__':
    app = QApplication()
    window = LSPromptLabel()
    window.show()
    app.exec_()
