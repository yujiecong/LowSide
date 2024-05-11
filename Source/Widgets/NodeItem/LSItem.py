import uuid
from typing import *

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from Source.Common.Enums import PropertyName, PropertyState
from Source.Common.Func import OS
from Source.Common.Util import Util
from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSItem(QFrame, LSObject):
    LMouseButtonIsPressed: bool = False

    def __init__(self, uuid_=None):
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.uuid_ = str(uuid_ or uuid.uuid4())

        super().__init__()
        LSObject.__init__(self)


    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()
        self.setFocusPolicy(Qt.ClickFocus)

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()


    @property
    def proxy(self) -> QGraphicsProxyWidget:
        return self.graphicsProxyWidget()

    def set_selected(self, f):
        if f:
            self.setProperty(PropertyName.State, PropertyState.Selected)
        else:
            self.setProperty(PropertyName.State, PropertyState.Normal)

        Util.repolish(self)

    def is_selected(self):
        return self.property(PropertyName.State) == PropertyState.Selected

    def duplicate(self) -> "LSItem":
        raise NotImplementedError



    def mousePressEvent(self, event: QMouseEvent) -> None:
        """

        :param event:
        :return:
        """
        # 这个super的位置也不能动. 不然会导致move不了
        super().mousePressEvent(event)

        "如果没有这个 会继续传递给scene导致移动不了.."
        event.accept()

    def __repr__(self):
        return f"{self.__class__.__qualname__} pos={self.pos().toTuple()}"


if __name__ == '__main__':
    app = QApplication()
    window = LSItem()
    window.show()
    app.exec_()
