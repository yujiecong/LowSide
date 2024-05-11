from unittest import TestCase

from PySide2.QtWidgets import QApplication
from Source.Widgets.LSMain import LSMain
class TestGraphicsView(TestCase):
    app = QApplication()

    def test_load(self):
        window = LSMain()
        window.load_last()
        window.show()
        self.app.exec_()