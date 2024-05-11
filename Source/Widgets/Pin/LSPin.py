import typing
import uuid

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source import Globs
from Source.Common.Enums import PropertyState
from Source.Custom.Enums.LSPinEnum import PinType, PinFlow, LSPinAttrType
from Source.Custom.LSColor import PinAttrTypeExternalColor, PinAttrTypeInternalColor
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject
from Source.Widgets.Common.LSPathItem import LSPathItem
from Source.Widgets.LSPinWrapper import LSPinWrapper
from Source.Widgets.PinIconWidget.LSPinIconWidget import LSPinIconWidget

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


# ItemType = TypeVar("ItemType", bound="LSNodeItem")


class LSPin(QFrame, LSObject):
    LMousePressPos = QPointF(0, 0)
    LMouseIsPressed: bool = False

    lineReleased_signal = Signal(object, object)
    lineMoved_signal = Signal(object, object)

    destroyed_signal = Signal()
    doubleClicked_signal = Signal()
    disabled_color = PinAttrTypeExternalColor(PropertyState.Disabled)

    @classmethod
    def deserialize(cls,new_item_instance, wrapper: "LSPin"):
        new_pin=cls(flow=wrapper.flow,
                    attr_type=wrapper.attr_type,
                    title=wrapper.title,
                    uuid_=wrapper.uuid_)
        new_pin.node=new_item_instance
        return new_pin

    def finished_init(self):
        pass

    def __init__(self, flow: PinFlow,
                 attr_type=LSPinAttrType.object,
                 title="", uuid_=None, is_enabled=True):
        self.node = None
        self._type = PinType.NoneType
        self.row = -1
        with LSObject.Record(self, LSObject.RecordType.Duplicate):
            self.is_enabled = is_enabled

        with LSObject.Record(self, LSObject.RecordType.Duplicate | LSObject.RecordType.Serialize):
            self.title = title
            self.attr_type: LSPinAttrType = attr_type
            self.flow: PinFlow = flow


        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.uuid_ = uuid_ or str(uuid.uuid4())
            self.class_name = f"{self.__class__.__name__}"
        super().__init__()
        LSObject.__init__(self)

    def init_ui(self):
        super().init_ui()
        self.wrapper = LSPinWrapper(self)

    def init_attrs(self):
        super().init_attrs()
        self.from_: typing.List["LSFlowPin"] = []
        self.out_lines: typing.List[LSPathItem] = []
        self.in_lines: typing.List[LSPathItem] = []
        self.is_in_connected = False
        self.is_out_connected = False
        # with LSObject.RecordConverionKeysContext(self):
        self.to_: typing.List["LSFlowPin"] = []

    def init_style(self):
        super().init_style()
        self.setStyleSheet(qss)
        # self.setStyleSheet("background-color:red;")

    def init_connection(self):
        super().init_connection()

    def get_flow(self) -> PinFlow:
        return self.flow

    def get_type(self) -> PinType:
        raise NotImplementedError

    def set_row(self, row):
        self.row = row

    def update_connected_line(self):
        pass

    def update_connection_style(self):
        pass
    def duplicate(self, dup_node, *args, **kwargs):
        ins = type(self)(*args, **kwargs)
        ins.node = dup_node
        return ins

    def duplicate_finished(self, origin_pin):
        """
        用于在复制完成后,将origin_pin的属性复制到当前pin
        :param origin_pin:
        :return:
        """
        pass


    def __repr__(self):
        return f"{self.__class__.__name__}({self.row},{self.flow},{self.title})"


if __name__ == '__main__':
    app = QApplication()
    window = LSPin()
    window.show()
    app.exec_()
