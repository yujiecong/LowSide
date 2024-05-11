
from Source import Globs
from PySide2.QtWidgets import *

from Source.Common import Func
from Source.Common.Func import OS
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSPropertyType
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSItemData import LSRawVariableData
from Source.Custom.LSObject import LSObject
from Source.Widgets.NodeItem.LSNodeItem import LSNodeItem

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class LSVariableNodeItem(LSNodeItem):

    def duplicate(self, *args, **kwargs) -> "LSVariableNodeItem":
        ins:LSVariableNodeItem=super().duplicate(*args, **kwargs)
        ins.set_attr(self.attr_type, self.attr_name)
        return ins

    @staticmethod
    def is_exist(variable_name: str):
        return (LSIdentifierData.variable_property_path(variable_name, LSPropertyType.Get)
                in LSIdentifierData.FromVariable) or (
                LSIdentifierData.variable_property_path(variable_name, LSPropertyType.Set)
                in LSIdentifierData.FromVariable)

    # noinspection PyCallingNonCallable
    @staticmethod
    def _create_curry_instance(constructor:"LSVariableNodeItem",ast_data:LSRawVariableData,create_mode):
        return constructor(
            create_mode=create_mode,
            name=ast_data.name,
            attr_type=ast_data.attr_type,
            attr_name=ast_data.attr_name,
        )

    def __init__(self, name="new_var", attr_type=LSPinAttrType.object,attr_name=LSPinAttrType.object, *args, **kwargs):
        with LSObject.Record(self, LSObject.RecordType.Duplicate | LSObject.RecordType.Serialize):
            "如果在这加了参数 记得修改 curry instance"
            self.attr_type = attr_type
            self.attr_name = attr_name
            self.name = name
        super().__init__(*args, **kwargs)


    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()

    def set_attr(self, attr_type, attr_name):
        pass


if __name__ == '__main__':
    app=QApplication()
    window=LSVariableNodeItem()
    window.show()
    app.exec_()
