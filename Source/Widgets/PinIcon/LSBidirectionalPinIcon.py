
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from Source.Custom.LSColor import LSColor
from Source.Common.Func import OS
from Source.Widgets.PinIcon.LSDataPinIcon import LSDataPinIcon

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSBidirectionalPinIcon(LSDataPinIcon):


    def init_attrs(self):
        super().init_attrs()
        self.disconnected_external_color=QColor(129, 122, 122, 155)
        self.disconnected_internal_color=Default = QColor(39, 37, 37)



    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()



    def _prepare_ellipse_color(self):
        if self.is_in_connected or self.is_out_connected:
            self.pen.setColor(LSColor.White)
            if self.is_out_connected:
                self.brush.setColor(LSColor.White)
            else:
                self.brush.setColor(QColor(20,20,20))
        else:
            self.brush.setColor(self.disconnected_internal_color)
            self.pen.setColor(self.disconnected_external_color)


    def _prepare_triangle_color(self):
        if self.is_in_connected or self.is_out_connected:
            self.pen.setColor(LSColor.White)
            self.brush.setColor(LSColor.White)
        else:
            self.pen.setColor(self.disconnected_external_color)
            self.brush.setColor(self.disconnected_external_color)

if __name__ == '__main__':
    app=QApplication()
    window=LSBidirectionalPinIcon()
    window.show()
    app.exec_()
