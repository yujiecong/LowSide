
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyState
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Common.Func import OS
from Source.Widgets.PinIcon.LSPinIcon import LSPinIcon


qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDataPinIcon(LSPinIcon):
    FixedWidth = 18
    FixedHeight = 18

    ELLIPSE_PEN_WIDTH = 2
    _PenWidth = 1
    _TriangleWidth = 2

    _EllipseWidth = 4
    _EllipseHeight = 4

    _HalfWidth = FixedWidth / 2
    _HalfHeight = FixedHeight / 2

    TriangleStartX = 4
    TriangleEndX = TriangleStartX + _TriangleWidth
    EllipseStartX = 0
    EllipseEndX = EllipseStartX + _EllipseWidth

    RightLineStartPos = QPoint(TriangleStartX+_TriangleWidth, 0)
    LeftLineStartPos = QPoint(2, 0)

    def init_properties(self):
        super().init_properties()
        self.pen.setWidth(LSDataPinIcon._PenWidth)
        self.brush.setStyle(Qt.SolidPattern)
        # self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.setMinimumSize(LSDataPinIcon.FixedWidth, LSDataPinIcon.FixedHeight)

    def init_attrs(self):
        super().init_attrs()
        self.pen = QPen()
        self.brush = QBrush()
        self.state=PropertyState.Normal


        self.init_pixmap()

    def init_pixmap(self):
        self.ellipse_pixmap=None
        self.triangle_pixmap=None
        self.list_pixmap=None
        self.dict_pixmap=None


    def set_normal_style(self):
        self.state=PropertyState.Normal
        self.init_pixmap()
        self.repaint()

    def set_connected_style(self):
        self.init_pixmap()
        self.repaint()

    def set_disconnected_style(self):
        self.init_pixmap()
        self.repaint()

    def right_pos(self):
        offset=QPoint(self.width()//2,self.height()//2)
        return LSDataPinIcon.RightLineStartPos+offset

    def left_pos(self):
        offset=QPoint(0,self.height()//2)
        return LSDataPinIcon.LeftLineStartPos+offset


    def _prepare_ellipse_color(self):
        color=self.pin.current_color
        self.pen.setColor(color)
        if self.is_in_connected or self.is_out_connected:
            self.brush.setColor(color)
        else:
            self.brush.setColor(self.pin.internal_color)


    def _prepare_triangle_color(self):
        self.brush.setColor(self.pin.current_color)

    def _prepare_tuple_color(self):
        self.pen.setColor(self.pin.current_color)
        self.brush.setColor(self.pin.current_color)

    def _prepare_dict_color(self):
        self.pen.setColor(self.pin.current_color)
        self.brush.setColor(self.pin.current_color)


    def _draw_ellipse(self, painter):
        offset = QPoint(self.width() // 2, self.height() // 2)
        self.pen.setWidth(self.ELLIPSE_PEN_WIDTH)
        self._prepare_ellipse_color()
        painter.setBrush(self.brush)
        painter.setPen(self.pen)

        center = QPoint(- self._TriangleWidth + self.EllipseStartX, 0) + offset
        painter.drawEllipse(center, self._EllipseWidth, self._EllipseHeight)

        # if self.ellipse_pixmap is None:
        #
        #     self.ellipse_pixmap=QPixmap(self.width(),self.height())
        #     self.ellipse_pixmap.fill(Qt.transparent)
        #     pixmap_painter=QPainter(self.ellipse_pixmap)
        #
        #     offset=QPoint(self.width()//2,self.height()//2)
        #
        #     self.pen.setWidth(4)
        #     self._prepare_ellipse_color()
        #     pixmap_painter.setBrush(self.brush)
        #     pixmap_painter.setPen(self.pen)
        #
        #     center = QPoint(- self._TriangleWidth+self.EllipseStartX, 0)+offset
        #     pixmap_painter.drawEllipse(center, self._EllipseWidth, self._EllipseHeight)
        #     pixmap_painter.end()
        # painter.drawPixmap(0,0,self.ellipse_pixmap)




    def _draw_triangle(self, painter):
        offset = QPoint(self.width() // 2, self.height() // 2)
        triangle = QPolygon(
            [QPoint(LSDataPinIcon.TriangleStartX, LSDataPinIcon._TriangleWidth) + offset,
             QPoint(LSDataPinIcon.TriangleStartX, - LSDataPinIcon._TriangleWidth) + offset,
             LSDataPinIcon.RightLineStartPos + offset])
        self.pen.setWidth(1)
        self._prepare_triangle_color()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(triangle)

        # if self.triangle_pixmap is None:
        #     self.triangle_pixmap = QPixmap(self.width(), self.height())
        #     self.triangle_pixmap.fill(Qt.transparent)
        #     pixmap_painter=QPainter(self.triangle_pixmap)
        #
        #     offset=QPoint(self.width()//2,self.height()//2)
        #     triangle = QPolygon(
        #         [QPoint(LSDataPinIcon.TriangleStartX, LSDataPinIcon._TriangleWidth)+offset,
        #          QPoint(LSDataPinIcon.TriangleStartX, - LSDataPinIcon._TriangleWidth)+offset,
        #          LSDataPinIcon.RightLineStartPos+offset])
        #     self.pen.setWidth(1)
        #     self._prepare_triangle_color()
        #     pixmap_painter.setPen(self.pen)
        #     pixmap_painter.setBrush(self.brush)
        #     pixmap_painter.drawPolygon(triangle)
        # painter.drawPixmap(0,0,self.triangle_pixmap)

    def _draw_list(self, painter:QPainter):

        self._prepare_tuple_color()
        self.pen.setWidth(1)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        gap = 2.5

        side_length = LSDataPinIcon.FixedWidth/4-2.5
        rect = QRect(0 ,0, LSDataPinIcon.FixedWidth, LSDataPinIcon.FixedHeight)  # 宽度为40的矩形
        rects=[]
        for i in range(3):
            for j in range(3):
                if i==1 and j ==1:
                    continue
                x = rect.left() + gap * (i + 1) + side_length * i+1
                y = rect.top() + gap * (j + 1) + side_length * j +1
                square_rect = QRectF(x, y, side_length, side_length)
                rects.append(square_rect)
        painter.drawRects(rects)


        # if self.list_pixmap is None:
        #     self.list_pixmap = QPixmap(self.width(), self.height())
        #     self.list_pixmap.fill(Qt.transparent)
        #     pixmap_painter=QPainter(self.list_pixmap)
        #
        #     self._prepare_tuple_color()
        #     self.pen.setWidth(1)
        #     pixmap_painter.setPen(self.pen)
        #     pixmap_painter.setBrush(self.brush)
        #     gap = 3
        #     side_length = LSDataPinIcon.FixedWidth//4 - 3
        #     rect = QRect(0 ,0, LSDataPinIcon.FixedWidth, LSDataPinIcon.FixedHeight)  # 宽度为40的矩形
        #     rects=[]
        #     for i in range(3):
        #         for j in range(3):
        #             if i==1 and j ==1:
        #                 continue
        #             x = rect.left() + gap * (i + 1) + side_length * i+1
        #             y = rect.top() + gap * (j + 1) + side_length * j+3
        #             square_rect = QRect(x, y, side_length, side_length)
        #             rects.append(square_rect)
        #     pixmap_painter.drawRects(rects)
        # painter.drawPixmap(0,0,self.list_pixmap)
    def _draw_dict(self, painter: QPainter):
        self._prepare_dict_color()
        self.pen.setWidth(1)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        gap = 2.5

        side_length = LSDataPinIcon.FixedWidth / 4 - 2.5
        rect = QRect(0, 0, LSDataPinIcon.FixedWidth, LSDataPinIcon.FixedHeight)  # 宽度为40的矩形
        draw_rects=[]
        for i in range(3):
            x = rect.left() + gap+1
            y = rect.top() + gap * (i + 1) + side_length * i +1

            square_rect1 = QRectF(x, y, side_length, side_length)

            x2 = x + side_length + gap
            square_rect2 = QRectF(x2, y, LSDataPinIcon.FixedWidth-side_length-gap-7,side_length, )
            draw_rects.append(square_rect1)
            draw_rects.append(square_rect2)

        painter.drawRects(draw_rects)

        # if self.dict_pixmap is None:
        #     self.dict_pixmap = QPixmap(self.width(), self.height())
        #     self.dict_pixmap.fill(Qt.transparent)
        #     pixmap_painter = QPainter(self.dict_pixmap)
        #
        #     self._prepare_dict_color()
        #     self.pen.setWidth(1)
        #     pixmap_painter.setPen(self.pen)
        #     pixmap_painter.setBrush(self.brush)
        #     gap = 3
        #
        #     side_length = LSDataPinIcon.FixedWidth // 4 - 3
        #     rect = QRect(0, 0, LSDataPinIcon.FixedWidth, LSDataPinIcon.FixedHeight)  # 宽度为40的矩形
        #     draw_rects=[]
        #     for i in range(3):
        #         x = rect.left() + gap+1
        #         y = rect.top() + gap * (i + 1) + side_length * i +3
        #
        #         square_rect1 = QRect(x, y, side_length, side_length)
        #
        #         x2 = x + side_length + gap
        #         square_rect2 = QRect(x2, y, LSDataPinIcon.FixedWidth-side_length-gap-9,side_length, )
        #         draw_rects.append(square_rect1)
        #         draw_rects.append(square_rect2)
        #
        #     pixmap_painter.drawRects(draw_rects)
        # painter.drawPixmap(0, 0, self.dict_pixmap)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing,True)

        if self.attr_type == LSPinAttrType.list:
            self._draw_list(painter)
        elif self.attr_type == LSPinAttrType.dict:
            self._draw_dict(painter)
        else:
            self._draw_ellipse(painter)
            self._draw_triangle(painter)

        painter.end()

    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.setCursor(Qt.CrossCursor)




if __name__ == '__main__':
    app=QApplication()
    w=QWidget()
    lay=QVBoxLayout(w)
    window=LSDataPinIcon(QColor(1,160,230),QColor(Qt.black))
    # window=QLabel("asd")
    print(window.size())
    lay.addWidget(window)

    w.show()
    app.exec_()
