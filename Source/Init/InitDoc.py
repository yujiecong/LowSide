# import os
#
# from Common.Func import OS
# os.environ["PDOC_ALLOW_EXEC"]="1"
# path = "../../LowSide/Widgets/Custom"
# OS.system("pdoc --output ../Docs %s" % path)
# OS.system(f"pdoc {path} -p 8081")
import ast
import importlib
import inspect
import os
import pprint
import sys
import traceback
import types
import typing

from Source import Globs
from Source.Common.Func import OS, Shutil

temp="""
class {name}({parents}):
\t"自动生成的代码"
\tdef __init__(self):
\t{class_members}
\t\tpass
\t{instanced_members}

"""



MUST_BE_PARENT={
    "LSOutPin":"LSPin",
    "LSInPin":"LSPin",
}
python_path = sys.executable
# 通过解释器路径找到 site-packages 目录
site_packages_dir = os.path.join(OS.dirnameTimes(python_path,2), 'Lib', 'site-packages')

# 定义一个函数来遍历 AST 树
def extract_strings(node):
    strings = []
    if isinstance(node, ast.Name):
        strings.append(node.id)
    elif isinstance(node, ast.Subscript):
        strings.extend([f"{extract_strings(node.value)}[{extract_strings(node.slice)}]"])

    elif isinstance(node,ast.Attribute):
        strings.extend([f"{node.value.id}.{node.attr}"])

    return "".join(strings)


ABS = "Abstract"


def prapare(mod_name):
    for ever in OS.walk(OS.join(Globs.source_dir,mod_name)):
        ever=OS.basename(ever,suffix=True)
        if ever.startswith("__"):
            continue
        if ever.endswith(".py"):
            name = ever.split('.')[0]
            abc_name = f"Abs{name}"
            abstract_py = OS.join(Globs.source_dir,ABS, mod_name, abc_name + ".py")

            OS.makedirs(abstract_py, fileDirectory=True)
            ab_content = temp.format(
                name=abc_name,
                import_list="\n".join([]),
                parents=",".join([]),
                class_members="\t\n".join([]),
                instanced_members="\t\t\n".join([]),
            ) + "\n".join([])
            with open(abstract_py, "w", encoding="utf8") as f:
                f.write(ab_content)


