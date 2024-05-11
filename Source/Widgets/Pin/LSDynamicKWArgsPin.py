from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.Pin.LSDynamicKWArgsSubPin import LSDynamicKWArgsSubPin
from Source.Widgets.Pin.LSDynamicDataPin import LSDynamicDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSDynamicKWArgsPin(LSDynamicDataPin):
    def init_attrs(self):
        super().init_attrs()

    def init_connection(self):
        super().init_connection()
        self.append_kwarg_btn.clicked.connect(lambda :self.add_sub_pin())

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()
        self.pin_layout.setSpacing(5)
        self.append_kwarg_btn=QPushButton()
        self.append_kwarg_btn.setFixedSize(16,16)
        self.append_kwarg_btn.setIcon(QIcon(LSIcons.add_svg))
        self.pin_layout.addWidget(self.append_kwarg_btn,0,2)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

    def create_sub_pin(self,sub_pin_idx) -> LSDynamicKWArgsSubPin:
        return LSDynamicKWArgsSubPin(flow=self.get_flow(), attr_type=LSPinAttrType.object,
                                     key=f"kwarg{sub_pin_idx}")




if __name__ == '__main__':
    app=QApplication()
    window=LSDynamicKWArgsPin()
    window.show()
    app.exec_()
