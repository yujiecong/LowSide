from PySide2.QtCore import QPoint
from PySide2.QtWidgets import *
from Source import Globs
from Source.Common.Func import OS

from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()

class LSPinIcon(QFrame, LSObject):

    def __init__(self, pin, attr_type):
        self.pin=pin
        self.attr_type=attr_type

        super().__init__()
        LSObject.__init__(self)

    def init_attrs(self):
        super().init_attrs()
        self.is_in_connected=False
        self.is_out_connected=False

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()


    def init_style(self):
        super().init_style()
        self.setStyleSheet(qss)

    def init_connection(self):
        super().init_connection()

    def right_pos(self) -> QPoint:
        raise NotImplementedError
    def left_pos(self) -> QPoint:
        raise NotImplementedError



if __name__ == '__main__':
    app = QApplication()
    window = LSPinIcon()
    window.show()
    window.resize(500, 500)
    app.exec_()
