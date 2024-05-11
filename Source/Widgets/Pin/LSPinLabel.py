
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject


qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSPinLabel(QLabel,LSObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        LSObject.__init__(self)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setEnabled(False)

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    # def mousePressEvent(self, ev:QMouseEvent):
    #     ev.ignore()
    #     pass
    # def mouseMoveEvent(self, ev:QMouseEvent):
    #     ev.ignore()

if __name__ == '__main__':
    app=QApplication()
    window=LSPinLabel()
    window.show()
    app.exec_()
