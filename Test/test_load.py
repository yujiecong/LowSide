from PySide2.QtCore import Qt, QCoreApplication

from Source import Globs
from Source.Common.Func import OS

from unittest import TestCase
from PySide2.QtWidgets import *

from Source.Custom.LSResolver import LSResolver
from Source.Widgets.LSGraphicsView import LSGraphicsView
import Source.Init.InitResources

Source.Init.InitResources
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

screen_shot_dir=OS.join(OS.dirnameTimes(__file__),"Screenshot")
class TestGraphicsView(TestCase):
    def setUp(self) -> None:
        self.app = QApplication()
        self.view = LSGraphicsView()


    def test_1(self):
        self.resolver = LSResolver()

        self.view.show()
        self.app.exec_()

