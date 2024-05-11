import dataclasses

from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Common.Meta import LSNameMeta, LSNameField


class LSAstData:
    pass



class LSAstIdentifierSplitter:
    IdentifierSplitter = "/"
    ClassSplitter = "."


@dataclasses.dataclass
class LSAstReturnData:
    return_names: list = dataclasses.field(default_factory=list)
    attr_type: str = LSPinAttrType.null


class LSAstFuncType(LSNameMeta):
    ClassMethod = LSNameField()
    StaticMethod = LSNameField()
    NormalMethod = LSNameField()


class LSAstCodeFragmentName:
    body = "body"
    orelse = "orelse"
    last = "last"
