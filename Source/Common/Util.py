import contextlib
import logging
import time
import traceback
import types

from PySide2.QtCore import QTime, QCoreApplication, QEventLoop

from Source.Common.Logger import ls_print, LogInfo


class Util:

    class IgnoreKey:
        name = "__name__"
        qualname = "__qualname__"

    @staticmethod
    @contextlib.contextmanager
    def timing_context():
        start_time = time.time()

        try:
            # yield之前的代码在进入with语句块时执行
            yield
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")



    @staticmethod
    def log(func: types.MethodType):
        # is_print_it = func.__name__ not in IgnoreMethods
        is_print_it=True
        def wrapper(*args, **kwargs):
            try:
                if is_print_it:
                    ls_print(f"{LogInfo.prefix()}{func.__qualname__}",
                             log_level=logging.DEBUG,
                             is_log_callstack=False,
                             color=LogInfo.Color.Green)
                if LogInfo.FuncDepth>30:
                    raise RecursionError("递归深度过深")

                LogInfo.FuncDepth += 1
                t1=time.time()
                rt = func(*args, **kwargs)
                t2=time.time()
                LogInfo.FuncDepth-=1
                if is_print_it:
                    ls_print(f"{LogInfo.prefix()}%s" % (f"Elapsed time={round(t2 - t1, 6)}s"),
                             log_level=logging.DEBUG, is_log_callstack=False,
                             color=LogInfo.Color.Blue)
                return rt
            except Exception as e:
                LogInfo.FuncDepth -= 1
                if isinstance(e,NotImplementedError):
                    ls_print(func.__qualname__, "需要实现该方法")

                ls_print(LogInfo.prefix() + func.__qualname__, f"args={args}", f"kwargs={kwargs}", log_level=logging.ERROR, color=LogInfo.Color.Red, is_log_callstack=False)
                ls_print(LogInfo.prefix() + traceback.format_exc(), log_level=logging.ERROR, color=LogInfo.Color.Red)
        return wrapper

    @staticmethod
    def repolish(cls):
        cls.style().unpolish(cls)
        cls.style().polish(cls)
        cls.update()



    @staticmethod
    def process_sleep(msec, maxTime=10):
        """

        :param msec:
        :param maxTime:
        :return:
        """
        dieTime = QTime.currentTime().addMSecs(msec)
        while QTime.currentTime() < dieTime:
            QCoreApplication.processEvents(QEventLoop.AllEvents, maxTime)

