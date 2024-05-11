from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyState
from Source.Custom.LSColor import LSColor
from Source.Common.Func import OS
from Source.Widgets.PinIcon.LSDataPinIcon import LSDataPinIcon
from Source.Widgets.PinIconWidget.LSPinIconWidget import LSPinIconWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()



class LSDataPinWidget(LSPinIconWidget):

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

        # self.setFixedSize(_DataIcon.FixedWidth, _DataIcon.FixedHeight)

    def init_ui(self):
        super().init_ui()
        self.init_icon()
        # self.lay.setContentsMargins()

    def init_icon(self):
        self.icon = LSDataPinIcon(self.pin, self.attr_type)
        self.main_layout.addWidget(self.icon)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)
        # self.setStyleSheet("background-color:green;")

    def init_connection(self):
        super().init_connection()


    def set_connected_style(self):
        self.icon.set_connected_style()

    def set_disconnected_style(self):
        self.icon.set_disconnected_style()

    def set_normal_style(self):
        self.state=PropertyState.Normal
        self.repaint()

    def set_hover_style(self):
        self.state=PropertyState.Hover
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.state == PropertyState.Hover:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
            hover_color = QLinearGradient(0, 0, self.width(), 0)
            hover_color.setColorAt(0, LSColor.Black)
            pos = (self.width()) / self.width()
            hover_color.setColorAt(pos, self.pin.current_color)
            hover_color.setColorAt(1, LSColor.Black)
            self.brush = QBrush(hover_color)
            painter.begin(self)
            painter.setBrush(self.brush)
            painter.drawRect(self.rect())
            painter.end()



if __name__ == '__main__':
    app = QApplication()

    window = LSDataPinWidget(QColor(1, 160, 230), QColor(Qt.black))
    window.show()
    app.exec_()
