import abc

from PySide2.QtCore import *


class LSNameField(object):
    def __init__(self, ):
        self.name = None
        self.internalName = None

    def __get__(self, instance, instance_type):
        if instance is None: return self.name
        return getattr(instance, self.name, '')

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class LSFieldMeta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, LSNameField):
                value.name = key
                value.internalName = "_" + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


class LSNameMeta(metaclass=LSFieldMeta):
    pass

