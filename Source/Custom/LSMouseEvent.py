from PySide2.QtGui import QMouseEvent


class LSMouseEvent(QMouseEvent):
    def __init__(self,is_ignored, *args,**kwargs):
        super(LSMouseEvent, self).__init__(*args, **kwargs)
        self._is_ignored = is_ignored

    @property
    def is_ignored(self):
        return self._is_ignored

    @is_ignored.setter
    def is_ignored(self, value):
        self._is_ignored = value