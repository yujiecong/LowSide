
from Source import Globs
from PySide2.QtWidgets import *
from Source.Common.Func import OS
from Source.Widgets.PinIcon.LSOperatorDataPinIcon import LSOperatorDataPinIcon
from Source.Widgets.PinIconWidget.LSDataPinIconWidget import LSDataPinWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class LSOperatorDataPinWidget(LSDataPinWidget):
    def init_icon(self):
        self.icon=LSOperatorDataPinIcon(self.pin,self.attr_type)
        self.main_layout.addWidget(self.icon)

if __name__ == '__main__':
    app=QApplication()
    window=LSOperatorDataPinWidget()
    window.show()
    app.exec_()
