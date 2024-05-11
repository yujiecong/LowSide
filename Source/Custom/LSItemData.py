import dataclasses

from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSNodeSourceType
from Source.Custom.LSAstData import LSAstReturnData, LSAstFuncType


@dataclasses.dataclass
class LSRawData:
    title: str = ""
    node_type: LSNodeItemType = LSNodeItemType.Stubs
    instance_type: str = ""
    source:str = LSNodeSourceType.Undefined
    func_name:str= ""

@dataclasses.dataclass
class LSRawAstItemData(LSRawData):
    """
    由ast解析出来的原始数据
    """
    args_info: dict[str,str] = dataclasses.field(default_factory=dict)
    return_info: LSAstReturnData = dataclasses.field(default_factory=LSAstReturnData)
    func_type:LSAstFuncType=LSAstFuncType.NormalMethod
    # extra:dict=dataclasses.field(default_factory=dict)
    
@dataclasses.dataclass
class LSRawClassMethodData(LSRawAstItemData):
    class_name:str=""


@dataclasses.dataclass
class LSRawVariableData(LSRawData):
    attr_type: str = ""
    attr_name: str = ""
    name: str = ""

