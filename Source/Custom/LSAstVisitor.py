import ast
import collections
import inspect
import pprint

from Source import Globs
from Source.Common.Util import Util
from Source.Custom.Enums.LSPinEnum import LSPinAttrType
from Source.Custom.LSAstData import LSAstReturnData, LSAstFuncType, LSAstIdentifierSplitter
from Source.Custom.LSGlobalData import LSAstAttrTypeData
from Source.Custom.LSItemData import LSRawAstItemData, LSRawClassMethodData
from Source.Custom.Enums.LSItemEnum import LSNodeItemType, LSNodeSourceType
from Source.Widgets.NodeItem.LSMagicMethodNodeItem import LSMagicMethodNodeItem
from Source.Widgets.NodeItem.Event.LSExecNodeItem import LSExecNodeItem

DEFAULT_RETURN_VALUE = "return_value"


class LSAstReturnVisitor(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_return_name = DEFAULT_RETURN_VALUE
        self.return_names = [self.default_return_name]
        self.return_type = object.__name__
        self.count = 0

    def visit_Return(self, node):
        """
        如果发现有多个return 用union
        :param node:
        :return:
        """
        value = node.value
        if isinstance(value, (ast.Tuple, ast.List)):
            self.return_type = type(value).__name__.lower()
            for ele_idx, element in enumerate(value.elts):
                if isinstance(element, ast.Name):
                    self.return_names.append(element.id)
                else:
                    self.return_names.append(f"rt{ele_idx}")
        elif isinstance(value, (ast.Name)):
            self.return_names.append(value.id)
        elif isinstance(value, (ast.Constant)):
            self.return_names.append("const_rt")
            self.return_type = type(value.value).__name__
        else:
            "这里很多种可能性，比如是一个常量，一个变量，一个表达式，一个函数调用等等"
            self.return_names=[self.default_return_name]

        self.count += 1
        if self.count > 1:
            self.return_names = ["union_rt"]
        else:
            self.return_names=[self.default_return_name]

            # visitor=LSAstNameVisitor()
            # visitor.visit(body_node.value)
            # return_name = ast.unparse(body_node.value)
            # return_names = visitor.var_names


class LSAstVisitor(ast.NodeVisitor):
    def __init__(self, code_file,rel_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_file = code_file
        self.ast_info = {}
        self.func_path = []
        self.func_type = LSAstFuncType.NormalMethod
        self.current_class_name=""
        module_name = code_file.replace(rel_dir, "").replace("/", ".")
        module_name=module_name[1:module_name.rfind(".")]
        self.module=__import__(module_name)
        # 作用域
        with open(code_file, "r", encoding="utf8") as file:
            source = file.read()

        tree = ast.parse(source)
        self.visit(tree)

    def visit_ClassDef(self, node:ast.ClassDef):
        class_name = node.name
        if class_name.startswith("__"):
            return
        self.func_path.append(class_name)
        construct_func_ast = None
        self.current_class_name=class_name
        self.func_type = LSAstFuncType.ClassMethod
        for ever in node.body:
            if isinstance(ever, ast.FunctionDef) and ever.name.startswith("__"):
                if ever.name == "__init__":
                    construct_func_ast = ever
            else:
                self.visit(ever)

        arg_anno_dict = collections.OrderedDict()
        return_info = LSAstReturnData()

        _object_name = object.__name__
        if construct_func_ast is None:
            "如果没构造函数 可能是继承的类"
            if node.bases:
                parent_class = node.bases[0].id
                parent_init_func=inspect.getfullargspec(getattr(self.module,parent_class).__init__)
                if parent_init_func.args:
                    arg_anno_dict[parent_init_func.args[0]] = LSPinAttrType.user_class
                    for arg_name in parent_init_func.args[1:]:
                        arg_anno_dict[arg_name] = parent_init_func.annotations.get(arg_name, _object_name)
                    if parent_init_func.varargs:
                        arg_anno_dict[f"*{parent_init_func.varargs}"] = _object_name
                    if parent_init_func.varkw:
                        arg_anno_dict[f"**{parent_init_func.varkw}"] = _object_name
            else:
                "如果真没构造函数 就"
                arg_anno_dict[f"*args"] = _object_name
                arg_anno_dict[f"**kwargs"] = _object_name
        else:
            node_args = construct_func_ast.args
            if len(node_args.args) >= 1:
                "如果有装饰器 不一定是类成员函数"
                if construct_func_ast.decorator_list:
                    raise ValueError(f"Decorator not supported in init method")
                else:
                    for node_arg in node_args.args[1:]:
                        arg_name = node_arg.arg
                        if node_arg.annotation:
                            arg_anno = ast.unparse(node_arg.annotation)
                        else:
                            arg_anno = _object_name
                        arg_anno_dict[arg_name] = arg_anno
                    return_info.return_names = [DEFAULT_RETURN_VALUE]
                    return_info.attr_type = getattr(LSPinAttrType, class_name, LSPinAttrType.user_class)
        
            if node_args.vararg:
                arg_anno_dict[f"*{node_args.vararg.arg}"] = _object_name
            if node_args.kwarg:
                arg_anno_dict[f"**{node_args.kwarg.arg}"] = _object_name
            
        class_id= LSAstIdentifierSplitter.ClassSplitter.join(self.func_path) + f"{LSAstIdentifierSplitter.ClassSplitter}__init__"
        current_data = LSRawClassMethodData(func_name="__init__",
                                            class_name=class_name,
                                            args_info=arg_anno_dict,
                                            return_info=return_info,
                                            node_type=LSNodeItemType.ClassMagicMethod,
                                            instance_type=LSMagicMethodNodeItem.__name__,
                                            title=class_id,
                                            func_type=LSAstFuncType.ClassMethod,
                                            source=LSNodeSourceType.Ast
                                            )

        self.ast_info[class_id] = current_data

        self.func_type=LSAstFuncType.NormalMethod
        self.func_path.pop()

    def visit_FunctionDef(self, node):

        self.func_path.append(node.name)
        return_visitor = LSAstReturnVisitor()
        return_visitor.visit(node)
        returns = node.returns
        if returns:
            return_type = ast.unparse(returns)
        else:
            return_type = return_visitor.return_type

        return_info = LSAstReturnData(return_visitor.return_names, return_type)
        node_args = node.args

        arg_anno_dict = collections.OrderedDict()
        for node_arg in node_args.args:
            arg_name = node_arg.arg
            if node_arg.annotation:
                arg_anno = ast.unparse(node_arg.annotation)
            else:
                arg_anno = "object"

            arg_anno_dict[arg_name] = arg_anno

        if node_args.vararg:
            arg_anno_dict[f"*{node_args.vararg.arg}"] = object.__name__
        if node_args.kwarg:
            arg_anno_dict[f"**{node_args.kwarg.arg}"] = object.__name__

        func_id = LSAstIdentifierSplitter.ClassSplitter.join(self.func_path)
        if self.func_type==LSAstFuncType.NormalMethod:
            current_data = LSRawAstItemData(args_info=arg_anno_dict,
                                            return_info=return_info,
                                            node_type=LSNodeItemType.Stubs,
                                            instance_type=LSExecNodeItem.__name__,
                                            title=func_id,
                                            func_name=node.name,
                                            func_type=self.func_type,
                                            source=LSNodeSourceType.Ast
                                            )
        else:
            if node_args.args:
                arg_anno_dict[node_args.args[0].arg] = LSPinAttrType.user_class
            current_data = LSRawClassMethodData(func_name=node.name,
                                                class_name=self.current_class_name,
                                                args_info=arg_anno_dict,
                                                return_info=return_info,
                                                node_type=LSNodeItemType.ClassMagicMethod,
                                                instance_type=LSMagicMethodNodeItem.__name__,
                                                title=func_id,
                                                func_type=self.func_type,
                                                source=LSNodeSourceType.Ast
                                                )

        self.ast_info[func_id] = current_data
        self.func_path.pop()
