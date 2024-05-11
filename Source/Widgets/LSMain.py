import ast
import json
import logging
import os
import pprint
import sys
import traceback

from PySide2.QtCore import *
from PySide2.QtGui import QKeyEvent, QShowEvent, QIcon
from PySide2.QtWidgets import *

from Source.Custom.LSIcons import LSIcons
from Source.Widgets.LSDetailTreeWidget import LSDetailTreeWidget

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
from Source.Common.Func import OS
from Source.Common.Logger import ls_print
from Source.Common.Obj import LSDictWrapper
from Source.Widgets.LSPropertyTreeWidget import LSPropertyTreeWidget
from Source.Widgets.LSTabWidget import LSTabWidget
from Source import Main_ui, Globs
from Source.Custom.LSObject import LSObject
from Source.Custom.LSResolver import LSResolver
import Source.Init.InitResources

Source.Init.InitResources

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSMain(QMainWindow, Main_ui.Ui_MainWindow, LSObject):
    def __init__(self):
        super(LSMain, self).__init__()
        LSObject.__init__(self)
        self.init_serialize_data()

    def init_properties(self):
        self.setWindowFlags(Qt.WindowType.Widget)
        self.setDockOptions(
            QMainWindow.AnimatedDocks |
            QMainWindow.AllowNestedDocks)
        # self.setDockOptions(
        #     QMainWindow.AnimatedDocks |
        #     QMainWindow.AllowNestedDocks)

    def init_style(self):
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        pass

    def init_attrs(self):
        self.resolver = LSResolver()

    def init_ui(self):
        self.setupUi(self)
        # self.center_widget = LSMainWindow(self)
        # self.verticalLayout_2.addWidget(self.center_widget)
        self.property_tree_widget = LSPropertyTreeWidget(self)
        self.detail_tree_widget = LSDetailTreeWidget(self)

        self.property_tree_widget.clickedVariable_signal.connect(self.detail_tree_widget.update_detail)
        self.detail_tree_widget.changeProperty_signal.connect(self.property_tree_widget.change_variable)

        self.verticalLayout_3.addWidget(self.property_tree_widget)
        self.verticalLayout_4.addWidget(self.detail_tree_widget)

        self.tab_widget = LSTabWidget(
            self.property_tree_widget,
            self.detail_tree_widget,
        )
        self.verticalLayout_2.addWidget(self.tab_widget)

        # self.tab_dock = QDockWidget(self)
        # self.tab_dock.setWindowFlag(Qt.WindowType.Widget)
        # self.tab_dock.setWidget(self.tab_widget)
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tab_dock)
        "如果只有一个dock 会崩溃"
        # self.variable_dock = QDockWidget(self)
        # # self.variable_dock.titleBarWidget().hide()
        # self.variable_dock.setWidget(None)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.variable_dock)

        # self.setCentralWidget(self.center_widget)

    def init_serialize_data(self):
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.tab_data = self.tab_widget.serialize

    def save(self):
        # current_path=self.tab_widget.current_view.current_path
        # current_path=fr"{Globs.test_dir}\serialize\main.pyls"
        if self.tab_widget.current_tab:
            if not self.tab_widget.current_tab.is_saved:
                user_path, _ = QFileDialog.getSaveFileName(self, "Save",Globs.example_dir,
                                                           f"LowSide File (*{Globs.LOWSIDE_FILE_TYPE})",
                                                           )
            else:
                user_path = self.tab_widget.current_tab.saved_path
        else:
            user_path=None
        ls_print("save", user_path)
        if not user_path:
            return
        main_data = self.serialize()
        if OS.exists(user_path):
            backup = open(user_path, "r", encoding='utf8').read()
            with open(user_path, "w", encoding='utf8') as f:
                try:
                    json.dump(main_data, f, indent=2)
                except Exception as e:
                    f.write(backup)
                    pprint.pprint(main_data)
                    ls_print(traceback.print_exc(), log_level=logging.ERROR)
        else:
            with open(user_path, "w", encoding='utf8') as f:
                json.dump(main_data, f, indent=2)

        self.tab_widget.save_current(user_path)
        self.tab_widget.update_user_cache()
    @Globs.disable_record_command
    def load_last(self):
        for loaded_path in Globs.user_cache.loaded_paths:
            try:
                serialized_data = json.load(open(loaded_path, "r", encoding="utf8"))
                wrapper_data: "LSMain" = LSDictWrapper(serialized_data)
                self.tab_widget.add_view_tab(loaded_path, LSDictWrapper(wrapper_data.tab_data))
            except Exception as e:
                self.tab_widget.add_view_tab()
                ls_print(traceback.print_exc(), log_level=logging.ERROR)

    @Globs.disable_record_command
    def load(self):
        path=QFileDialog.getOpenFileName(self, "Open", Globs.example_dir,
                                         f"LowSide File (*{Globs.LOWSIDE_FILE_TYPE})")[0]
        try:
            serialized_data = json.load(open(path, "r", encoding="utf8"))
            wrapper_data: "LSMain" = LSDictWrapper(serialized_data)
            self.tab_widget.add_view_tab(path, LSDictWrapper(wrapper_data.tab_data))
        except Exception as e:
            self.tab_widget.add_view_tab()
            ls_print(traceback.print_exc(), log_level=logging.ERROR)

    def restart_program(self):
        return
        # 获取当前程序的路径和参数
        program = sys.argv[0]
        arguments = sys.argv[1:]
        os.popen(f'{sys.executable} {program}')
        # 启动一个新的进程，重新运行当前程序
        # process = QProcess()
        # process.startDetached(program, arguments)
        # 关闭当前程序
        # 创建一个定时器，在一段时间后退出程序
        QCoreApplication.quit()

    def generate_code(self):
        start_ast = ast.Module(body=[], type_ignores=[])
        variable_ast = self.property_tree_widget.generate_code()
        start_ast.body.extend(variable_ast)

        if self.tab_widget.current_tab:
            self.tab_widget.current_tab.generate_code(start_ast)

        ast.fix_missing_locations(start_ast)
        ls_print("generate_code")
        # for node in start_ast.body:
        #     print(ast.unparse(node),ast.dump(node))
        print(ast.unparse(start_ast))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # if event.isAutoRepeat():
        #     return
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        elif event.key() == Qt.Key_F12:
            self.restart_program()
        elif event.key() == Qt.Key_S and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.save()
        elif event.key() == Qt.Key_O and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.load()
        elif event.key() == Qt.Key_N and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.tab_widget.add_view_tab()
        elif event.key() == Qt.Key_Z and QApplication.keyboardModifiers() == Qt.ControlModifier:
            with Globs.DisableRecordCommandContext():
                if self.tab_widget.current_tab:
                    self.tab_widget.current_tab.tab_view.undo_stack.undo()
        elif event.key() == Qt.Key_F5:
            self.generate_code()


if __name__ == '__main__':
    app = QApplication()
    window = LSMain()
    window.load_last()
    window.show()
    app.exec_()
