
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Common.Func import OS
from Source.Custom.LSIcons import LSIcons
from Source.Custom.LSObject import LSObject

from Source.Widgets.Pin.LSDynamicDataSubPin import LSDynamicDataSubPin
from Source.Widgets.Pin.LSPinLineEdit import LSPinLineEdit

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDynamicKWArgsSubPin(LSDynamicDataSubPin):

    @classmethod
    def deserialize(cls,new_item_instance, wrapper: "LSDynamicKWArgsSubPin"):
        new_pin = super().deserialize(new_item_instance, wrapper)
        new_pin.set_key(wrapper.key)
        return new_pin

    def __init__(self,key="",*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("")
        with LSObject.Record(self, LSObject.RecordType.Duplicate | LSObject.RecordType.Serialize):
            self.key=key

        self.set_key(self.key)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.pin_layout.setContentsMargins(10, 0, 4, 0)
        self.pin_layout.setSpacing(5)
        self.remove_arg_btn=QPushButton()
        self.remove_arg_btn.setFixedSize(16,16)
        self.remove_arg_btn.setIcon(QIcon(LSIcons.remove_svg))
        self.pin_layout.addWidget(self.remove_arg_btn,0,2)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()
        self.remove_arg_btn.clicked.connect(self.destoryed)
        self.lineedit.textChanged.connect(self.set_key)

    def init_body(self):
        super().init_body()
        self.lineedit = LSPinLineEdit()
        if self.get_flow() == PinFlow.In:
            self.pin_layout.addWidget(self.lineedit,0,1)
            self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)
        else:
            self.pin_layout.addWidget(self.lineedit,0,0)
            self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)
        self.lineedit.setText(self.title)


    def set_key(self, key: str):
        self.key=key
        self.lineedit.setText(key)


    def set_title(self, title: str):
        pass

if __name__ == '__main__':
    app=QApplication()
    window=LSDynamicKWArgsSubPin()
    window.show()
    app.exec_()
