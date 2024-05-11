from Source.Common.Meta import LSNameMeta, LSNameField


class PropertyState(LSNameMeta):
    Normal = LSNameField()
    Hover = LSNameField()
    Selected = LSNameField()
    Disabled = LSNameField()


class PropertyName(LSNameMeta):
    State = LSNameField()


class ItemZValue:
    Background = -1
    Line = 0
    CoreNode = 1
    PromptLabel = 2
    QuickSearchWidget = 2

class LSMimeSource(LSNameMeta):
    Property=LSNameField()
    Search=LSNameField()

class LSDetailSource(LSNameMeta):
    Variable=LSNameField()
    Node=LSNameField()
    Null=LSNameField()

class LSCreateItemMode(LSNameMeta):
    Identifier=LSNameField()
    Serial=LSNameField()
    Duplicate=LSNameField()
    Default=LSNameField()

