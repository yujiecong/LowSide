

from PySide2.QtWidgets import *

from Source.Common.Enums import ItemZValue
from Source.Custom.LSObject import LSObject
from Source.Widgets.Common.LSPromptLabel import LSPromptLabel


class LSGraphicsScene(QGraphicsScene, LSObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        LSObject.__init__(self)
        # self.setItemIndexMethod(QGraphicsScene.NoIndex)


    def init_ui(self):
        super().init_ui()
        self.prompt_label=LSPromptLabel()


    def init_properties(self):
        super().init_properties()
        proxy=self.addWidget(self.prompt_label)
        proxy.setZValue(ItemZValue.PromptLabel)
        self.prompt_label.hide()

        self.setItemIndexMethod(QGraphicsScene.NoIndex)

