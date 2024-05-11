from PySide2.QtCore import Qt
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Source.Common.Enums import ItemZValue
from Source.Common.Util import Util
from Source.Widgets.LSGraphicsViewBackgroundPixmap import LSGraphicsViewBackgroundPixmap, \
    LSGraphicsViewBackgroundBigPixmap


class LSGraphicsBackgroundPixmapItem(QGraphicsPixmapItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.custom_pixmap = LSGraphicsViewBackgroundBigPixmap()
        self.setZValue(ItemZValue.Background)
        # self.setFlag(QGraphicsItem.ItemIgnoresTransformations,True)
        self.setTransformationMode(Qt.SmoothTransformation)
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        # self.setCacheMode(QGraphicsItem.CacheMode.ItemCoordinateCache)
        self.update_pixmap()

    def update_pixmap(self):
        # pix = LSGraphicsViewBackgroundPixmap()
        pix = LSGraphicsViewBackgroundPixmap()
        # pix = LSGraphicsViewBackgroundPixmap(LSGraphicsViewBackgroundPixmap.Width,LSGraphicsViewBackgroundPixmap.Height)
        self.custom_item=pix.scaled(
            LSGraphicsViewBackgroundPixmap.Width,
            LSGraphicsViewBackgroundPixmap.Height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(self.custom_item)
        # self.setPixmap(pix)


    # def paint(self, painter:QPainter, option, widget):
    #     scaleFactor = 1.0 / painter.matrix().m11()
    #     painter.scale(scaleFactor, scaleFactor)
    #     super().paint(painter, option, widget)

if __name__ == '__main__':
    app=QApplication()
    window=LSGraphicsBackgroundPixmapItem()
    window.show()
    app.exec_()
