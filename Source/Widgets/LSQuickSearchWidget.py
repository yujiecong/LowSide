import collections
import pprint
import typing

from PySide2.QtCore import *

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from Source.Common import Func
from Source.Custom.LSAstData import LSAstIdentifierSplitter
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSNodeSourceType
from Source.Custom.LSColor import PinAttrTypeExternalColor
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSIcons import LSIcons
from Source.Common.Func import OS
from Source.Custom.LSItemData import LSRawAstItemData, LSRawVariableData
from Source.Custom.LSMimeData import LSMimeData
from Source.Custom.LSObject import LSObject

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()

class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText("搜索")

    def keyPressEvent(self, arg__1) -> None:
        super().keyPressEvent(arg__1)
        if arg__1.key()==Qt.Key_Down:
            arg__1.ignore()

class _SearchWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.brush = QBrush(QColor(15, 15, 15))
        self.pen = QPen(QColor(15, 97, 180))
        self.pen.setWidth(2)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.brush)
        painter.setPen(self.pen)

        rect = self.rect()
        rect.setWidth(rect.width() - 1);
        rect.setHeight(rect.height() - 1);
        painter.drawRoundedRect(rect, 5, 5);
        painter.end()

class _SearchTreeWidget(QTreeWidget):
    placed_signal = Signal(LSMimeData)

    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        # self.itemDoubleClicked.connect(self.click_item)
        self.clicked.connect(self.click_item)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        "icon大小"
        self.setIconSize(QSize(12, 12))
        "branch大小"
        self.setIndentation(14)

    def click_item(self, model_index: QModelIndex):
        item = self.currentItem()
        if isinstance(item, (FuncTreeItem,
                             EventTreeItem,
                             ControlTreeItem,
                             ClassMagicMethodItem,
                             VariableTreeItem,ClassTreeItem)):
            if isinstance(item,ClassTreeItem):
                self.placed_signal.emit(LSMimeData(item.init_item.identifier,pos=self.parent.pos()))
            else:
                self.placed_signal.emit(LSMimeData(item.identifier,pos=self.parent.pos()))


    def wheelEvent(self, arg__1:QWheelEvent):
        super().wheelEvent(arg__1)
        arg__1.accept()

class TreeColumn:
    Zero = 0


