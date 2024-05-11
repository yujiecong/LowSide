
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.DataClass import LSVariableDetailData
from Source.Common.Enums import LSDetailSource
from Source.Common.Func import OS
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSObject import LSObject
from Source.Widgets.Common.LSAttrTypeComboBox import LSAttrTypeComboBox


class Column:
    Zero = 0
    One = 1
    Two = 2

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()



class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent:QTreeWidget, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.tree=parent
        self.root_item=parent.invisibleRootItem()


    def paint(self, painter, option, index):
        super(BorderItemDelegate, self).paint(painter, option, index)
        item=self.tree.itemFromIndex(index)
        rect = option.rect
        lines=[]
        lines.append(QLine(rect.topRight(), rect.bottomRight()))
        if item.parent() is None:
            lines.append(QLine(rect.topLeft(), rect.topRight()))
        lines.append(QLine(rect.bottomLeft(), rect.bottomRight()))
        pen=QPen(QColor(26, 26, 26))
        pen.setWidthF(0.6)
        painter.setPen(pen)
        painter.drawLines(lines)

        painter.restore()


            
class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.item_font=QFont("微软雅黑", 7)
        self.setFont(Column.Zero, self.item_font)
        self.setTextColor(Column.Zero, QColor(174, 174, 174))



class TopTreeWidgetItem(QTreeWidgetItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.var_title_item_font=QFont("微软雅黑", 7,weight=QFont.Weight.Bold)
        self.setTextColor(Column.Zero, QColor(200, 200, 200))
        self.setFont(Column.Zero, self.var_title_item_font)
        self.setBackgroundColor(Column.Zero, QColor(47, 47, 47))
        self.setBackgroundColor(Column.One, QColor(47, 47, 47))
        self.setBackgroundColor(Column.Two, QColor(47, 47, 47))

class LSDetailTreeWidget(QTreeWidget,LSObject):
    changeProperty_signal=Signal(LSVariableDetailData, LSVariableDetailData)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "如果有父了 就不要调用了"
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
        self.setItemDelegate(BorderItemDelegate(self, Qt.UserRole))

        
    def init_ui(self):
        super().init_ui()
        self.header().hide()
        self.clear()
        self.setHeaderLabels(['列1', '列2','列2'])
        self.header().setSectionResizeMode(Column.One, QHeaderView.Stretch)
        self.header().setSectionResizeMode(Column.Two, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Column.Zero, QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.expandAll()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def update_detail(self,detail_source:str,detail_data:LSVariableDetailData):
        self.clear()
        if detail_data is None:
            return
        self.detail_source=detail_source
        self.detail_data:LSVariableDetailData=detail_data
        if detail_source==LSDetailSource.Variable:
            self.update_variable_details()
        elif detail_source==LSDetailSource.Null:
            pass
        self.expandAll()

    def update_variable_details(self):
        self._update_variable_detail()
        self.top_var_value_item = TopTreeWidgetItem(self.invisibleRootItem())
        self.top_var_value_item.setText(Column.Zero, "默认值")
        self._update_value_detail()

    def _update_variable_detail(self):
        self.top_var_variable_item = TopTreeWidgetItem(self.invisibleRootItem())
        self.top_var_variable_item.setText(Column.Zero, "变量")
        placeholder_widget = QWidget()
        placeholder_widget.setStyleSheet("background-color:transparent;")
        placeholder_widget.setFixedSize(1, 23)
        self.setItemWidget(self.top_var_variable_item, Column.Two, placeholder_widget)
        self.addTopLevelItem(self.top_var_variable_item)
        variable_name_item = TreeWidgetItem(self.top_var_variable_item)
        variable_name_item.setText(Column.Zero, "变量名")
        self.variable_name_lineedit = QLineEdit()
        self.variable_name_lineedit.setText(self.detail_data.variable_name)
        self.variable_name_lineedit.editingFinished.connect(self._change_property)
        self.setItemWidget(variable_name_item, Column.One, self.variable_name_lineedit)

        self.top_var_variable_item.addChild(variable_name_item)
        variable_type_item = TreeWidgetItem(self.top_var_variable_item)
        variable_type_item.setText(Column.Zero, "变量类型")
        self.top_var_variable_item.addChild(variable_type_item)

        self.variable_type_comboBox = LSAttrTypeComboBox()
        self.variable_type_comboBox.setCurrentText(self.detail_data.variable_attr_name)

        self.variable_type_comboBox.clicked_type.connect(self._change_variable_type)

        self.setItemWidget(variable_type_item, Column.One, self.variable_type_comboBox)

    def _update_value_detail(self,is_default=False):
        for i in range(self.top_var_value_item.childCount()):
            self.top_var_value_item.removeChild(self.top_var_value_item.child(0))

        variable_name_item = TreeWidgetItem(self.top_var_value_item)
        variable_name_item.setText(Column.Zero, self.detail_data.variable_name)

        if self.detail_data.variable_attr_type in {LSPinAttrType.str, LSPinAttrType.int, LSPinAttrType.float}:
            self.variable_value_widget = QLineEdit()
            if not is_default:
                self.variable_value_widget.setText(str(self.detail_data.variable_value))

            self.variable_value_widget.editingFinished.connect(self._change_property)

        elif self.detail_data.variable_attr_type==LSPinAttrType.bool:
            self.variable_value_widget = QCheckBox()
            if not is_default:
                self.variable_value_widget.setChecked(self.detail_data.variable_value)
            else:
                self.variable_value_widget.setChecked(True)

            self.variable_value_widget.clicked.connect(self._change_property)
        else:
            self.variable_value_widget = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(3,0,0,0)
            layout.addWidget(QLabel("None"))
            self.variable_value_widget.setLayout(layout)
        self.setItemWidget(variable_name_item, Column.One, self.variable_value_widget)

    def _get_variable_detail_data(self):
        variable_name=self.variable_name_lineedit.text()
        variable_attr_type=self.variable_type_comboBox.currentText()

        if self.detail_data.variable_attr_type==LSPinAttrType.str:
            variable_value=self.variable_value_widget.text()
        elif self.detail_data.variable_attr_type==LSPinAttrType.float:
            variable_value=float(self.variable_value_widget.text())
        elif self.detail_data.variable_attr_type==LSPinAttrType.int:
            variable_value=int(self.variable_value_widget.text())
        elif self.detail_data.variable_attr_type==LSPinAttrType.bool:
            variable_value=self.variable_value_widget.isChecked()
        else:
            variable_value=None
        return LSVariableDetailData(variable_name=variable_name,
                                    variable_attr_type=variable_attr_type,
                                    variable_attr_name=self.detail_data.variable_attr_name,
                                    variable_value=variable_value)

    def _change_variable_type(self):
        self.detail_data.variable_attr_type=self.variable_type_comboBox.get_current_attr_type()
        self.detail_data.variable_attr_name=self.variable_type_comboBox.get_current_attr_name()
        self._update_value_detail(is_default=True)
        self._change_property()

    def _change_property(self):
        if self.detail_source==LSDetailSource.Variable:
            current_detail_data = self._get_variable_detail_data()
            self.changeProperty_signal.emit(self.detail_data, current_detail_data)
            self.detail_data=current_detail_data

        else:
            raise Exception("未知的detail_source")





if __name__ == '__main__':
    app=QApplication()
    window=LSDetailTreeWidget()
    window.show()
    app.exec_()
