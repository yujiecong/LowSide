from PySide2.QtCore import Signal, QEvent, Qt
from PySide2.QtGui import QCursor, QMouseEvent

from Source import Globs
from PySide2.QtWidgets import *

from Source.Common import Func
from Source.Common.Func import OS
from Source.Common.Obj import LSDictWrapper
from Source.Common.Util import Util
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Custom.LSObject import LSObject
from Source.Widgets.LSCustomPin import LSCustomPin
from Source.Widgets.Pin.LSOperatorDataPin import LSOperatorDataPin
from Source.Widgets.NodeItem.Operator.LSOperatorNodeItem import LSOperatorNodeItem
from Source.Widgets.Pin.LSPin import LSPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()


class AddPinPin(LSCustomPin):
    add_pin_signal=Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def init_ui(self):
        super().init_ui()
        self.pin_layout=QHBoxLayout(self)
        self.pin_layout.setContentsMargins(0,0,0,0)
        self.pushButton=QPushButton()
        self.pushButton.setStyleSheet('''
        QPushButton[status=normal]{background-color:transparent;color:rgb(155,155,155);border:none;}
        QPushButton[status=hover]{background-color:transparent;color:rgb(255,255,255);border:none;}
        ''')
        self.pushButton.setProperty("status","normal")

        self.pushButton.setText("添加引脚+")
        self.pin_layout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.add_pin_signal.emit)


    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.pushButton.setProperty("status","hover")
        Util.repolish(self.pushButton)
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.pushButton.setProperty("status","normal")
        Util.repolish(self.pushButton)
        self.setCursor(Qt.ArrowCursor)

class LSOperatorNodeItem_Add(LSOperatorNodeItem):
    __LS_TYPE_NAME__ = "Add"

    def duplicate(self, *args, **kwargs) -> "LSNodeItem":
        ins=super().duplicate(*args, **kwargs)
        return ins

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def init_pins_from_identifier(self):
        self.add_pin(
            LSOperatorDataPin(flow=PinFlow.In, ),
        )
        self.add_pin(
            LSOperatorDataPin(flow=PinFlow.In, ),
        )

        with self.register_variable_pin_data():
            self.add_pin_button_pin = AddPinPin(flow=PinFlow.Out)
            self.out_pin = LSOperatorDataPin(flow=PinFlow.Out, title="value")

        self.add_pin(self.out_pin,)
        self.add_pin(self.add_pin_button_pin)
        self.finished_init()

    def finished_init(self):
        super().finished_init()
        self.add_pin_button_pin.add_pin_signal.connect(self.add_input_pin)

    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()
        self.body_layout.setVerticalSpacing(10)
        self.body_layout.setHorizontalSpacing(10)

        
    def init_ui(self):
        super().init_ui()


    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()


    def add_input_pin(self):
        self.out_pin = self.add_pin(
            LSOperatorDataPin(flow=PinFlow.In),
        )

if __name__ == '__main__':
    app=QApplication()
    window=LSOperatorNodeItem_Add()
    window.show()
    app.exec_()
