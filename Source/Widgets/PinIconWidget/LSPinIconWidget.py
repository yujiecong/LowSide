from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyState
from Source.Common.Func import OS

from Source.Widgets.PinIcon.LSPinIcon import LSPinIcon
from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSPinIconWidget(QFrame,LSObject):
    mousePressed=Signal(object)
    mouseMoved=Signal(object)
    mouseReleased=Signal(object)
    LMouseIsPressed: bool = False


    def __init__(self, pin, attr_type, *args, **kwargs):
        self.pin=pin
        self.attr_type=attr_type
        super().__init__(*args, **kwargs)
        LSObject.__init__(self,*args, **kwargs)

    def init_attrs(self):
        super().init_attrs()
        self.state = PropertyState.Normal
        self.is_in_connected=False
        self.is_out_connected=False
        self.icon:LSPinIcon=None

    def init_properties(self):
        super().init_properties()
        self.setMouseTracking(True)


    def init_ui(self):
        super().init_ui()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(1)

        # self.setLayout(self.main_layout)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)


    def init_connection(self):
        super().init_connection()



    def set_disconnected_style(self):
        raise NotImplementedError

    def set_connected_style(self):
        raise NotImplementedError

    def set_normal_style(self):
        raise NotImplementedError

    def set_hover_style(self):
        raise NotImplementedError


    # def mousePressEvent(self, event:QMouseEvent) -> None:
    #     # super().mousePressEvent(event)
    #     event.accept()
    #     LSPinIconWidget.LMouseIsPressed=True
    #     self.mousePressed.emit(event)
    #
    # def mouseMoveEvent(self, event:QMouseEvent):
    #     # super().mouseMoveEvent(event)
    #     event.accept()
    #     self.mouseMoved.emit(event)
    #
    #
    # def mouseReleaseEvent(self, event:QMouseEvent) -> None:
    #     # super().mouseReleaseEvent(event)
    #     LSPinIconWidget.LMouseIsPressed=False
    #     self.mouseReleased.emit(event)
    #




if __name__ == '__main__':
    app = QApplication()
    window = LSPinIcon()
    window.show()
    app.exec_()
