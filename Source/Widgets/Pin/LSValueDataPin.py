
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.Pin.LSDataPin import LSDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSValueDataPin(LSDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        
    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.value_widget=QWidget()
        self.value_layout=QHBoxLayout()
        self.value_widget.setLayout(self.value_layout)
        self.value_layout.setContentsMargins(0, 0, 0, 0)

        self.pin_layout.addWidget(self.value_widget,1,1,1,1)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def connect_finished(self):
        super().connect_finished()
        if self.is_in_connected:
            self.value_widget.hide()
        else:
            self.value_widget.show()

        self.pin_layout.addWidget(self._pin_icon,0,0)

    def disconnect_finished(self):
        super().disconnect_finished()
        if self.is_in_connected:
            self.value_widget.hide()
        else:
            self.value_widget.show()

        self.pin_layout.addWidget(self._pin_icon,0,0,2,1)



    def update_item(self):
        self.node.graphicsProxyWidget().update()
        self.node.update_pins()
        super().update_item()


if __name__ == '__main__':
    app=QApplication()
    window=LSValueDataPin(flow="In")
    window.show()
    app.exec_()
