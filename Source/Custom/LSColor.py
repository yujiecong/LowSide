from PySide2.QtGui import QColor, Qt

from Source.Common.Enums import PropertyState
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSObject import LSObject

class LSColor:
    Black = QColor(Qt.black)
    White = QColor(Qt.white)


class PinAttrTypeColor(QColor,LSObject):
    mapped = {
        LSPinAttrType.object: "244,244,244",
    }
    def __init__(self, attr_type=LSPinAttrType.object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color=self.mapped.get(attr_type, self.mapped[LSPinAttrType.object])
        self.setRgb(*map(int, color.strip().split(",")))
        self.color=[self.red(), self.green(), self.blue(), self.alpha()]

class PinLineColor(PinAttrTypeColor):
    mapped = {
        LSPinAttrType.object: "255,255,255,200",
    }


class PinAttrTypeExternalColor(PinAttrTypeColor):
    mapped = {
        LSPinAttrType.any: "129,122,122",
        LSPinAttrType.object: "0, 170, 245",
        # LSPinAttrType.bytearray: "0, 111, 101",
        LSPinAttrType.null: "244, 244, 244",
        LSPinAttrType.none: "172, 128, 229",
        LSPinAttrType.str: "255, 0, 212",
        LSPinAttrType.int: "31, 227, 175",
        LSPinAttrType.float: "56, 213, 0",
        LSPinAttrType.bool: "136,2,1",
        LSPinAttrType.list: "255, 202, 35",
        LSPinAttrType.tuple: "0, 66, 106",
        LSPinAttrType.set: "0, 175, 157",
        LSPinAttrType.user_class: "255, 202, 104",
        PropertyState.Disabled: "144,144,144,100",
    }


class PinAttrTypeInternalColor(PinAttrTypeColor):
    mapped = {
        LSPinAttrType.object: "0,0,0",
    }


class LSExternalColor:
    Default = QColor(244, 244, 244)
    Red = QColor(136, 2, 1)


class LSInternalColor:
    Default = LSColor.Black
