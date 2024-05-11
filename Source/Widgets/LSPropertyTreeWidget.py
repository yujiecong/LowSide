import ast
import itertools
import typing

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.DataClass import LSVariableDetailData
from Source.Common.Enums import LSMimeSource, LSDetailSource
from Source.Common.Obj import LSDictWrapper
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Common.Func import OS

from Source.Custom.Enums.LSItemEnum import LSPropertyType, LSNodeSourceType
from Source.Custom.LSCommand import LSAddPropertyCommand
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSIcons import LSIcons
from Source.Custom.LSMimeData import LSMimeData
from Source.Custom.LSObject import LSObject
from Source.Widgets.Common.LSAttrTypeComboBox import LSAttrTypeComboBox
from Source.Widgets.NodeItem.LSSetVariableNodeItem import LSSetVariableNodeItem
from Source.Widgets.NodeItem.LSVariableNodeItem import LSVariableNodeItem
from Source.Widgets.NodeItem.LSGetVariableNodeItem import LSGetVariableNodeItem


class Column:
    Zero = 0
    One = 1
    Two = 2


qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class VariableTreeItem(QTreeWidgetItem):
    def __init__(self, detail:LSVariableDetailData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail=detail
        self.identifier = LSIdentifierData.variable_path(detail.variable_name)




class LSPropertyTreeWidget(QTreeWidget, LSObject):
    clickedVariable_signal = Signal(str, object)

    def __init__(self, *args, **kwargs):
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.variable_data: typing.List[LSVariableDetailData] = []

        super().__init__(*args, **kwargs)
        LSObject.__init__(self)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.setWindowFlag(Qt.WindowType.Widget)
        "icon大小"
        self.setIconSize(QSize(12, 12))
        "branch大小"
        self.setIndentation(14)
        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.add_variable()
        # self.add_variable()
        # self.add_variable()

        self.expandAll()

    def init_ui(self):
        super().init_ui()
        self.header().hide()
        self.clear()
        self.setHeaderLabels(['列1', '列2', '列2'])
        self.header().setSectionResizeMode(Column.One, QHeaderView.Stretch)
        self.header().setSectionResizeMode(Column.Two, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Column.Zero, QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)

        self.menu = QMenu(self)
        self.remove_action = self.menu.addAction("删除")
        self.remove_action.triggered.connect(self.remove_selected)

    def init_variable_property(self):
        self.top_variable_item = QTreeWidgetItem()
        self.top_variable_item.setText(Column.Zero, "变量")
        self.top_variable_item.setBackgroundColor(Column.Zero, QColor(47, 47, 47))
        self.top_variable_item.setBackgroundColor(Column.One, QColor(47, 47, 47))
        self.top_variable_item.setBackgroundColor(Column.Two, QColor(47, 47, 47))
        self.addTopLevelItem(self.top_variable_item)
        self.add_variable_widget = QWidget()
        self.add_variable_widget.setObjectName("add_variable_widget")
        self.add_variable_widget.setStyleSheet(
            "#add_variable_widget{background-color:transparent;}QPushButton{border:none;}")
        self.add_variable_layout = QHBoxLayout(self.add_variable_widget)
        self.add_variable_layout.setContentsMargins(4, 4, 4, 4)
        self.add_variable_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.add_variable_button = QPushButton()
        self.add_variable_button.setFixedSize(15, 15)
        self.add_variable_button.setStyleSheet("QPushButton{border-image:url(%s);}" % (LSIcons.add_png))
        self.add_variable_button.clicked.connect(lambda: [self.add_variable(), self.update_variables_info()])
        self.add_variable_layout.addWidget(self.add_variable_button)
        self.setItemWidget(self.top_variable_item, Column.Two, self.add_variable_widget)

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()
        self.itemDoubleClicked.connect(self.double_clicked)
        # self.clicked.connect(self.clicked_item)

    def double_clicked(self, item, column):
        # 开启编辑模式
        self.edit_item(item)

    def edit_item(self, item):
        if item is not None:
            # 获取项目的当前文本
            current_text = item.text(Column.Zero)

            # 创建一个文本编辑框并设置当前文本
            line_edit = QLineEdit(self)
            line_edit.setText(current_text)

            # 将文本编辑框插入到项目中
            self.setItemWidget(item, Column.Zero, line_edit)

            # 设置文本编辑框的焦点
            line_edit.setFocus()

            # 当编辑完成时保存修改
            line_edit.editingFinished.connect(lambda: self.save_edited_text(item, line_edit))

    def save_edited_text(self, item: VariableTreeItem, line_edit):
        # 获取编辑后的文本
        edited_text = line_edit.text()

        # 设置项目的文本为编辑后的文本
        item.setText(0, edited_text)

        # 移除文本编辑框
        self.removeItemWidget(item, 0)
        self.update_variables_info()


    def update_property(self, data: typing.Union[dict,None]):
        self.clear()
        LSIdentifierData.unregister_all_variables()
        self.init_variable_property()
        if data:
            with Globs.DisableRecordCommandContext():
                wrapper_data: "LSPropertyTreeWidget" = LSDictWrapper(data)
                for var_data in wrapper_data.variable_data:
                    var_wrapper_data: LSVariableDetailData = LSDictWrapper(var_data)
                    self.add_variable(var_wrapper_data)
        self.update_variables_info(is_update_detail=False)
        self.expandAll()

    def add_variable(self,detail:LSVariableDetailData=None):
        if detail is None:
            default_name = "new_var"
            new_name = default_name
            idx = 1
            while LSVariableNodeItem.is_exist(new_name):
                new_name = f"{default_name}{idx}"
                idx += 1
        else:
            new_name = detail.variable_name

        attr_type_values = LSPinAttrType.valid_values()
        if detail is None:
            attr_type = attr_type_values[0]
        else:
            attr_type=detail.variable_attr_type

        if detail is None:
            attr_name = attr_type
        else:
            attr_name=detail.variable_attr_name

        LSGetVariableNodeItem.register(new_name, attr_type,attr_name)
        LSSetVariableNodeItem.register(new_name, attr_type,attr_name)
        if detail is None:
            value = self.get_default_value(attr_type)
        else:
            value=detail.variable_value

        variable_item = VariableTreeItem(LSVariableDetailData(variable_name=new_name,
                                                              variable_attr_type=attr_type,
                                                              variable_attr_name=attr_type,
                                                              variable_value=value),
                                         self.top_variable_item)
        variable_item.setText(Column.Zero, new_name)
        if self.view:
            self.view.undo_stack.push(LSAddPropertyCommand(variable_item, self))

        comboBox = LSAttrTypeComboBox()
        comboBox.setCurrentText(attr_name)
        comboBox.clicked_type.connect(self.change_type)

        self.setItemWidget(variable_item, Column.One, comboBox)

    def get_default_value(self, attr_type):
        if attr_type == LSPinAttrType.bool:
            default_value = True
        elif attr_type == LSPinAttrType.int:
            default_value = 0
        elif attr_type == LSPinAttrType.float:
            default_value = 0.0
        elif attr_type == LSPinAttrType.str:
            default_value = ""
        else:
            default_value = None
        return default_value

    def get_variable_items(self, variable_name):
        if not self.view:
            return []
        items = list(itertools.chain(
            self.view.find_item_by_identifier(
                LSIdentifierData.variable_property_path(variable_name, LSPropertyType.Get)),
            self.view.find_item_by_identifier(
                LSIdentifierData.variable_property_path(variable_name, LSPropertyType.Set)),
        ))
        return items

    def remove_selected(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            self.remove_variable(item)
        self.update_variables_info()
        self.clear_selection()

    def remove_variable(self, item: VariableTreeItem):
        items = self.get_variable_items(item.detail.variable_name)
        if items:
            btn = QMessageBox.warning(self, "警告", f"有节点正在使用该变量({item.detail.variable_name}),你真的想删除吗?",
                                      buttons=QMessageBox.Yes | QMessageBox.No)
            if btn == QMessageBox.No:
                return

        LSGetVariableNodeItem.unregister(item.detail.variable_name)
        LSSetVariableNodeItem.unregister(item.detail.variable_name)
        item_parent = item.parent()
        item_parent.removeChild(item)
        self.view.remove_items(items)

    def change_type(self):
        "如果改了类型 那么默认值也要改"
        comboBox: LSAttrTypeComboBox = self.sender()
        comboBox_item:VariableTreeItem=None
        for idx in range(self.top_variable_item.childCount()):
            child_item=self.top_variable_item.child(idx)
            item_widget=self.itemWidget(child_item,Column.One)
            if item_widget is comboBox:
                comboBox_item=child_item
                break
        if comboBox_item:
            comboBox_item.detail.variable_value=self.get_default_value(comboBox.get_current_attr_type())
            self.update_variables_info()

    def update_property_detail(self):
        for var_item_idx in range(self.top_variable_item.childCount()):
            item: VariableTreeItem = self.top_variable_item.child(var_item_idx)
            self.clickedVariable_signal.emit(LSDetailSource.Variable, item.detail)


    def update_variables_info(self,is_update_detail=True):
        self.variable_data.clear()
        self.variable_2_item = {}

        for var_item_idx in range(self.top_variable_item.childCount()):
            item: VariableTreeItem = self.top_variable_item.child(var_item_idx)
            old_var_name=item.detail.variable_name
            LSGetVariableNodeItem.unregister(item.detail.variable_name)
            LSSetVariableNodeItem.unregister(item.detail.variable_name)
            new_name = item.text(Column.Zero)
            item.detail.variable_name = new_name
            variable_comboBox: LSAttrTypeComboBox = self.itemWidget(item, Column.One)
            new_attr_type = variable_comboBox.get_current_attr_type()
            new_attr_name = variable_comboBox.get_current_attr_name()
            item.detail.variable_attr_type = new_attr_type
            item.detail.variable_attr_name = new_attr_name
            self.variable_data.append(item.detail)

            LSGetVariableNodeItem.register(new_name, new_attr_type,new_attr_name)
            LSSetVariableNodeItem.register(new_name, new_attr_type,new_attr_name)
            item.identifier = LSIdentifierData.variable_path(new_name)
            "如果已经存在了  那么要通知所有的变量改名字..."
            self.variable_2_item[new_name] = item
            items = self.get_variable_items(old_var_name)
            for existed_item in items:
                existed_item: typing.Union[LSGetVariableNodeItem, LSSetVariableNodeItem]
                if existed_item.name != new_name:
                    existed_item.set_variable(new_name)
                if existed_item.attr_type != new_attr_type:
                    "因为一个attr_type可以代表多种不同的 类 类型 所以要.知道当前到底是啥attr"
                    existed_item.set_attr(new_attr_type,new_attr_name)

        if is_update_detail:
            self.update_property_detail()

    def change_variable(self, old_detail_data: LSVariableDetailData, new_detail_data: LSVariableDetailData):
        item = self.variable_2_item[old_detail_data.variable_name]
        item.setText(Column.Zero, new_detail_data.variable_name)
        attr_type_comboBox: QComboBox = self.itemWidget(item, Column.One)
        attr_type_comboBox.setCurrentText(new_detail_data.variable_attr_name)
        item.detail.variable_value = new_detail_data.variable_value

        self.update_variables_info(is_update_detail=False)

    def generate_code(self):
        assign_code = [ast.Constant(value="生成变量定义..")]
        for variable_data in self.variable_data:
            assign_code.append(ast.AnnAssign(target=ast.Name(id=variable_data.variable_name, ctx=ast.Store()),
                                             annotation=ast.Name(id=variable_data.variable_attr_name, ctx=ast.Load()),
                                             value=ast.Constant(value=variable_data.variable_value), simple=1))
        return assign_code

    def clear_selection(self):
        self.clickedVariable_signal.emit(LSDetailSource.Variable, None)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        selected_items = self.selectedItems()

        if event.button() == Qt.MouseButton.RightButton:
            if selected_items:
                self.menu.exec_(QCursor.pos())
        elif event.button() == Qt.MouseButton.LeftButton:
            if selected_items:
                if self.itemAt(event.pos()) is None:
                    self.clear_selection()
                else:

                    item: VariableTreeItem = selected_items[0]
                    if not selected_items or not isinstance(item,VariableTreeItem):
                        self.clear_selection()
                    else:
                        self.clickedVariable_signal.emit(LSDetailSource.Variable, item.detail)
            else:
                self.clear_selection()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        selected_items = self.selectedItems()
        if selected_items:
            item: VariableTreeItem = selected_items[0]
            if isinstance(item,VariableTreeItem):
                drag = QDrag(self)
                mime_data = LSMimeData(item.identifier, source=LSMimeSource.Property)
                drag.setMimeData(mime_data)
                drag.exec_(Qt.CopyAction | Qt.MoveAction)



if __name__ == '__main__':
    app = QApplication()
    window = LSPropertyTreeWidget()
    window.show()
    app.exec_()
