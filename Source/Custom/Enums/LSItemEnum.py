from Source.Common.Meta import LSNameMeta, LSNameField


class LSNodeItemSourceType(LSNameMeta):
    Builtin = LSNameField()
    UserDefined = LSNameField()
    Undefined = LSNameField()


class LSNodeItemType:
    Undefined = "Undefined"
    Stubs = "Stubs"
    Plugins = "Plugins"
    ClassMagicMethod = "ClassMagicMethod"
    PureFunc = "Pure"
    Event = "Event"
    Operator = "Operator"
    Control = "Control"
    Variable = "Variable"

class LSPropertyType(LSNameMeta):
    Get=LSNameField()
    Set=LSNameField()

class LSNodeSourceType(LSNameMeta):
    Undefined=LSNameField()
    Ast=LSNameField()
    Plugins=LSNameField()
    Builtin=LSNameField()
    Variable=LSNameField()