import ast

from PySide2.QtCore import QTimer
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Source import Globs
from Source.Common import Func
from Source.Common.Enums import PropertyState
from Source.Custom.Enums.LSPinEnum import PinType, PinFlow
from Source.Common.Func import OS
from Source.Widgets.Pin.LSPinLineEdit import LSPinLineEdit
from Source.Widgets.PinIconWidget.LSDataPinIconWidget import LSDataPinWidget
from Source.Widgets.Pin.LSFlowPin import LSFlowPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSDataPin(LSFlowPin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_attrs(self):
        super().init_attrs()
        self.state = PropertyState.Normal
        self._type = PinType.Data

    def init_properties(self):
        super().init_properties()
        "这句话会导致hover效果失效 因为缩短了...草"
        # self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_ui(self):
        super().init_ui()
        if self.get_flow() == PinFlow.In:
            pass
        else:
            self.pin_icon.main_layout.setContentsMargins(0, 0, 2, 0)

    def init_connection(self):
        super().init_connection()
        self.doubleClicked_signal.connect(self.on_double_clicked)



    def get_flow(self) -> PinFlow:
        return self.flow

    def get_type(self) -> PinType:
        return PinType.Data

    @property
    def pin_icon(self) -> LSDataPinWidget:
        return self._pin_icon

    @property
    def pin_icon_type(self):
        return LSDataPinWidget

    def set_state(self, state: PropertyState):
        self.state = state
        self.repaint()

    def set_hover_style(self):
        self.state = PropertyState.Hover
        self.repaint()

    def set_normal_style(self):
        self.state = PropertyState.Normal
        self.repaint()

    def get_value(self):
        raise NotImplementedError(f"{self}")

    def on_double_clicked(self):
        "将自己的label变成lineedit"
        self.new_title_label=LSPinLineEdit(self.title)
        self.new_title_label.setFixedWidth(self.title_label.width())
        self.origin_title_label=self.title_label
        "全选内容"
        "移动光标到最后"

        self.pin_layout.replaceWidget(self.origin_title_label,self.new_title_label)
        self.new_title_label.editingFinished.connect(self.rename_finished)

    def rename_finished(self):
        text = self.sender().text()
        self.set_title(text)
        self.pin_layout.replaceWidget(self.new_title_label,self.origin_title_label)
        self.new_title_label.deleteLater()
        if self.node:
            QTimer.singleShot(10,self.node.update_pins)


    def to_ast(self):
        return ast.Name(id=self.title, ctx=ast.Load())


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        painter.begin(self)
        painter.setPen(Qt.NoPen)

        if self.is_enabled:
            if self.state == PropertyState.Hover:
                hover_color = QLinearGradient(0, 0, self.width(), 0)
                hover_color.setColorAt(0, Func.lighten_color(self.current_color,0.3))
                # pos = (self.pin_icon.width()) / self.width()
                # hover_color.setColorAt(pos, self.current_color)
                hover_color.setColorAt(1,self.current_color.darker(300))
                self.brush = QBrush(hover_color)
                painter.setBrush(self.brush)
                painter.drawRect(self.rect())
        else:
            self.brush = QBrush(Func.lighten_color(self.disabled_color, 0.5))
            painter.setBrush(self.brush)
            painter.drawRect(self.rect())

        painter.end()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if event.button() == Qt.RightButton:
            self.is_double_clicked = True
        event.accept()


if __name__ == '__main__':
    app = QApplication()
    window = LSDataPin()
    window.resize(60, 40)
    window.show()
    app.exec_()
