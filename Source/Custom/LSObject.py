import collections
import contextlib
import dataclasses
import pprint
import types
import typing
from typing import Union

from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from Source.Common import Func
from Source.Common.Logger import ls_print
from Source.Common.Util import Util

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore



ignore_methods = set()

for ever in dir(QtWidgets):
    ignore_methods |= set(dir(getattr(QtWidgets, ever)))

for ever in dir(QtGui):
    ignore_methods |= set(dir(getattr(QtGui, ever)))

for ever in dir(QtCore):
    ignore_methods |= set(dir(getattr(QtCore, ever)))





class LSObjectMeta(type(QObject), type):
    registered_classes = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        # 注册类和其对应的反序列化方法
        LSObjectMeta.registered_classes[name] = cls


class LSObject(metaclass=LSObjectMeta):
    ConstructorKeywords = collections.defaultdict(set)
    SerializeKeywords = collections.defaultdict(set)

    __NODE_ITEM_TYPE__=None
    __LS_TYPE_NAME__=None

    class RecordType:
        Duplicate = 1
        Serialize = 2

    def serialize(self):
        data = {}

        for key in self.serialize_keywords:
            attr = getattr(self, key)
            if dataclasses.is_dataclass(attr):
                # value=dataclasses.asdict(attr)
                value=Func.parse_dataclass(attr)
            elif isinstance(attr, list):
                value = [Func.parse_dataclass(item) for item in attr]
            elif callable(attr):
                result=attr()
                value=Func.parse_dataclass(result)

                # if dataclasses.is_dataclass(result):
                #     value=dataclasses.asdict(result)
                # else:
                #     value=result
            else:
                value = attr
            data[key] = value

        return data
    @classmethod
    def deserialize(cls,data):
        raise NotImplementedError

    def __init__(self):
        self.view: Union[QGraphicsView] = None

        self.init_attrs()
        self.init_ui()
        self.init_connection()
        self.init_style()
        self.init_properties()

        # all_methods = set(dir(self))
        # all_methods -= ignore_methods
        # print(all_methods)
        # "生成Abstract类的方法"
        # for method in all_methods:
        #     if not method.startswith('__') and not method.endswith('__'):
        #         attr = getattr(self, method)
        #         if isinstance(attr, (types.MethodType, property)):
        #             pass
                    # if attr.__name__ in IgnoreMethods or attr.__qualname__ in IgnoreMethods:
                    #     continue
                    # setattr(self, method, Util.log(attr))

    def init_attrs(self):
        pass

    def init_properties(self):
        pass

    def init_ui(self):
        pass

    def init_style(self):
        pass

    def init_connection(self):
        pass

    def destruct(self):
        self.view=None

    def set_view(self, view):
        if not issubclass(type(view),QGraphicsView):
            raise ValueError("view must be a QGraphicsView")
        if self.view:
            # return
            raise ValueError("view already set")
        self.view: Union[QGraphicsView] = view

    def update_view(self,view):
        self.view: Union[QGraphicsView] = view


    @staticmethod
    @contextlib.contextmanager
    def Record(instance, record_type):
        # origin_dict:dict=instance.__dict__
        # instance.__dict__={}
        locals1 = list(instance.__dict__.keys())
        yield
        locals2 = list(instance.__dict__.keys())
        instance.__class__: LSObject
        diff = set(locals2) - set(locals1)
        # origin_dict.update(instance.__dict__)
        # instance.__dict__=origin_dict
        if record_type & LSObject.RecordType.Duplicate:
            instance.__class__.ConstructorKeywords[instance.__class__.__name__] |= diff
        if record_type & LSObject.RecordType.Serialize:
            instance.__class__.SerializeKeywords[instance.__class__.__name__] |= diff

    @property
    def constructor_keywords(self):
        return sorted(list(self.ConstructorKeywords[self.__class__.__name__]))

    @property
    def serialize_keywords(self):
        return sorted(list(self.SerializeKeywords[self.__class__.__name__]))



    @staticmethod
    def recursive_to_data(obj: "LSObject"):
        if not isinstance(obj, (int, float, str, bool, type(None), dict, list)):
            # if isinstance(obj, (LSObject)):
            # if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.serialize()
        else:
            if isinstance(obj, dict):
                return {key: LSObject.recursive_to_data(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [LSObject.recursive_to_data(item) for item in obj]

        return obj


if __name__ == '__main__':
    app = QApplication()
    window = LSObject()
    window.show()
    app.exec_()
