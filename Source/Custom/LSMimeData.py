
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common.Enums import LSMimeSource
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject


class LSMimeData(QMimeData):
    def __init__(self, identifier, pos=None, source: str = LSMimeSource.Search):
        super().__init__()
        self.identifier = identifier
        self.name = identifier[identifier.rfind("/")+1:]
        self.source = source
        self.pos = pos or QPoint()