def resolve(mod_name):
    # Shutil.rmtree(OS.join(site_packages_dir,"Source",mod_name))
    for ever in OS.walk(OS.join(Globs.source_dir,mod_name),relative=True):
        basename=ever.split("/")[-1]
        if basename.startswith("__"):
            continue
        if basename.endswith(".py"):
            name = basename.split('.')[0]

            # 获取当前 Python 解释器的路径

            abstract_py=OS.join(OS.join(Globs.source_dir,ABS,mod_name),f"Abs{name}"+".py")
            OS.makedirs(abstract_py,fileDirectory=True)
            mod_path=f"Source.{mod_name}{ever.split('.')[0].replace('/','.')}"
            mod=importlib.import_module(mod_path)

            content=[]
            import_list = []

            for mod_mem in dir(mod):
                value = getattr(mod, mod_mem)
                if not (inspect.isclass(value) and inspect.getmodule(value) == mod and value.__module__ != 'builtins'):
                    continue
                abc_name = f"Abs{mod_mem}"

                method_str=[]
                all_methods = set(dir(value))
                parents=[]
                members=[]
                all_member_names=[]
                mem_map={}

                instanced_members=[]
                for mem_name in inspect.getmembers(value):
                    if mem_name[0].startswith("__"):
                        continue
                    if inspect.isclass(mem_name[1]):
                        continue
                    all_member_names.append(mem_name[0])
                    mem_map[mem_name[0]]=mem_name[1]

                ignore_parents={"LSObject"}
                if hasattr(value, '__bases__'):
                    for base_cls in value.__bases__:
                        all_methods -= set(dir(base_cls))
                        for mem_name in inspect.getmembers(base_cls):
                            if mem_name[0] in all_member_names:
                                all_member_names.remove(mem_name[0])

                        if (base_cls.__name__.startswith("LS")):
                            module__ = base_cls.__module__
                            prefix=".".join(module__.split(".")[:-1]).replace("Source",f"Source.{ABS}")
                            # print(prefix)
                            # prefix=f"Source.Abstract.{mod_name}"
                            import_list.append(f"from {prefix}.Abs{base_cls.__name__} import Abs{base_cls.__name__}")

                            parents.append("Abs"+base_cls.__name__)
                        else:
                            if base_cls.__name__.startswith("Abs"):
                                pass
                            else:
                                pass
                                # parents.append(base_cls.__name__)

                        #
                        # else:

                class_source = inspect.getsource(value)

                # 解析源代码得到 AST
                class_ast = ast.parse(class_source)

                # 遍历 AST，查找赋值语句
                instance_variable_names=[]
                for node in ast.walk(class_ast):
                    # if isinstance(node, ast.Assign):
                    #     for target in node.targets:
                    # if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':

                    if isinstance(node, (ast.AnnAssign,)):
                        target = node.target
                        node_annotation = node.annotation
                        if isinstance(node_annotation, ast.Name):
                            member_type= node_annotation.id
                        elif isinstance(node_annotation, ast.Subscript):
                            if isinstance(node_annotation.slice,ast.Name):
                                # member_type = node_annotation.slice.id
                                member_type = ast.unparse(node_annotation)
                                mem_name = node_annotation.slice.id
                                mem_class = mod.__dict__.get(mem_name)
                                if mem_class:
                                    module__ = mem_class.__module__
                                    prefix = ".".join(module__.split(".")[:-1])
                                    prefix += "." + ABS
                                    # import_list.append(
                                    #     f"from {prefix}.Abs{mem_class.__name__} import Abs{mem_class.__name__}")


                            else:
                                member_type = ast.unparse(node_annotation)

                        else:
                            member_type=""

                        if (isinstance(target, ast.Attribute)
                                and isinstance(target.value,ast.Name)
                                and target.value.id == 'self'):
                            # 获取实例变量名和初始值
                            # print(ast.dump(target))
                            if isinstance(target,ast.Attribute):
                                instance_variable_name = target.attr
                            else:
                                instance_variable_name = target.value.attr
                            # print(ast.dump(node))
                            # if isinstance(node.value,ast.Attribute):
                            #     instanced_members.append(f"\t\tself.{instance_variable_name}:\"{node.value.value.id}\" = None")
                            # elif isinstance(node.value,ast.Name):
                            #     instanced_members.append(f"\t\tself.{instance_variable_name}:\"{node.value.id}\" = None")
                            # elif isinstance(node.value,ast.Call):
                            # instanced_members.append(f"\t\tself.{instance_va riable_name} = None")
                        elif isinstance(target, ast.Name):
                            instance_variable_name=target.id
                        else:
                            continue
                            # raise ValueError("aaa")
                        if member_type:
                            instanced_members.append(f'\tself.{instance_variable_name} : "{member_type}" = ...')
                            mem_class = mod.__dict__.get(member_type)

                            if mem_class:
                                module__ = mem_class.__module__
                                module___split = module__.split(".")
                                prefix = ".".join([*module___split[:-1],ABS,"Abs"+module___split[-1]] )

                                # import_list.append(f"from {prefix}.Abs{mem_class.__name__} import Abs{mem_class.__name__}")

                            else:
                                # pass
                                builtin_types = (int, float, str, list, tuple, dict, set)
                                if isinstance(member_type,builtin_types):
                                    pass
                                else:
                                    pass
                                    # import_list.append(
                                    #     f"from {prefix}.Abs{mem_class.__name__} import Abs{mem_class.__name__}")

                        else:
                            instanced_members.append(f'\tself.{instance_variable_name} = ...')

                        instance_variable_names.append(instance_variable_name)
                    elif isinstance(node,ast.Assign):

                        target = node.targets[0]
                        # target2 = node.targets[1]
                        #
                        node_value = node.value
                        # member_type = ast.unparse(node_value)

                        if isinstance(node_value, ast.Call):
                            # member_type=target1.annotation

                            node_value_func = node_value.func
                            if isinstance(node_value_func, ast.Name):
                                member_type= node_value_func.id
                        else:
                            member_type=""

                        # if isinstance(target, ast.Name):
                        #     pass
                            # print(target.id)

                        if isinstance(target, ast.Attribute):
                            instance_variable_name = target.attr
                            if member_type:
                                instanced_members.append(f'\tself.{target.attr} : "{member_type}" = ...')

                                # module__ = base_cls.__module__
                                # prefix = ".".join(module__.split(".")[:-1])
                                # prefix += "." + ABS
                                # import_list.append(f"from {prefix}.Abs{base_cls.__name__} import Abs{base_cls.__name__}")

                                # import_list.append(f"from Source.{mod_name}.{name} import {member_type}")
                            else:
                                instanced_members.append(f'\tself.{target.attr} = ...')
                        elif isinstance(target, ast.Name):
                            instanced_members.append(f'\tself.{target.id} = ...')

                        # instanced_members.append("")
                        # print(f"Instance variable: {instance_variable_name}, Type: {vid}")

                # print(instanced_members)
                if instanced_members:
                    instanced_members = sorted(list(set(instanced_members)))

                "有特殊情况"
                if name in MUST_BE_PARENT:
                    parents.append(MUST_BE_PARENT[name])
                    # import_list.append(f"from Source.{mod_name}.{MUST_BE_PARENT[name]} import {MUST_BE_PARENT[name]}")


                members_str=[]
                for mem_name in all_member_names:
                    mem_type = mem_map[mem_name]

                    if isinstance(mem_type,(types.FunctionType,types.MethodType)):
                        continue
                    mem_type_name = type(mem_type).__name__
                    # if hasattr(mem_type,"__module__"):
                        # import_list.append(f"from {mem_type.__module__} import {mem_type_name}")
                    members_str.append(f'\tself.{mem_name}:"{mem_type_name}"')



                for method in sorted(all_methods):
                    if not method.startswith('__') and not method.endswith('__'):
                        attr = getattr(value, method)
                        # print(value, method)
                        if isinstance(attr, (types.FunctionType,types.ClassMethodDescriptorType,types.MethodType)):
                            inspect_signature = inspect.signature(attr)
                            para_str_list=[]
                            for k,para in inspect_signature.parameters.items():
                                anno=para.annotation
                                if anno is inspect._empty:
                                    para_str_list.append(f"{k}")
                                else:
                                    if isinstance(anno,type):
                                        para_str_list.append(f"{k}:\"{anno.__name__}\"")
                                    elif isinstance(anno,str):
                                        para_str_list.append(f"{k}:\"{anno}\"")
                                    else:
                                        para_str_list.append(f"{k}:\"{anno}\"")


                            para_str=",".join(para_str_list)
                            method_str.append(
                                f"""\tdef {method}({para_str}):\n\t\traise NotImplementedError\n""")

                        # elif isinstance(attr,property):
                        #     pass
                ab_content=temp.format(
                    name=abc_name,
                    parents=",".join(parents),
                    # parents="",
                    class_members="\n\t".join(members_str),
                    instanced_members="\n\t".join(instanced_members)
                )+"\n".join(method_str)
                content.append(ab_content)

            import_list = "\n".join(sorted(list(set(import_list))))
            content.insert(0,"""{import_list}""".format(import_list=import_list))
            with open(abstract_py,"w",encoding="utf8") as f:
                f.write("\n".join(content))

raise
prapare("Widgets")
prapare("Custom")
prapare("Common")

resolve("Widgets")
resolve("Custom")
resolve("Common")