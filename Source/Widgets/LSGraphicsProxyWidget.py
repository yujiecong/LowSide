from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import *

from Source.Common.Enums import ItemZValue
from Source.Custom.LSObject import LSObject


class LSGraphicsProxyWidget(QGraphicsProxyWidget, LSObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self, *args, **kwargs)
        # self.setCacheMode(QGraphicsItem.CacheMode.NoCache)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()
        self.setZValue(ItemZValue.CoreNode)

    def init_ui(self):
        super().init_ui()

    def init_connection(self):
        super().init_connection()

    # def paint(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget:QWidget) -> None:
    #     painter.setClipRect( option.exposedRect)
    #     super().paint(painter, option, widget)

    # def boundingRect(self) -> QRectF:
    #     size = self.size()
    #     return QRectF(0, 0, size.width(), size.height())



if __name__ == '__main__':
    app = QApplication()
    window = LSGraphicsProxyWidget()
    window.show()
    app.exec_()
