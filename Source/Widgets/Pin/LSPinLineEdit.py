
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject


qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSPinLineEdit(QLineEdit,LSObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.textChanged.connect(self.adjustSize)
        # self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def init_attrs(self):
        super().init_attrs()
    def init_properties(self):
        super().init_properties()

        # self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def adjustSize(self):
        if len(self.text())<16:
            width = self.fontMetrics().width(self.text())
            self.setMinimumWidth(width + 10)  # 加上一些额外的空间
        else:
            super().adjustSize()

        # self.setFocus()
        # print(cursor_pos)
        # self.setCursorPosition(cursor_pos)


    def mousePressEvent(self, arg__1):
        super().mousePressEvent(arg__1)
        arg__1.accept()

    def mouseMoveEvent(self, arg__1):
        super().mouseMoveEvent(arg__1)
        arg__1.accept()


    def mouseReleaseEvent(self, arg__1):
        super().mouseReleaseEvent(arg__1)
        arg__1.accept()
    def mouseDoubleClickEvent(self, arg__1):
        super().mouseDoubleClickEvent(arg__1)
        arg__1.accept()

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()


    def keyPressEvent(self, arg__1):
        super().keyPressEvent(arg__1)
        arg__1.accept()

    def focusOutEvent(self, arg__1):
        super().focusOutEvent(arg__1)
        self.editingFinished.emit()




if __name__ == '__main__':
    app=QApplication()
    window=LSPinLineEdit()
    window.show()
    app.exec_()
