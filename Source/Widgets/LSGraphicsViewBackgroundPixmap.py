from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Custom.LSColor import LSColor


class LSGraphicsViewBackgroundPixmap(QPixmap):
    DefaultWidth = 100
    DefaultHeight = 100
    Width = 100
    Height = 100
    PenWidth = 1

    def __init__(self, w=DefaultWidth, h=DefaultHeight, *args, **kwargs):
        # super().__init__(LSGraphicsViewBackgroundPixmap.DefaultWidth,LSGraphicsViewBackgroundPixmap.DefaultHeight,*args,**kwargs)
        super().__init__(w, h, *args, **kwargs)

        self.count = 8
        self.bg_color = QColor(38, 38, 38)
        self.pen = QPen(QColor(73, 73, 73))
        self.pen.setWidth(LSGraphicsViewBackgroundPixmap.PenWidth)  # 设置线宽度
        self.pen.setStyle(Qt.SolidLine)
        # self.pen.setCosmetic(True)

        self.fill(self.bg_color)
        self.pen.setWidthF(0.2)

        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing,False)
        painter.setPen(self.pen)

        x_interval = w / self.count
        y_interval = h / self.count

        lines = []

        for i in range(1, self.count):
            lines.append(QLine(0, i * y_interval, w, i * y_interval))
            lines.append(QLine(i * x_interval, 0, i * x_interval, h))
        painter.drawLines(lines)

        self.pen.setColor(QColor(12,12,12))
        painter.setPen(self.pen)
        painter.setBrush(QBrush(Qt.transparent))

        rect_lines=[
            QLine(0,0,w,0),
            QLine(0,0,0,h),
        ]

        painter.drawLines(rect_lines)
        # painter.drawRect(self.rect())
        painter.end()


class LSGraphicsViewBackgroundBigPixmap(QPixmap):
    Square = 3600
    EverSingle = 200
    PenWidth = 2
    XOffset = 0
    YOffset = 0

    def __init__(self, *args, **kwargs):
        # super().__init__(LSGraphicsViewBackgroundPixmap.DefaultWidth,LSGraphicsViewBackgroundPixmap.DefaultHeight,*args,**kwargs)
        super().__init__(LSGraphicsViewBackgroundBigPixmap.Square, LSGraphicsViewBackgroundBigPixmap.Square, *args,
                         **kwargs)

        bg_color = QColor(38, 38, 38)
        pen = QPen(QColor(53, 53, 53))
        pen.setWidth(LSGraphicsViewBackgroundPixmap.PenWidth)  # 设置线宽度
        pen.setStyle(Qt.SolidLine)

        self.fill(bg_color)

        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)
        tile_interval = LSGraphicsViewBackgroundBigPixmap.EverSingle
        tile_count = LSGraphicsViewBackgroundBigPixmap.Square // tile_interval

        line_interval = tile_interval / 8

        lines = []
        rects = []

        x_symbol = 1 if LSGraphicsViewBackgroundBigPixmap.XOffset >= 0 else -1
        y_symbol = 1 if LSGraphicsViewBackgroundBigPixmap.YOffset >= 0 else -1
        y_mod = abs(LSGraphicsViewBackgroundBigPixmap.YOffset) % LSGraphicsViewBackgroundBigPixmap.Square
        x_mod = abs(LSGraphicsViewBackgroundBigPixmap.XOffset) % LSGraphicsViewBackgroundBigPixmap.Square

        y_signed = y_symbol * y_mod
        x_signed = x_symbol * x_mod


        total_count = tile_count * tile_count
        square_with_interval=LSGraphicsViewBackgroundBigPixmap.Square+tile_interval

        for idx in range(total_count*8):

            ever_interval = idx * line_interval
            line1_y = ever_interval + y_signed
            line2_x = ever_interval + x_signed

            if line1_y > LSGraphicsViewBackgroundBigPixmap.Square:
                line1_y -= LSGraphicsViewBackgroundBigPixmap.Square
            elif line1_y < 0:
                line1_y += LSGraphicsViewBackgroundBigPixmap.Square

            if line2_x > LSGraphicsViewBackgroundBigPixmap.Square:
                line2_x -= LSGraphicsViewBackgroundBigPixmap.Square
            elif line2_x < 0:
                line2_x += LSGraphicsViewBackgroundBigPixmap.Square


            line = QLine(0,
                         line1_y,
                         LSGraphicsViewBackgroundBigPixmap.Square,
                         line1_y)
            line2 = QLine(line2_x,
                          0,
                          line2_x,
                          LSGraphicsViewBackgroundBigPixmap.Square)
            # rect=QRect(0,
            #            line1_y,
            #            LSGraphicsViewBackgroundBigPixmap.Square,
            #            line1_y+line_interval)
            # rect2=QRect(line2_x,
            #               0,
            #               line2_x+line_interval,
            #               LSGraphicsViewBackgroundBigPixmap.Square)
            #
            # rects.append(rect)
            # rects.append(rect2)
            lines.append(line)
            lines.append(line2)

        row_count=tile_count+1
        col_count=tile_count+1
        for row in range(row_count):
            for col in range(col_count):
                rect_p1_y = row * tile_interval + y_signed
                rect_p1_x = col * tile_interval + x_signed

                if rect_p1_y > LSGraphicsViewBackgroundBigPixmap.Square:
                    rect_p1_y -= square_with_interval
                elif rect_p1_y < -tile_interval:
                    rect_p1_y += square_with_interval

                if rect_p1_x > LSGraphicsViewBackgroundBigPixmap.Square:
                    rect_p1_x -= square_with_interval
                elif rect_p1_x < -tile_interval:
                    rect_p1_x += square_with_interval

                p1 = QPoint(rect_p1_x, rect_p1_y)
                p2 = p1 + QPoint(tile_interval, tile_interval)
                rect = QRect(p1, p2)
                rects.append(rect)


        painter.drawLines(lines)

        painter.setPen(pen)
        painter.drawRects(rects)

        painter.end()


if __name__ == '__main__':
    app = QApplication()
    # window=LSGraphicsViewBackgroundPixmap()
    window = LSGraphicsViewBackgroundBigPixmap()
    window.show()
    app.exec_()
