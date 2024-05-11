from PySide2.QtCore import Qt, QCoreApplication

from Source.Common.Func import OS

from unittest import TestCase
from PySide2.QtWidgets import *
from Source.Widgets.LSGraphicsView import LSGraphicsView
from Source.Widgets.NodeItem.LSGetVariableNodeItem import LSGetVariableNodeItem

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

screen_shot_dir=OS.join(OS.dirnameTimes(__file__),"Screenshot")
class TestGraphicsView(TestCase):
    def setUp(self) -> None:
        self.app = QApplication()
        self.view = LSGraphicsView()
        # self.view.resize(2000,1000)
        # Util.process_sleep(300)

    def test_1(self):
        item=LSGetVariableNodeItem()
        self.view.add_item(item)

        self.view.show()
        self.app.exec_()



if __name__ == '__main__':

    v=TestGraphicsView()
