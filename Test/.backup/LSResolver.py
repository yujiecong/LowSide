import builtins
import collections
import dataclasses
import inspect
import pprint
import types

import Globs
from Common.Enums import LSNodeItemType
from Common.Func import OS
from Common.Util import Util
from Source.Custom.LSResolveData import LSResolveData


class LSResolver:
    def __init__(self):
        self.custom_method_dict = {}
        self.module_stubs_dict = {}

    def _recursive_resolve_stb_members(self, stubs_dict,member, path, depth=0):
        if inspect.isclass(member):
            class_members = dir(member)
            for class_member_name in class_members:
                if class_member_name.startswith("__"):
                    continue
                class_member = getattr(member, class_member_name)

                if inspect.isfunction(class_member) or inspect.ismethod(class_member) or inspect.ismethoddescriptor(
                        class_member):
                    stubs_dict[f"{path}.{class_member_name}"] = LSResolveData(class_member,
                                                                              inspect.signature(class_member).parameters)
                elif isinstance(class_member, type):
                    self._recursive_resolve_stb_members(stubs_dict,class_member, class_member_name,
                                                        f"{path}.{class_member_name}", depth + 1)

        elif isinstance(member, (types.FunctionType, types.BuiltinFunctionType)):
            stubs_dict[path] = LSResolveData(member,
                                             inspect.signature(member).parameters)

    def resolve(self, stub_file):
        stub_file=OS.unixpath(stub_file)
        module_full_path = OS.basename(stub_file).replace(Globs.stubs_dir, "").replace("/", ".")
        cur_module_stubs_dict={}
        target_module = Util.create_module_from_file(stub_file, OS.basename(stub_file))
        all_module_class_names = dir(target_module)
        for module_class_name in all_module_class_names:
            if module_class_name.startswith("__"):
                continue
            # if not module_class_name=="str":
            #     continue
            module_class = getattr(target_module, module_class_name)
            self._recursive_resolve_stb_members(cur_module_stubs_dict,module_class, f"{module_full_path}.{module_class_name}")

        self.module_stubs_dict[module_full_path]=cur_module_stubs_dict
        return cur_module_stubs_dict

    def resolve_stubs(self):
        for rel_path in OS.walk(Globs.stubs_dir, relative=True):
            stub_file = Globs.stubs_dir + rel_path
            if not OS.isfile(stub_file):
                continue
            self.resolve(stub_file)

if __name__ == '__main__':
    r = LSResolver()
    # r.resolve_stubs()
    r.resolve(r"C:\repo\_USDQ\LowSide\Source\Stubs\test_mod.py")
    pprint.pprint(r.module_stubs_dict)

