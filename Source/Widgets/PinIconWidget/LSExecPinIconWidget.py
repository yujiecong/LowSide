from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import PropertyName, PropertyState
from Source.Common.Func import OS
from Source.Common.Util import Util
from Source.Widgets.PinIcon.LSExecPinIcon import LSExecPinIcon
from Source.Widgets.PinIconWidget.LSPinIconWidget import LSPinIconWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()




class LSExecPinWidget(LSPinIconWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        "要将icon的坐标变换到当前的坐标系"

    def init_attrs(self):
        super().init_attrs()

    def init_ui(self):
        super().init_ui()

        self.icon = LSExecPinIcon(self.pin, self.attr_type)
        self.main_layout.addWidget(self.icon)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def init_properties(self):
        super().init_properties()

    def set_connected_style(self):
        self.icon.set_connected_style()

    def set_hover_style(self):
        self.setProperty(PropertyName.State, PropertyState.Hover)
        Util.repolish(self)
        self.setCursor(Qt.ArrowCursor)

    def set_normal_style(self):
        self.setProperty(PropertyName.State, PropertyState.Normal)
        Util.repolish(self)

    def set_disconnected_style(self):
        self.icon.set_normal_style()


    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.set_hover_style()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.set_normal_style()




if __name__ == '__main__':
    app = QApplication()
    window = LSExecPinWidget()
    window.setStyleSheet("background-color:black;")
    window.show()
    app.exec_()
