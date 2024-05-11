
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSAstData import LSAstIdentifierSplitter
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSIcons import LSIcons
from Source.Widgets.Common.LSAttrTypeIcon import LSAttrTypeIcon

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()

class TreeColumn:
    Zero = 0


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

class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText("搜索")

    def keyPressEvent(self, arg__1) -> None:
        super().keyPressEvent(arg__1)
        if arg__1.key() == Qt.Key_Down:
            arg__1.ignore()


class IconTreeItem(QTreeWidgetItem):
    icon = None

    @staticmethod
    def init_icon():
        raise NotImplementedError

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        type(self).init_icon()
        # pixmap:QPixmap=type(self).icon.pixmap(8,8)
        # self.setIcon(TreeColumn.Zero, pixmap)
        self.setIcon(TreeColumn.Zero, type(self).icon)


class BuiltinAttrTypeTreeItem(IconTreeItem):
    def __init__(self,attr_type,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setIcon(TreeColumn.Zero, LSAttrTypeIcon(attr_type))
        self.setText(TreeColumn.Zero, attr_type)
        self.attr_type=attr_type
        self.identifier = None


    @staticmethod
    def init_icon():
        BuiltinAttrTypeTreeItem.icon=QIcon()

class ClassTypeTreeItem(BuiltinAttrTypeTreeItem):
    def __init__(self, identifier, attr_type, *args, **kwargs):
        super().__init__(LSPinAttrType.user_class,*args, **kwargs)
        self.attr_type = attr_type
        self.identifier = identifier
        self.setText(TreeColumn.Zero, attr_type)
        self.setToolTip(TreeColumn.Zero, f"{identifier}:{attr_type}")

    @staticmethod
    def init_icon():
        ClassTypeTreeItem.icon=QIcon()


class _SearchTreeWidget(QTreeWidget):
    clicked_item=Signal(str)
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        # self.itemDoubleClicked.connect(self.click_item)
        self.clicked.connect(self.click_item)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.setWindowFlag(Qt.WindowType.Widget)
        "icon大小"
        self.setIconSize(QSize(16, 16))
        "branch大小"
        self.setIndentation(14)

    def click_item(self, model_index: QModelIndex):
        item = self.currentItem()
        if isinstance(item, (BuiltinAttrTypeTreeItem,ClassTypeTreeItem)):
            self.clicked_item.emit(item.attr_type)
            self.parent.deleteLater()

    def wheelEvent(self, arg__1:QWheelEvent):
        super().wheelEvent(arg__1)
        arg__1.accept()

    def keyPressEvent(self, event:QKeyEvent) -> None:
        if event.key()==Qt.Key_Return:
            self.click_item(None)


class LSAttrTypeSearchWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.init_attrs()
        self.init_ui()
        self.init_properties()
        self.init_style()
        self.init_connection()
        self.update_tree()

    def init_attrs(self):
        pass

    def init_properties(self):
        # 设置无边框
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Popup)
        self.setFixedSize(250,350)
        self.setObjectName("LSAttrTypeSearchWidget")
        self.main_layout.setContentsMargins(2,2,2,2)
        self.search_label.setFixedSize(12, 12)
        self.search_label.setScaledContents(True)
        self.search_label.setPixmap(LSIcons.search_svg)
        self.search_label.setFixedSize(12, 12)
        self.search_label.setScaledContents(True)
        self.search_label.setPixmap(LSIcons.search_svg)
        self.search_layout.setContentsMargins(6, 3, 3, 3)
        self.search_layout.setSpacing(5)

        self.search_widget.setObjectName("search_widget")
        self.search_lineedit.setObjectName("search_line")
        self.tree_widget.setObjectName("tree_widget")

        self.tree_widget.setHeaderHidden(True)


    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.search_widget = _SearchWidget()
        self.search_layout = QHBoxLayout(self.search_widget)
        self.tree_widget=_SearchTreeWidget(self)

        self.search_label = QLabel()
        self.search_lineedit = LineEdit()

        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_lineedit)

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.tree_widget)
        self.setLayout(self.main_layout)


    def init_style(self):
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        self.search_lineedit.textChanged.connect(self.search)

    def init_class_types(self):
        self.class_types_item= QTreeWidgetItem(self.tree_widget)
        self.class_types_item.setText(TreeColumn.Zero, "Class Types")
        self.tree_widget.addTopLevelItem(self.class_types_item)
        cache=set()
        for identifier,class_type in LSIdentifierData.class_types().items():
            class_id = identifier.split(LSAstIdentifierSplitter.ClassSplitter)[0]
            if class_id in cache:
                continue
            cache.add(class_id)
            class_type_item=ClassTypeTreeItem(identifier,class_type, self.class_types_item)
            self.class_types_item.addChild(class_type_item)

    def init_builtin_types(self):
        for value in LSPinAttrType.valid_values():
            attr_item = BuiltinAttrTypeTreeItem(value, )
            self.tree_widget.addTopLevelItem(attr_item)

    def update_tree(self):
        self.tree_widget.clear()
        self.init_builtin_types()
        self.init_class_types()
        self.tree_widget.expandAll()

    def search(self,text):
        iterator = QTreeWidgetItemIterator(self.tree_widget)
        show_items = []
        while iterator.value():
            item = iterator.value()
            if text.lower() in item.text(TreeColumn.Zero).lower():
                show_items.append(item)
            item.setHidden(True)
            iterator += 1  # 移动到下一个项

        for item in show_items:
            item.setHidden(False)

            item_parent = item.parent()
            while item_parent:
                item_parent.setHidden(False)
                item_parent = item_parent.parent()

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


if __name__ == '__main__':
    app=QApplication()
    window=LSAttrTypeSearchWidget()
    window.show()
    app.exec_()
