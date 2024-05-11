import time

from PySide2.QtCore import QCoreApplication, Qt

from Source.Custom.Enums.LSPinEnum import PinFlow, LSPinAttrType
from Source.Common.Func import OS
from Source.Widgets.NodeItem.Control.LSControlNodeItem_If import LSControlNodeItem_If
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source.Widgets.Pin.LSExecPin import LSExecPin

from unittest import TestCase
from PySide2.QtWidgets import *
from Source.Widgets.NodeItem.Event.LSExecNodeItem import LSExecNodeItem
from Source.Widgets.LSGraphicsView import LSGraphicsView

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# QCoreApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

screen_shot_dir=OS.join(OS.dirnameTimes(__file__),"Screenshot")
class TestGraphicsView(TestCase):
    def setUp(self) -> None:
        self.app = QApplication()
        self.view = LSGraphicsView()
        # self.view.resize(2000,1000)
        # Util.process_sleep(300)

    def screen_shot(self):
        pixmap=self.view.grab(self.view.rect())
        thumbnail_path=OS.join(screen_shot_dir,f"{time.time()}.jpg")
        pixmap.save(thumbnail_path)

    def test_connect(self):
        gw1 = LSExecNodeItem()
        gw2 = LSExecNodeItem()
        gw4 = LSControlNodeItem_If()



        data_pin1=gw1.add_pin(LSDataPin(PinFlow.Out, attr_type=LSPinAttrType.object))
        data_pin2=gw1.add_pin(LSDataPin(PinFlow.In, title="目标(self)", attr_type=LSPinAttrType.object))


        gw2_data_pin1=gw2.add_pin(LSDataPin(PinFlow.In, attr_type=LSPinAttrType.object))
        gw2_data_pin2=gw2.add_pin(LSDataPin(PinFlow.Out, attr_type=LSPinAttrType.object))





        turing_point_item=self.view.create_bidirectional_item()
        turing_point_item.proxy.moveBy(0,300)
        #
        turing_point_item2=self.view.create_bidirectional_item()
        turing_point_item2.proxy.moveBy(110,300)
        #
        # turing_point_item.pin.connect_pin(turing_point_item2.pin)
        # gw1.pins[1].connect_pin(gw2.pins[0])
        #
        # turing_point_item.pin.connect_pin(gw1.pins[1])
        # turing_point_item.pin.connect_pin(gw2.pins[0])
        gw2.pins[1].connect_pin(turing_point_item.pins[0])

        gw1.pins[1].connect_pin(turing_point_item.pins[0])

        self.view.add_item(gw1)
        self.view.add_item(gw2)
        # self.view.add_item(gw4)


        gw1.proxy.moveBy(-400,0)
        # gw2.proxy.moveBy(00,00)
        # gw4.proxy.moveBy(10,-200)

        self.view.show()
        self.app.exec_()

    def test_connect2(self):
        gw1 = LSExecNodeItem(self.view)
        pin11=gw1.add_pin(LSExecPin(PinFlow.Out))

        gw2 = LSExecNodeItem(self.view)
        pin21=gw2.add_pin(LSExecPin(PinFlow.In))


        pin11.connect_pin(pin21)
        data=gw1.serialize()

        self.view.add_item(gw1)
        self.view.add_item(gw2)
        gw1.proxy.setPos(-200,0)

        self.view.show()
        self.app.exec_()


if __name__ == '__main__':

    v=TestGraphicsView()
    v.test_connect()