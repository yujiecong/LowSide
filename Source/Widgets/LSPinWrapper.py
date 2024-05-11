
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.Enums.LSPinEnum import PinFlow
from Source.Custom.LSObject import LSObject



qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSPinWrapper(QFrame):
    def __init__(self,pin,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "如果有父了 就不要调用了"
        self.pin=pin
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)
        self.lay.setContentsMargins(0, 0, 0, 0)

        if pin.get_flow()==PinFlow.In:
            self.lay.addWidget(self.pin)
            self.lay.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        else:
            self.lay.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
            self.lay.addWidget(self.pin)

if __name__ == '__main__':
    app=QApplication()
    window=LSPinWrapper()
    window.show()
    app.exec_()
