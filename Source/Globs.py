import contextlib
import dataclasses
import json
import logging
import os
import sys


# 或者使用下面这行，两行任选一行即可
from Source.Common.Func import OS, DateTime

from Source.Init.InitLog import init_logger


LOWSIDE_FILE_TYPE=".pyls"

widgets_fromlist= "Source.Widgets"
stubs_fromlist= "Source.Stubs"

main_dir = OS.dirnameTimes(__file__,2)

scripts_directory = OS.join(sys.exec_prefix, "Scripts")

uic = OS.join(scripts_directory, "pyside2-uic.exe")
rcc = OS.join(scripts_directory, "pyside2-rcc.exe")

example_dir = OS.join(main_dir, "Example")
logs_dir = OS.join(main_dir, "logs")

_now = DateTime.today().replace(":", "_")
log_path = OS.join(logs_dir, f"{_now}.log")
OS.makedirs(log_path, fileDirectory=True)

logger = init_logger(log_path)

config_dir = OS.join(main_dir, "Config")

source_dir = OS.join(main_dir, "Source")
test_dir = OS.join(main_dir, "Test")

widgets_dir = OS.join(source_dir, "Widgets")
custom_dir = OS.join(source_dir, "Custom")
qss_dir = OS.join(widgets_dir, "Qss")

stubs_dir = OS.join(source_dir, "Stubs")
plugins_dir = OS.join(source_dir, "Plugins")
resolve_paths=[stubs_dir,plugins_dir]


# 用于存储用户的缓存数据
user_cache_dir = OS.join(OS.expanduser("~"),"AppData","Local","LowSide","User")
tool_cache_dir = OS.join(OS.expanduser("~"),"AppData","Local","LowSide","Tool")
OS.makedirs(tool_cache_dir)

user_cache_json = OS.join(user_cache_dir,"cache.json")
logger.debug(f"user_cache_json: {user_cache_json}")

@dataclasses.dataclass
class UserCacheKey:
    loaded_paths:list[str]=dataclasses.field(default_factory=list)

    @staticmethod
    def save():
        logger.debug(f"save {user_cache_json}")
        with open(user_cache_json,"w") as f:
            json.dump(dataclasses.asdict(user_cache), f,indent=2)


OS.makedirs(user_cache_json,fileDirectory=True)
if OS.not_exist(user_cache_json):
    with open(user_cache_json,"w") as f:
        user_cache = UserCacheKey()
        json.dump(dataclasses.asdict(user_cache), f)
else:
    user_cache=UserCacheKey(**json.load(open(user_cache_json,"r",encoding="utf8")))


"让 解析器有环境"
for path in resolve_paths:
    if path in sys.path:
        sys.path.remove(path)
    sys.path.insert(0, path)

# Flag
is_record_command = True

@contextlib.contextmanager
def DisableRecordCommandContext():
    global is_record_command
    is_record_command = False
    yield
    is_record_command = True

def disable_record_command(func):
    def wrapper(*args, **kwargs):
        with DisableRecordCommandContext():
            return func(*args, **kwargs)
    return wrapper

