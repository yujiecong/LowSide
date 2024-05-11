import dataclasses

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Widgets.Common.LSAttrTypeIcon import LSAttrTypeIcon
from Source.Widgets.LSAttrTypeSearchWidget import LSAttrTypeSearchWidget

@dataclasses.dataclass
class Data:
    name:str
    type:str

class LSAttrTypeComboBox(QComboBox):
    clicked_type=Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaxVisibleItems(20)
        self.attr_widget:QWidget=None
        self.init_values()

        "设置"
    def init_values(self):
        # 怎么处理相同的名字
        self.idx_2_data = {}
        idx=0
        for value in LSPinAttrType.valid_values():
            self.addItem(LSAttrTypeIcon(value), value)
            self.idx_2_data[idx] = Data(name=value,type=value)
            idx+=1

        for identifier,attr_name in LSIdentifierData.class_types().items():
            self.addItem(LSAttrTypeIcon(LSPinAttrType.user_class), attr_name)
            self.idx_2_data[idx] = Data(name=attr_name,type=LSPinAttrType.user_class)
            idx+=1


    def activate_item(self,attr_type):
        self.setCurrentText(attr_type)
        self.clicked_type.emit()

    def get_current_attr_type(self):
        return self.idx_2_data[self.currentIndex()].type

    def get_current_attr_name(self):
        return self.idx_2_data[self.currentIndex()].name


    def showPopup(self):
        self.attr_widget=LSAttrTypeSearchWidget()
        self.attr_widget.show()
        self.attr_widget.move(self.mapToGlobal(QPoint(0, self.height())))
        self.attr_widget.tree_widget.clicked_item.connect(self.activate_item)

    # 重写下拉框关闭时的事件处理
    def hidePopup(self):
        if self.attr_widget:
            try:
                self.attr_widget.deleteLater()
                "关闭程序时已经销毁 就不理了"
            except RuntimeError:
                pass

if __name__ == '__main__':
    app=QApplication()
    window=LSAttrTypeComboBox()
    window.show()
    app.exec_()
