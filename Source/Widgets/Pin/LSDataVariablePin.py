
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common import Func
from Source.Common.Enums import PropertyState
from Source.Common.Func import OS
from Source.Widgets.Pin.LSDataPin import LSDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDataVariablePin(LSDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_body(self):
        super().init_body()
        self.pin_layout.setContentsMargins(10,0,0,0)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()


    def paintEvent(self, event: QPaintEvent) -> None:
        if self.state == PropertyState.Hover:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
            color = Func.lighten_color(self.current_color, 0.5)
            color.setAlpha(155)
            self.brush = QBrush(color)
            painter.begin(self)
            painter.setBrush(self.brush)
            painter.setPen(Qt.transparent)
            painter.drawRect(self.rect())
            painter.end()

if __name__ == '__main__':
    app=QApplication()
    window=LSDataVariablePin()
    window.show()
    app.exec_()
