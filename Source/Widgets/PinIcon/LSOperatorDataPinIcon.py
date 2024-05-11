
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.PinIcon.LSDataPinIcon import LSDataPinIcon

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSOperatorDataPinIcon(LSDataPinIcon):

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing,True)
        self._draw_ellipse(painter)
        painter.end()
if __name__ == '__main__':
    app=QApplication()
    window=LSOperatorDataPinIcon()
    window.show()
    app.exec_()
