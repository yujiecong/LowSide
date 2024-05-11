
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSColor import PinAttrTypeExternalColor
from Source.Custom.LSObject import LSObject


class LSAttrTypeIcon(QIcon):
    def __init__(self, attr_type):
        color = PinAttrTypeExternalColor(attr_type)
        width = 26
        pixmap = QPixmap(width, 32)  # 创建一个64x64的空白Pixmap
        pixmap.fill(Qt.transparent)  # 填充为透明背景
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿
        painter.setBrush(color)  # 设置画刷颜色为蓝色
        painter.setPen(Qt.NoPen)  # 设置无边框
        # 绘制一个蓝色的圆形
        painter.drawRoundedRect(0, 10, width, 13, 3, 3)
        painter.end()

        super().__init__(pixmap)

if __name__ == '__main__':
    app=QApplication()
    window=LSAttrTypeIcon()
    window.show()
    app.exec_()
