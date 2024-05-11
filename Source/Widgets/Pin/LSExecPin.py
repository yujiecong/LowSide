from PySide2.QtWidgets import *
from Source import Globs
from Source.Custom.Enums.LSPinEnum import PinType, PinFlow, LSPinAttrType
from Source.Common.Func import OS
from Source.Custom.LSAstData import LSAstCodeFragmentName

from Source.Widgets.PinIconWidget.LSExecPinIconWidget import LSExecPinWidget
from Source.Widgets.Pin.LSFlowPin import LSFlowPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSExecPin(LSFlowPin):
    def __init__(self,attr_type=LSPinAttrType.null, *args, **kwargs):
        super().__init__(attr_type=attr_type,*args, **kwargs)
        self.code_fragment = LSAstCodeFragmentName.body


    def init_ui(self):
        """
        这个是图片的icon 所以在这里声明
        :return:
        """
        super().init_ui()
        if self.get_flow() == PinFlow.In:
            "血的教训啊 加了弹簧会在 graphicsview 移除item后 有wheelevent之后 崩溃"
            "貌似是发生在第二次 addItem 之后 因为父类已经add过了"
            # self.pin_layout.addItem(self.icon_spacer)
            # self.pin_icon.main_layout.setContentsMargins(0, 4, 0, 4)
        else:
            "同上"
            # self.pin_layout.insertItem(0, self.icon_spacer)
            # self.pin_icon.main_layout.setContentsMargins(21, 0, 0, 0)

    def init_properties(self):
        super().init_properties()
        # self.setFixedWidth(LSExecPin.FixedWidth)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)
        # self.setStyleSheet("background-color:red;")

    def init_connection(self):
        super().init_connection()


    @property
    def pin_icon(self) -> LSExecPinWidget:
        return self._pin_icon

    @property
    def pin_icon_type(self):
        return LSExecPinWidget

    def get_flow(self) -> PinFlow:
        return self.flow

    def get_type(self) -> PinType:
        return PinType.Exec




if __name__ == '__main__':
    app = QApplication()
    window = LSExecPin()
    window.show()
    app.exec_()
