import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.centre = QMainWindow(self)
        self.centre.setWindowFlags(Qt.Widget)
        self.centre.setDockOptions(
            QMainWindow.AnimatedDocks |
            QMainWindow.AllowNestedDocks)
        self.setCentralWidget(self.centre)
        self.dockCentre1 = QDockWidget(self.centre)
        self.dockCentre1.setWindowTitle('Centre 1')
        self.centre.addDockWidget(
            Qt.LeftDockWidgetArea, self.dockCentre1)
        self.dockCentre2 = QDockWidget(self.centre)
        self.dockCentre2.setWindowTitle('Centre 2')
        self.centre.addDockWidget(
            Qt.RightDockWidgetArea, self.dockCentre2)
        self.dockLeft = QDockWidget(self)
        self.dockLeft.setWindowTitle('Left')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockLeft)
        self.dockRight = QDockWidget(self)
        self.dockRight.setWindowTitle('Right')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockRight)
        self.menuBar().addMenu('File').addAction('Quit', self.close)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(500, 50, 600, 400)
    window.show()
    sys.exit(app.exec_())