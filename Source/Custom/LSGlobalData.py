import collections
import typing
from typing import *

from Source.Common import Func
from Source.Custom.LSAstData import LSAstIdentifierSplitter
from Source.Custom.LSItemData import LSRawData, LSRawVariableData, LSRawAstItemData, LSRawClassMethodData
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSPropertyType, LSNodeSourceType


class LSGlobalData:
    pass

class LSAstAttrTypeData:
    AttrType: Dict[str,str] = {}

    @staticmethod
    def register(attr_type: str, data: str):
        LSAstAttrTypeData.AttrType[attr_type] = data
    @staticmethod
    def unregister(attr_type: str):
        del LSAstAttrTypeData.AttrType[attr_type]


class LSIdentifierData:
    FromAst: Dict[str, typing.Union[LSRawAstItemData]] = {}
    FromVariable: Dict[str, typing.Union[LSRawVariableData]] = {}
    FromBuiltin: Dict[str, typing.Union[LSRawAstItemData]] = {}
    FromPlugins: Dict[str, typing.Union[LSRawAstItemData]] = {}
    Type2Identifier: Dict[str, LSRawData] = {}

    @staticmethod
    def get(identifier:str):
        if identifier in LSIdentifierData.FromAst:
            return LSIdentifierData.FromAst[identifier]
        elif identifier in LSIdentifierData.FromVariable:
            return LSIdentifierData.FromVariable[identifier]
        elif identifier in LSIdentifierData.FromBuiltin:
            return LSIdentifierData.FromBuiltin[identifier]
        elif identifier in LSIdentifierData.FromPlugins:
            return LSIdentifierData.FromPlugins[identifier]
        else:
            raise ValueError(f"identifier {identifier} not found")

    @staticmethod
    def class_types():
        id_2_type = {}
        for identifier, data in LSIdentifierData.FromAst.items():
            data:LSRawClassMethodData
            if data.node_type==LSNodeItemType.ClassMagicMethod:
                id_2_type[identifier] = data.class_name
        # sort by class name
        id_2_type = collections.OrderedDict(sorted(id_2_type.items(), key=lambda x: x[1]))
        return id_2_type

    @staticmethod
    def register(identifier: str, data: LSRawData,source:str):
        if source==LSNodeSourceType.Ast:
            LSIdentifierData.FromAst[identifier] = data
        elif source==LSNodeSourceType.Variable:
            LSIdentifierData.FromVariable[identifier] = data
        elif source==LSNodeSourceType.Builtin:
            LSIdentifierData.FromBuiltin[identifier] = data
        elif source==LSNodeSourceType.Plugins:
            LSIdentifierData.FromPlugins[identifier] = data
        else:
            raise ValueError(f"source {source} not supported")

    @staticmethod
    def unregister(identifier: str,source:str):
        if source==LSNodeSourceType.Ast and identifier in LSIdentifierData.FromAst:
            del LSIdentifierData.FromAst[identifier]
        elif source==LSNodeSourceType.Variable and identifier in LSIdentifierData.FromVariable:
            del LSIdentifierData.FromVariable[identifier]
        elif source==LSNodeSourceType.Builtin and identifier in LSIdentifierData.FromBuiltin:
            del LSIdentifierData.FromBuiltin[identifier]
        elif source==LSNodeSourceType.Plugins and identifier in LSIdentifierData.FromPlugins:
            del LSIdentifierData.FromPlugins[identifier]
    @staticmethod
    def register_variable(variable_name: str, data: LSRawData,type_):
        identifier = LSIdentifierData.variable_property_path(variable_name, type_)
        if identifier in LSIdentifierData.FromVariable:
            raise ValueError(f"identifier {identifier} already exists")
        LSIdentifierData.FromVariable[identifier] = data
        return identifier

    @staticmethod
    def unregister_variable(variable_name: str,type_):
        LSIdentifierData.unregister(
            LSIdentifierData.variable_property_path(variable_name,type_),
            LSNodeSourceType.Variable)

    @staticmethod
    def unregister_all_variables():
        LSIdentifierData.FromVariable.clear()


    @staticmethod
    def variable_property_path(variable_name: str, type_:str):
        return Func.ls_joinPaths(LSIdentifierData.variable_path(variable_name), type_)

    @staticmethod
    def variable_path(variable_name: str):
        return Func.ls_joinPaths(LSNodeItemType.Variable, variable_name)