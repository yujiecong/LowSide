
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.LSGraphicsView import LSGraphicsView
from Source.Widgets.LSTabWidget import LSTabWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSMainWindow(QMainWindow,LSObject):
    def __init__(self,main_ui,*args,**kwargs):
        self.main_ui=main_ui
        super().__init__(*args,**kwargs)
        LSObject.__init__(self)
        self.setParent(self.main_ui)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()
        self.setWindowFlags(Qt.WindowType.Widget)
        self.setDockOptions(
            QMainWindow.AnimatedDocks |
            QMainWindow.AllowNestedDocks)
        
    def init_ui(self):
        super().init_ui()
        self.tab_widget=LSTabWidget()
        self.tab_dock = QDockWidget(self)
        self.tab_dock.setWidget(self.tab_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tab_dock)
        "如果只有一个dock 会崩溃"
        self.variable_dock = QDockWidget(self)
        # self.variable_dock.titleBarWidget().hide()
        self.variable_dock.setWidget(None)
        self.addDockWidget(Qt.RightDockWidgetArea, self.variable_dock)




    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()
        pass
if __name__ == '__main__':
    app=QApplication()
    window=LSMainWindow(None)
    window.show()
    app.exec_()
