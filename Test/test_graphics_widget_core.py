from unittest import TestCase

from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem


class TestGraphicsWidgetCore(TestCase):


    def test_add_body_line(self):
        app = QApplication()
        window = LSNodeItem(None)
        window.show()
        app.exec_()