class IconTreeItem(QTreeWidgetItem):
    icon = None

    @staticmethod
    def init_icon():
        raise NotImplementedError

    def __init__(self, identifier, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = identifier
        self.setText(TreeColumn.Zero, text)
        type(self).init_icon()
        # pixmap:QPixmap=type(self).icon.pixmap(8,8)
        # self.setIcon(TreeColumn.Zero, pixmap)
        self.setIcon(TreeColumn.Zero, type(self).icon)


class FolderTreeItem(IconTreeItem):
    @staticmethod
    def init_icon():
        FolderTreeItem.icon = QIcon(LSIcons.folder_svg)


class ClassTreeItem(IconTreeItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.init_item=None
    @staticmethod
    def init_icon():
        ClassTreeItem.icon = QIcon(LSIcons.objects_svg)


class FuncTreeItem(IconTreeItem):
    @staticmethod
    def init_icon():
        FuncTreeItem.icon = QIcon(LSIcons.function_svg)

class ClassFuncTreeItem(FuncTreeItem):
    @staticmethod
    def init_icon():
        ClassFuncTreeItem.icon = QIcon(LSIcons.function_svg)


class EventTreeItem(IconTreeItem):
    @staticmethod
    def init_icon():
        EventTreeItem.icon = QIcon(LSIcons.event_svg)

class ControlTreeItem(IconTreeItem):
    @staticmethod
    def init_icon():
        ControlTreeItem.icon = QIcon(LSIcons.controls_svg)

class ClassMagicMethodItem(IconTreeItem):
    @staticmethod
    def init_icon():
        ClassMagicMethodItem.icon = QIcon(LSIcons.class_func_svg)

class VariableTreeItem(IconTreeItem):
    def __init__(self,attr_type,*args,**kwargs):
        super().__init__(*args,**kwargs)

        color = PinAttrTypeExternalColor(attr_type)
        pixmap = QPixmap(16, 16)  #
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        # 绘制一个蓝色的圆形
        painter.drawRoundedRect(0, 4, 16, 8, 3, 3)
        painter.end()

        self.setIcon(TreeColumn.Zero, pixmap)

    @staticmethod
    def init_icon():
        VariableTreeItem.icon=QIcon()


class LSQuickSearchWidget(QFrame, LSObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LSObject.__init__(self, *args, **kwargs)

    def init_attrs(self):
        super().init_attrs()
        self.builtins_data_dict = {}
        self.event_data_dict = {}

    def init_tree_widget(self):
        self.tree_widget.setHeaderHidden(True)

    def init_properties(self):
        super().init_properties()
        self.setFixedSize(300, 300)
        self.setting_button.setFixedSize(16,16)
        self.setObjectName("LSQuickSearchWidget")
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.title_layout.setContentsMargins(2, 2, 2, 2)

        self.search_label.setFixedSize(12, 12)
        self.search_label.setScaledContents(True)
        self.search_label.setPixmap(LSIcons.search_svg)
        self.search_layout.setContentsMargins(6, 3, 3, 3)
        self.search_layout.setSpacing(5)

        self.split_line.setLineWidth(2)
        self.split_line.setFrameShape(QFrame.HLine)

        self.checkbox.setObjectName("checkbox")
        self.title_widget.setObjectName("title_widget")
        self.title_label.setObjectName("title_label")
        self.search_widget.setObjectName("search_widget")
        self.search_lineedit.setObjectName("search_line")
        self.split_line.setObjectName("split_line")
        self.tree_widget.setObjectName("tree_widget")
        self.prompt_label.setObjectName("prompt_label")
        self.body_widget.setObjectName("body_widget")

        self.setTabOrder(self.search_lineedit, self.tree_widget)

    def init_ui(self):
        super().init_ui()
        self.main_layout = QVBoxLayout()
        self.title_widget = QWidget()
        self.title_layout = QHBoxLayout(self.title_widget)

        self.title_label = QLabel("可执行操作")
        self.checkbox = QCheckBox("情景关联")
        self.setting_button = QPushButton()
        self.setting_button.setIcon(QIcon(LSIcons.setting_svg))

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.checkbox)
        self.title_layout.addWidget(self.setting_button)

        self.search_widget = _SearchWidget()
        self.search_layout = QHBoxLayout(self.search_widget)

        self.search_label = QLabel()
        self.search_lineedit = LineEdit()

        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_lineedit)

        self.prompt_label = QLabel("选择组件来查看可用事件和函数")
        self.split_line = QFrame()
        self.tree_widget = _SearchTreeWidget(self)

        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)

        self.main_layout.addWidget(self.title_widget)

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.body_widget)

        self.body_layout.addWidget(self.prompt_label)
        self.body_layout.addWidget(self.split_line)
        self.body_layout.addWidget(self.tree_widget)

        self.setLayout(self.main_layout)

        self.init_tree_widget()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()
        self.search_lineedit.textChanged.connect(self.search)

    def search(self,text):
        """
        TODO: 优化这里的速度
        :param text:
        :return:
        """
        iterator = QTreeWidgetItemIterator(self.tree_widget)
        show_items=[]
        while iterator.value():
            item = iterator.value()
            # if isinstance(item, FuncTreeItem):
            if text.lower() in item.identifier.lower():
                show_items.append(item)
            item.setHidden(True)
            iterator += 1  # 移动到下一个项

        for item in show_items:
            item.setHidden(False)

            item_parent = item.parent()
            while item_parent:
                item_parent.setHidden(False)
                item_parent = item_parent.parent()
        if text:
            self.tree_widget.expandAll()
    def update_ast_data(self):
        # 专门更新ast数据
        data_items = LSIdentifierData.FromAst.items()
        self.update_tree(data_items)

    def update_variable_data(self):
        # 专门更新变量数据
        data_items = LSIdentifierData.FromVariable.items()
        self.update_tree(data_items)

    def update_builtin_data(self):
        # 专门更新变量数据
        data_items = LSIdentifierData.FromBuiltin.items()
        self.update_tree(data_items)
    def update_plugins_data(self):
        # 专门更新变量数据
        data_items = LSIdentifierData.FromPlugins.items()
        self.update_tree(data_items)

    def update_all_data(self):
        self.tree_widget.clear()
        self.update_ast_data()
        self.update_variable_data()
        self.update_builtin_data()
        self.update_plugins_data()
        self.search(self.search_lineedit.text())
        # self.tree_widget.expandAll()
        for root_idx in range(self.tree_widget.topLevelItemCount()):
            self.tree_widget.topLevelItem(root_idx).setExpanded(True)

    def update_tree(self,data_items):

        # pprint.pprint(LSGlobalData.IdentifierNodeData)
        module_cache = {}
        object_cache = {}
        # sort
        data_items = collections.OrderedDict(sorted(data_items, key=lambda x: x[0]))
        for identifier, node_ast_info in data_items.items():
            node_ast_info:typing.Union[LSRawAstItemData,LSRawVariableData]
            module_path, object_path = identifier.rsplit(LSAstIdentifierSplitter.IdentifierSplitter, 1)
            if module_path[0] == LSAstIdentifierSplitter.IdentifierSplitter:
                module_path = module_path[1:]

            module_split = module_path.split(LSAstIdentifierSplitter.IdentifierSplitter)
            for module_split_idx, ever_module in enumerate(module_split):
                cur_module_split_path = LSAstIdentifierSplitter.IdentifierSplitter.join(
                    module_split[:module_split_idx + 1])
                last_module_split_path = LSAstIdentifierSplitter.IdentifierSplitter.join(module_split[:module_split_idx])
                parent_item = module_cache.get(last_module_split_path, self.tree_widget.invisibleRootItem())
                if cur_module_split_path not in module_cache:

                    module_split_tree_item = FolderTreeItem(cur_module_split_path, ever_module)

                    module_cache[cur_module_split_path] = module_split_tree_item
                    parent_item.addChild(module_split_tree_item)

            object_item_parent = module_cache[module_path]
            # print(object_path,module_path,object_item_parent)

            object_split = object_path.split(LSAstIdentifierSplitter.ClassSplitter)
            for object_split_idx, ever_object in enumerate(object_split):
                cur_obj_split_path = LSAstIdentifierSplitter.ClassSplitter.join(object_split[:object_split_idx + 1])
                last_obj_split_path = LSAstIdentifierSplitter.ClassSplitter.join(object_split[:object_split_idx])
                cur_identifier = Func.ls_joinPaths(module_path, cur_obj_split_path)
                last_identifier = Func.ls_joinPaths(module_path, last_obj_split_path)
                if object_split_idx==0:
                    obj_parent_item = object_item_parent
                else:
                    obj_parent_item= object_cache[last_identifier]
                if object_split_idx == len(object_split) - 1:
                    "这个是函数"
                    if node_ast_info.node_type == LSNodeItemType.Stubs:
                        if isinstance(obj_parent_item,ClassTreeItem):
                            node_item = ClassFuncTreeItem(cur_identifier, ever_object)
                        else:
                            node_item = FuncTreeItem(cur_identifier, ever_object)
                    elif node_ast_info.node_type == LSNodeItemType.ClassMagicMethod:
                        node_item = ClassMagicMethodItem(cur_identifier, ever_object)
                        if node_ast_info.func_name=="__init__":
                            obj_parent_item.init_item=node_item
                    elif node_ast_info.node_type == LSNodeItemType.Event:
                        node_item = EventTreeItem(cur_identifier, ever_object)
                    elif node_ast_info.node_type == LSNodeItemType.Control:
                        node_item = ControlTreeItem(cur_identifier, ever_object)
                    elif node_ast_info.node_type == LSNodeItemType.Variable:
                        obj_parent_item.setIcon(TreeColumn.Zero, QIcon(LSIcons.variable_svg))
                        node_item = VariableTreeItem(node_ast_info.attr_type, cur_identifier, ever_object)
                    elif node_ast_info.node_type == LSNodeItemType.Operator:
                        node_item = FuncTreeItem(cur_identifier, ever_object)
                    else:
                        raise ValueError

                    obj_parent_item.addChild(node_item)
                else:
                    if cur_identifier not in object_cache:
                        obj_split_tree_item = ClassTreeItem(cur_identifier, ever_object)
                        object_cache[cur_identifier] = obj_split_tree_item
                        obj_parent_item.addChild(obj_split_tree_item)



    def keyPressEvent(self, event) -> None:
        selected_items = self.tree_widget.selectedItems()
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            if not selected_items:
                self.tree_widget.setCurrentItem(self.tree_widget.topLevelItem(0))
                self.tree_widget.setFocus()
            else:
                if selected_items[0]==self.tree_widget.topLevelItem(0) and event.key() == Qt.Key_Up:
                    self.tree_widget.clearSelection()
                    self.search_lineedit.setFocus()

        elif event.key() == Qt.Key_Return:
            if selected_items:
                self.tree_widget.click_item(None)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.search_lineedit.clear()
        self.search_lineedit.setFocus()
        self.update_all_data()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.search_lineedit.setFocus()

if __name__ == '__main__':
    app = QApplication()
    window = LSQuickSearchWidget()
    window.show()
    app.exec_()
