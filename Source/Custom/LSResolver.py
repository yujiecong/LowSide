import ast
import os
import pprint
import sys

from Source import Globs
from Source.Common import Func
from Source.Common.Func import OS
from Source.Custom.LSAstData import LSAstIdentifierSplitter
from Source.Custom.LSItemData import LSRawAstItemData
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSNodeSourceType
from Source.Custom.LSGlobalData import LSIdentifierData
from Source.Custom.LSAstVisitor import LSAstVisitor
from Source.Custom.LSObject import LSObject


class LSResolver:
    def __init__(self):
        self.resolve_all()

    def resolve_all(self):
        self.resolve_stubs()
        self.resolve_plugins()
        self.resolve_builtin_item_types()

    def resolve(self, code_file,rel_dir):
        code_file=OS.unixpath(code_file)
        visitor=LSAstVisitor(code_file,rel_dir)

        return visitor.ast_info

    def resolve_stubs(self):
        directory = Globs.stubs_dir
        for rel_path in OS.walk(directory, relative=True):
            full_path= directory + rel_path
            basename=OS.basename(full_path)
            if basename.startswith("__"):
                continue
            if OS.isfile(full_path) and rel_path.endswith(".py"):
                stub_file = directory + rel_path
                if not OS.isfile(stub_file):
                    continue
                func_info=self.resolve(stub_file,directory)
                for func_full_path,func_ast_data in func_info.items():
                    func_ast_data:LSRawAstItemData
                    module_path = rel_path[1:][:rel_path.rfind(".") - 1].replace("/", LSAstIdentifierSplitter.IdentifierSplitter)
                    identifier = Func.ls_joinPaths(LSNodeSourceType.Ast, module_path, func_full_path)
                    LSIdentifierData.register(identifier, func_ast_data,LSNodeSourceType.Ast)

    def resolve_plugins(self):
        directory = Globs.plugins_dir
        for rel_path in OS.walk(directory, relative=True):
            full_path= directory + rel_path
            basename=OS.basename(full_path)
            if basename.startswith("__"):
                continue
            if OS.isfile(full_path) and rel_path.endswith(".py"):
                stub_file = directory + rel_path
                if not OS.isfile(stub_file):
                    continue
                func_info=self.resolve(stub_file,directory)
                for func_full_path,func_ast_data in func_info.items():
                    func_ast_data:LSRawAstItemData
                    module_path = rel_path[1:][:rel_path.rfind(".") - 1].replace("/", LSAstIdentifierSplitter.IdentifierSplitter)
                    identifier = Func.ls_joinPaths(LSNodeItemType.Plugins, module_path, func_full_path)
                    LSIdentifierData.register(identifier, func_ast_data,LSNodeSourceType.Plugins)


    def resolve_builtin_item_types(self):
        for ever in OS.walk(Globs.widgets_dir,relative=True):
            # 检查文件是否以 .py 结尾，并且不是以 . 开头的文件
            path = ever.split(".")[0]
            path = path.replace("/", ".")
            if ever.endswith('.py') and not path.endswith('__'):
                __import__(f"{Globs.widgets_fromlist}{path}")

        for name,cls in LSObject.registered_classes.items():
            cls:LSObject
            item_type=cls.__NODE_ITEM_TYPE__
            if cls.__LS_TYPE_NAME__:
                if item_type==LSNodeItemType.Event:
                    identifier = Func.ls_joinPaths(LSNodeItemType.Event, cls.__LS_TYPE_NAME__)
                    title = cls.__LS_TYPE_NAME__
                elif item_type==LSNodeItemType.Control:
                    identifier = Func.ls_joinPaths(LSNodeItemType.Control, cls.__LS_TYPE_NAME__)
                    title = cls.__LS_TYPE_NAME__
                elif item_type == LSNodeItemType.Operator:
                    identifier = Func.ls_joinPaths(LSNodeItemType.Operator, cls.__LS_TYPE_NAME__)
                    title = cls.__LS_TYPE_NAME__
                else:
                    raise ValueError(f"Unknown item type {item_type}")
                item_ast_data = LSRawAstItemData(node_type=item_type, instance_type=cls.__name__, title=title,
                                        source=LSNodeSourceType.Builtin)
                LSIdentifierData.register(identifier,
                                          item_ast_data,
                                          source=LSNodeSourceType.Builtin)


        # for event_identifier in LSGlobalData.BuiltinsEventIdentifiers:
        #     LSGlobalData.IdentifierNodeData[event_identifier] = (
        #         LSRawAstData(node_type=LSNodeItemType.Event, instance_type=LSEventNodeItem_ProgramStart,
        #                      title=event_identifier.replace(Func.joinPaths(LSNodeItemType.Event, ""), ""))
        #     )

if __name__ == '__main__':
    r = LSResolver()

    # pprint.pprint(r.resolve(r"C:\repo\_USDQ\LowSide\Source\Stubs\test_mod.py"))

