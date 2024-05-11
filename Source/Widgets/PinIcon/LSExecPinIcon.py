
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Func import OS
from Source.Widgets.PinIcon.LSPinIcon import LSPinIcon

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSExecPinIcon(LSPinIcon):
    FixedWidth = 16
    FixedHeight = 16
    _PolygonOffsetX = 3
    _PolygonOffsetY = 4

    _PolygonWidth = 6
    _PolygonHeight = 12

    RightLineStartPos = QPoint(_PolygonHeight + _PolygonOffsetX-1, _PolygonWidth + _PolygonOffsetY)
    LeftLineStartPos = QPoint(0, _PolygonWidth + _PolygonOffsetY)

    PenWidth=1


    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)



    def init_properties(self):
        super().init_properties()
        self.setFixedSize(20, 20)

        self.pen.setWidth(LSExecPinIcon.PenWidth)
        self.pen.setColor(self.pin.current_color)
        self.brush.setColor(self.pin.internal_color)
        self.brush.setStyle(Qt.SolidPattern)



    def init_attrs(self):
        super().init_attrs()
        self.pen = QPen()
        self.brush = QBrush()



    def set_connected_style(self):
        self.brush.setColor(self.pin.current_color)
        self.pen.setColor(QColor(175,175,175))
        self.repaint()

    def set_normal_style(self):
        self.brush.setColor(self.pin.internal_color)
        self.pen.setColor(self.pin.current_color)
        self.repaint()

    def right_pos(self):
        return LSExecPinIcon.RightLineStartPos

    def left_pos(self):
        return LSExecPinIcon.LeftLineStartPos

    def paintEvent(self, event: QPaintEvent) -> None:
        # pixmap=QPixmap(32,32)
        # pixmap.fill(Qt.transparent)
        # painter = QPainter(pixmap)
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        "需要让起点平移到对应位置"

        painter.drawPolygon([
            QPoint(LSExecPinIcon._PolygonOffsetX, LSExecPinIcon._PolygonOffsetY),
            QPoint(LSExecPinIcon._PolygonWidth + LSExecPinIcon._PolygonOffsetX-1, LSExecPinIcon._PolygonOffsetY),
            LSExecPinIcon.RightLineStartPos,
            QPoint(LSExecPinIcon._PolygonWidth + LSExecPinIcon._PolygonOffsetX-1,
                    LSExecPinIcon._PolygonHeight + LSExecPinIcon._PolygonOffsetY),
            QPoint(LSExecPinIcon._PolygonOffsetX, LSExecPinIcon._PolygonHeight + LSExecPinIcon._PolygonOffsetY),
        ])

        painter.end()
        # pixmap.save(r"C:\repo\_USDQ\LowSide\Assets\exec_pin.png")



    def enterEvent(self, event: QEvent):
        super().enterEvent(event)

        self.setCursor(Qt.CrossCursor)

if __name__ == '__main__':
    app=QApplication()
    window=LSExecPinIcon()
    window.show()
    app.exec_()
