import inspect
import logging
import pprint

from Source import Globs


class LogInfo:
    """
    \033[91m：红色
    \033[92m：绿色
    \033[93m：黄色
    \033[94m：蓝色
    \033[95m：紫色
    \033[96m：青色
    \033[0m：重置颜色
    """
    class Color:
        Red="\033[91m"
        Red2="\033[35m"
        Green="\033[92m"
        Blue="\033[94m"
        Yellow="\033[93m"
        Default="\033[0m"

    FuncDepth = 0
    Symbol="──"
    @staticmethod
    def prefix():
        return "{0}".format(LogInfo.Symbol*LogInfo.FuncDepth)


def ls_print(*args,is_log_callstack=True,color=LogInfo.Color.Yellow,log_level=logging.DEBUG):
    stack = inspect.stack()
    # for i, frame in enumerate(stack):
    #     text = "{0}:{1}".format(frame.filename, frame.lineno)
        # if is_print:
        #     print(text)
        # if is_log_callstack:
            # Globs.logger.log(level=log_level,msg="{0}\"{1}\"".format(LogInfo.prefix(),text))
    if is_log_callstack:
        if log_level!=logging.ERROR:
            frame=stack[1]
            frame_info = " \"{0}:{1}\"".format(frame.filename, frame.lineno)
        else:
            info=[]
            for f in stack[1:]:
                info.append("\"{0}:{1}\"".format(f.filename, f.lineno))
            frame_info="\n".join(info)
    else:
        frame_info=""

    formatter = "{0}├─ {1}{2} -> [{3}]{4}"
    # formatter2 = "{0}├─ {1}{2}{3}{4}"

    # for arg in args:
    Globs.logger.log(level=log_level, msg=formatter.format(
        color,
        LogInfo.prefix(),
        " ".join(arg.__str__() for arg in args),frame_info,
        LogInfo.Color.Default
        ))

