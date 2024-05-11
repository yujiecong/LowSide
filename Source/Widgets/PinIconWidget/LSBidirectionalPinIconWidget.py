
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyState
from Source.Common.Func import OS
from Source.Widgets.PinIconWidget.LSPinIconWidget import LSPinIconWidget
from Source.Widgets.PinIcon.LSBidirectionalPinIcon import LSBidirectionalPinIcon

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSBidirectionalPinWidget(LSPinIconWidget):

    def init_attrs(self):
        super().init_attrs()
        self.icon = LSBidirectionalPinIcon(self.pin, self.attr_type)
        self.state = PropertyState.Normal

        
    def init_properties(self):
        super().init_properties()
        self.icon.setMinimumSize(self.icon.FixedWidth,self.icon.FixedHeight*4/5+2)

        
    def init_ui(self):
        super().init_ui()
        self.main_layout.addWidget(self.icon)
        self.main_layout.setContentsMargins(0,0,0,0)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
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
            transparency=166
            if self.is_in_connected or self.is_out_connected:
                hover_color1 = QColor(130, 130, 130,transparency)
                hover_color2 = QColor(222, 222, 222,transparency)
                hover_color3 = QColor(130, 130, 130,transparency)
            else:
                hover_color1 = QColor(58, 57, 57,transparency)
                hover_color2 = QColor(100, 100, 100,transparency)
                hover_color3 = QColor(47, 47, 47,transparency)

            hover_color.setColorAt(0, hover_color1)
            hover_color.setColorAt(0.5,
                                   hover_color2)
            hover_color.setColorAt(1, hover_color3)
            painter.begin(self)
            painter.setPen(QPen(Qt.transparent))
            painter.setBrush(QBrush(hover_color))
            painter.drawRect(self.rect())
            painter.end()
        else:
            super().paintEvent(event)


if __name__ == '__main__':
    app=QApplication()
    window=LSBidirectionalPinWidget()
    window.show()
    app.exec_()
