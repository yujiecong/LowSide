import ast

from Source import Globs
from PySide2.QtWidgets import *

from Source.Common import Func
from Source.Common.Func import OS
from Source.Widgets.NodeItem.Event.LSEventNodeItem import LSEventNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSEventNodeItem_ProgramStart(LSEventNodeItem):
    __LS_TYPE_NAME__ = "开始运行"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def to_ast(self):
        return ast.Expr(value=ast.Constant(value="生成图形代码.."))


if __name__ == '__main__':
    app = QApplication()
    window = LSEventNodeItem_ProgramStart()
    window.show()
    app.exec_()
