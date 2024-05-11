from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.Pin.LSDynamicArgsSubPin import LSDynamicArgsSubPin
from Source.Widgets.Pin.LSDynamicDataPin import LSDynamicDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSDynamicArgsPin(LSDynamicDataPin):
    def init_attrs(self):
        super().init_attrs()

    def init_connection(self):
        super().init_connection()
        self.append_arg_btn.clicked.connect(lambda: self.add_sub_pin())

    def init_ui(self):
        super().init_ui()
        self.pin_layout.setSpacing(5)
        self.append_arg_btn = QPushButton()

        self.append_arg_btn.setFixedSize(16, 16)
        self.append_arg_btn.setIcon(QIcon(LSIcons.add_svg))
        self.pin_layout.addWidget(self.append_arg_btn,0,2)

    def create_sub_pin(self,sub_pin_idx) -> LSDynamicArgsSubPin:

        return LSDynamicArgsSubPin(flow=self.get_flow(), attr_type=LSPinAttrType.object,
                                   title=f"arg{sub_pin_idx}")




if __name__ == '__main__':
    app = QApplication()
    window = LSDynamicArgsPin()
    window.show()
    app.exec_()
