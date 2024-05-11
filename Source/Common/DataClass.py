import dataclasses
import pprint
import typing
from typing import List

from PySide2.QtCore import QPoint

from Source.Common.Enums import LSMimeSource


@dataclasses.dataclass
class LSPinConnectInfo:
    node_uuid: str
    to_node_uuid: str
    pin_uuid: str
    to_pin_uuid: str


@dataclasses.dataclass
class LSSubPinInfo:
    sub_pins_uuid: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class LSNodeDetailData:
    return_name:str

@dataclasses.dataclass
class LSVariableDetailData:
    variable_name:str
    variable_attr_type:str
    variable_attr_name:str
    variable_value:typing.Any
