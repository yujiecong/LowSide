
from Source import Globs
from PySide2.QtWidgets import *
from Source.Common.Func import OS
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Widgets.PinIconWidget.LSOperatorDataPinIconWidget import LSOperatorDataPinWidget
from Source.Widgets.Pin.LSDataPin import LSDataPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSOperatorDataPin(LSDataPin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "如果有父了 就不要调用了"


    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_body(self):
        super().init_body()
        # if self.get_flow() == PinFlow.In:
        #     self.pin_layout.setContentsMargins(0, 0,0,0)
        #     # self.pin_layout.addItem(self.icon_spacer,0,1)
        #     self.pin_layout.addWidget(self._pin_icon, 0, 0)
        #
        # else:
        #     self.pin_layout.setContentsMargins(0, 0,0,0)
        #     # self.pin_layout.addItem(self.icon_spacer, 0, 0)
        #     self.pin_layout.addWidget(self._pin_icon, 0, 1)
        #
        #
        # self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)

    def init_ui(self):
        super().init_ui()
        if self.get_flow() == PinFlow.In:
            pass
        else:
            self.pin_icon.main_layout.setContentsMargins(0, 0, 0, 0)


    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

    def init_connection(self):
        super().init_connection()

    @property
    def pin_icon_type(self):
        return LSOperatorDataPinWidget
if __name__ == '__main__':
    app=QApplication()
    window=LSOperatorDataPin()
    window.show()
    app.exec_()
