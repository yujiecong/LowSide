from Source.Common.Meta import LSNameMeta, LSNameField


class PinColumn:
    In = 0
    Out = 1


class PinType(LSNameMeta):
    Exec = LSNameField()
    Data = LSNameField()
    NoneType = LSNameField()


class PinFlow(LSNameMeta):
    In = LSNameField()
    Out = LSNameField()
    Both = LSNameField()
    NoneType = LSNameField()
    All = LSNameField()


class LSPinAttrType(LSNameMeta):
    null = LSNameField()
    none = LSNameField()
    any = LSNameField()
    object = LSNameField()
    str = LSNameField()
    bool = LSNameField()
    int = LSNameField()
    float = LSNameField()
    list = LSNameField()
    tuple = LSNameField()
    dict = LSNameField()
    user_class = LSNameField()
    set = LSNameField()
    # frozenset = LSNameField()
    # complex = LSNameField()
    # bytes = LSNameField()
    # bytearray = LSNameField()
    # memoryview = LSNameField()


    @staticmethod
    def _ignore_values():
        return [LSPinAttrType.user_class, LSPinAttrType.any,LSPinAttrType.null]

    @staticmethod
    def valid_values():
        values = sorted([getattr(LSPinAttrType, a) for a in dir(LSPinAttrType) if
                    not a.startswith("__") and not callable(getattr(LSPinAttrType, a))])
        for ignore_value in LSPinAttrType._ignore_values():
            values.remove(ignore_value)
        return values


class PinConnectionFlag(LSNameMeta):
    FlowError = LSNameField()
    PinTypeError = LSNameField()
    DataTypeError = LSNameField()
    AttrTypeError = LSNameField()
    CanConnect = LSNameField()
    ReplaceExecConnect = LSNameField()
    OnlyOneExecConnect = LSNameField()
    ReplaceDataConnect = LSNameField()
    IsSelfError = LSNameField()
