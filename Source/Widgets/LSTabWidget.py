import json
import logging
import time
import traceback
import typing

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.DataClass import LSVariableDetailData
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Common.Obj import LSDictWrapper
from Source.Custom.LSIcons import LSIcons
from Source.Custom.LSObject import LSObject
from Source.Widgets.LSGraphicsView import LSGraphicsView

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()



class _TabWidget(QWidget, LSObject):
    def __init__(self,property_tree ,wrapper_data:"_TabWidget"=None):
        super().__init__()
        LSObject.__init__(self)
        self.property_tree=property_tree
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.view_sdata = self.get_tab_view_data
            self.property_sdata = self.property_tree.serialize

        if wrapper_data:
            view_data = wrapper_data.view_sdata
            self.view = LSGraphicsView.deserialize(view_data)
            self.property_data=wrapper_data.property_sdata
        else:
            self.view = LSGraphicsView()
            self.property_data= None

        self.lay.addWidget(self.view)

    def init_attrs(self):
        super().init_attrs()
        self.is_saved = False
        self.saved_path = ""

    def init_ui(self):
        super().init_ui()
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)
        self.lay.setContentsMargins(0, 0, 0, 0)


    @property
    def tab_view(self):
        return self.view

    def get_tab_view_data(self):
        return self.tab_view.serialize()

    def generate_code(self,start_ast):
        return self.tab_view.generate_code(start_ast)
class LSTabWidget(QTabWidget, LSObject):
    def __init__(self, property_tree,detail_tree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self)
        self.current_tab: _TabWidget = None
        self.property_tree = property_tree
        self.detail_tree = detail_tree
        self.loaded_paths = self.get_loaded_paths

        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.tab_widget_data = self.get_tab_data

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()
        self.setTabsClosable(True)

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()
        self.tabCloseRequested.connect(self.remove_current_tab)
        self.currentChanged.connect(self.view_tab_changed)

    def add_view_tab(self, path=None,wrapper_data=None):
        ls_print("add tab", path)
        if wrapper_data:
            tab_data_wrapper:"LSTabWidget"=wrapper_data
            tab = _TabWidget(self.property_tree,LSDictWrapper(tab_data_wrapper.tab_widget_data))
            tab.is_saved = True
            tab.saved_path = path
            tab_title = OS.basename(path, suffix=True)
        else:
            tab = _TabWidget(self.property_tree)
            tab.is_saved = False
            tab.saved_path = None
            tab_title = "未命名.."

        tab.tab_view.selectItem_signal.connect(self.detail_tree.update_detail)
        self.current_tab = tab
        self.property_tree.update_view(tab.tab_view)

        tab_idx = self.addTab(self.current_tab, QIcon(LSIcons.python_svg), tab_title)
        self.setCurrentIndex(tab_idx)
        return tab_idx

    def remove_current_tab(self, idx):
        self.removeTab(idx)
        # self.update_user_cache()

    def update_user_cache(self):
        Globs.user_cache.loaded_paths = self.get_loaded_paths()
        Globs.user_cache.save()

    def save_current(self,saved_path):
        self.current_tab.is_saved=True
        self.current_tab.saved_path=saved_path
        self.setTabText(self.currentIndex(),OS.basename(saved_path,suffix=True))

    def view_tab_changed(self, idx):
        self.current_tab: _TabWidget = self.widget(idx)
        if self.current_tab:
            self.property_tree.update_property(self.current_tab.property_data)
        else:
            self.property_tree.update_property(None)

    def get_loaded_paths(self):
        paths = []
        for i in range(self.count()):
            widget: _TabWidget = self.widget(i)
            if widget.is_saved:
                paths.append(widget.saved_path)
        return paths

    def get_tab_data(self):
        return self.current_tab.serialize()

    def keyPressEvent(self, arg__1):
        super().keyPressEvent(arg__1)
        # elif arg__1.key() == Qt.Key_W and arg__1.modifiers() == Qt.ControlModifier:
        #     self.removeTab(self.currentIndex())

    def showEvent(self, arg__1) -> None:
        super().showEvent(arg__1)
        if self.current_tab:
            self.current_tab.setFocus()


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication()
    from Source.Widgets.LSPropertyTreeWidget import LSPropertyTreeWidget

    window = LSTabWidget(LSPropertyTreeWidget(None))
    window.add_view_tab()
    window.show()
    app.exec_()
