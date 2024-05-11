import dataclasses
import datetime
import filecmp
import inspect
import logging
import os
import shutil
import signal
import subprocess
import sys
import threading
import types
import warnings

# import numpy as np
from PySide2.QtCore import *
from PySide2.QtGui import *
def distance_between_points(point1, point2):
    x1, y1 = point1.x(), point1.y()
    x2, y2 = point2.x(), point2.y()
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

def parse_dataclass(obj):
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            if hasattr(value, '__dataclass_fields__'):
                result[field.name] = parse_dataclass(value)
            elif isinstance(value, list):
                result[field.name] = [parse_dataclass(item) for item in value]
            elif isinstance(value, dict):
                result[field.name] = {k: parse_dataclass(v) for k, v in value.items()}
            else:
                result[field.name] = value
        return result
    elif isinstance(obj, list):
        return [parse_dataclass(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: parse_dataclass(v) for k, v in obj.items()}
    else:
        return obj
def make_lambda_runtime(sth):
    return sth()
def make_variable_runtime(sth):
    return sth

def lighten_color(color, factor):
    # 将 QColor 转换为 HSL 颜色空间
    h, s, l, a = color.getHslF()

    # 减少饱和度
    s *= factor

    # 限制饱和度的范围在 0 到 1 之间
    s = max(0.0, min(s, 1.0))

    # 创建新的 QColor 对象并返回
    return QColor.fromHslF(h, s, l, a)

def get_variable_name(var):
    frame = inspect.currentframe()
    try:
        locals_dict = frame.f_back.f_locals
        for name, value in locals_dict.items():
            if value is var:
                return name
    finally:
        del frame


# def bezier_curve(t, p0, p1, p2, p3):
#     u = 1 - t
#     return u ** 3 * p0 + 3 * u ** 2 * t * p1 + 3 * u * t ** 2 * p2 + t ** 3 * p3
def bezier_curve(t, p0, p1, p2, p3):
    u = 1 - t
    # 确保参数是数字而不是序列
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    # 使用数字进行乘法运算
    return [u ** 3 * x0 + 3 * u ** 2 * t * x1 + 3 * u * t ** 2 * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u ** 2 * t * y1 + 3 * u * t ** 2 * y2 + t ** 3 * y3]

# 
# def find_perpendicular_point(line_point1, line_point2, point_A, distance):
#     x1, y1 = line_point1
#     x2, y2 = line_point2
#     x_A, y_A = point_A
# 
#     # 计算直线斜率
#     # 计算直线斜率
#     diff_x = x2 - x1
#     diff_y = y2 - y1
# 
#     if diff_x != 0 and diff_y != 0:
#         slope = (diff_y) / (diff_x)
#     else:
#         slope = np.inf  # 使其表示垂直线
# 
#     # 处理垂直线的情况
#     if np.isinf(slope):
#         # 如果直线是垂直的，选择一个水平方向的直线
#         x_B = x_A + distance
#         y_B = y_A
#     else:
#         # 计算垂直斜率
#         perpendicular_slope = -1 / slope
# 
#         # 计算垂直线的截距
#         intercept = y_A - perpendicular_slope * x_A
# 
#         # 根据点斜式计算垂直线方程
#         def perpendicular_line_equation(x):
#             return perpendicular_slope * x + intercept
# 
#         # 找到垂直线上距离点 A 3 个单位的点 B
#         x_B = x_A + distance / np.sqrt(1 + perpendicular_slope ** 2)
#         y_B = perpendicular_line_equation(x_B)
#     return np.array([x_B, y_B])
# 
# 
# def calculate_control_points(p0, p3):
#     """
# 
#     :param p0:
#     :param p3:
#     :return:
#     """
#     # p1 = p0 + (p3 - p0) / 3.
#     # p2 = p3 - (p3 - p0) / 3.
#     if p3[0] < p0[0]:
#         diff_x = (abs(p3[0] - p0[0])) / 1.6
#         diff_y = 0
#         p1 = p0 + np.array([diff_x, diff_y])
#         p2 = p3 - np.array([diff_x, diff_y])
#     else:
#         p1 = p0 + (p3 - p0) / 3.
#         p2 = p3 - (p3 - p0) / 3.
# 
#     dis = abs(p0[1] - p3[1]) / 3
#     c1 = find_perpendicular_point(p0, p3, p1, dis)
#     c2 = find_perpendicular_point(p0, p3, p2, -dis)
# 
#     return c1, c2

def find_perpendicular_point(line_point1, line_point2, point_A, distance):
    x1, y1 = line_point1
    x2, y2 = line_point2
    x_A, y_A = point_A

    # 计算直线斜率
    diff_x = x2 - x1
    diff_y = y2 - y1

    if diff_x != 0 and diff_y != 0:
        slope = (diff_y) / (diff_x)
    else:
        slope = float('inf')  # 使其表示垂直线

    # 处理垂直线的情况
    if slope == float('inf'):
        # 如果直线是垂直的，选择一个水平方向的直线
        x_B = x_A + distance
        y_B = y_A
    else:
        # 计算垂直斜率
        perpendicular_slope = -1 / slope

        # 计算垂直线的截距
        intercept = y_A - perpendicular_slope * x_A

        # 根据点斜式计算垂直线方程
        def perpendicular_line_equation(x):
            return perpendicular_slope * x + intercept

        # 找到垂直线上距离点 A 3 个单位的点 B
        x_B = x_A + distance / (1 + perpendicular_slope ** 2) ** 0.5
        y_B = perpendicular_line_equation(x_B)
    return [x_B, y_B]


def calculate_control_points(p0, p3):
    """
    :param p0:
    :param p3:
    :return:
    """
    # p1 = p0 + (p3 - p0) / 3.
    # p2 = p3 - (p3 - p0) / 3.
    if p3[0] < p0[0]:
        diff_x = (abs(p3[0] - p0[0])) / 1.6
        diff_y = 0
        p1 = [p0[0] + diff_x, p0[1] + diff_y]
        p2 = [p3[0] - diff_x, p3[1] - diff_y]
    else:
        p1 = [p0[0] + (p3[0] - p0[0]) / 3., p0[1] + (p3[1] - p0[1]) / 3.]
        p2 = [p3[0] - (p3[0] - p0[0]) / 3., p3[1] - (p3[1] - p0[1]) / 3.]

    dis = abs(p0[1] - p3[1]) / 3
    c1 = find_perpendicular_point(p0, p3, p1, dis)
    c2 = find_perpendicular_point(p0, p3, p2, -dis)

    return c1, c2

class PainterPath:

    @staticmethod
    def linear_interpolation_qpoint(p0, p1, n):
        points = []
        for i in range(n):
            t = i / (n - 1)  # 步长在 [0, 1] 之间
            x = (1 - t) * p0.x() + t * p1.x()
            y = (1 - t) * p0.y() + t * p1.y()
            # points.append(QPoint(x, y))
            points.append([x, y])
        return points

    @staticmethod
    def bezier_painter_path(p1, p2):
        start_pos_x = p1.x()
        end_pos_x = p2.x()
        start_pos_y = p1.y()
        end_pos_y = p2.y()
        c1 = QPoint((start_pos_x + end_pos_x) / 2, start_pos_y)
        c2 = QPoint((start_pos_x + end_pos_x) / 2, end_pos_y)
        path = QPainterPath()
        path.moveTo(p1)
        path.cubicTo(c1, c2, p2)
        return path

    # @staticmethod
    # def create_line(p0, p3):
    #     path = QPainterPath()
    #     path.moveTo(*p0)
    #     p0 = np.array(p0)
    #     p3 = np.array(p3)
    #     p1, p2 = calculate_control_points(p0, p3)
    #     curve_points = np.array([bezier_curve(t,
    #                                           p0,
    #                                           p1,
    #                                           p2,
    #                                           p3) for t in np.linspace(0, 1, 100)])
    #     for point in curve_points:
    #         path.lineTo(*point)
    #     return path
    
    @staticmethod
    def create_line(p0, p3):
        path = QPainterPath()
        path.moveTo(*p0)
        p0 = list(p0)
        p3 = list(p3)
        p1, p2 = calculate_control_points(p0, p3)
        curve_points = [bezier_curve(t, p0, p1, p2, p3) for t in [i / 100 for i in range(101)]]
        for point in curve_points:
            path.lineTo(*point)
        return path


class OS:
    """
    下面的函数有些和 os一致,有些有很大区别,注意区分
    """

    @staticmethod
    def canwrite(file_path):
        if os.access(file_path, os.W_OK):
            return True
        else:
            return False

    @staticmethod
    def chmod(path, mode):
        """
        修改权限 经常出现只读文件的情况 所以要修改一下
        :param str path:
        :param str mode:
            - 0o444 只读
            - 0o666 读写
            - 0o777 执行

        :return:
        """
        os.chmod(path, mode)

    @staticmethod
    def utime(path, time_tuple):
        os.utime(path, time_tuple)

    @staticmethod
    def getctime(fp):
        """
        获得修改时间
        :param str fp:
        :return: str
        :rtype: str
        """
        return os.path.getctime(fp)

    @staticmethod
    def getmtime(fp):
        """
        获得修改时间
        :param str fp:
        :return: str
        :rtype: str
        """
        return os.path.getmtime(fp)

    @staticmethod
    def abspath(path, is_unix=True):
        """
        与 os的一致
        :param str path:
        :return:
        """
        return OS.unixpath(os.path.abspath(path)) if is_unix else os.path.abspath(path)

    @staticmethod
    def chdir(path):
        """
        与 os的一致
        :param str path:
        :return:
        """
        os.chdir(path)

    @staticmethod
    def curDir():
        """
        与 os的一致
        :return:
        """
        return os.path.curdir

    @staticmethod
    def expandinrd():
        return os.path.expanduser("~/inrd")

    @staticmethod
    def expanduser(path):
        """
        与 os的一致
        :param path:
        :return:
        """
        return os.path.expanduser(path)

    @staticmethod
    def startfile(fp):
        """
        与 os的一致
        :param fp:
        :return:
        """
        os.startfile(fp)

    @staticmethod
    def winpath(fp):
        """
        转化成反斜杠
        :param fp:
        :return:
        """
        return fp.replace("/", "\\")

    @staticmethod
    def relpath(abs_fp, base_fp):
        return os.path.relpath(abs_fp, base_fp)

    @staticmethod
    def unixpath(fp):
        """
        将反斜杠转化为斜杠
        :param fp:
        :return:str
        :rtype:str

        """
        return fp.replace("\\", '/')

    @staticmethod
    def unixpaths(fps):
        """
        批量 将反斜杠转化为斜杠
        :param fps:
        :return:
        """
        return [fp.replace("\\", '/') for fp in fps]

    @staticmethod
    def system(*args, **kwargs):
        """
        与 os的一致
        :param args:
        :param kwargs:
        :return:
        """
        return os.system(*args, **kwargs)

    @staticmethod
    def systemrd(dir_):
        """
        忘记干嘛的了
        :param dir_:
        :return:
        """
        return os.system("rd %s" % dir_)

    @staticmethod
    def isdir(fp):
        """
        与OS的一致
        :param fp:
        :return:
        """
        return os.path.isdir(fp)

    @staticmethod
    def isfile(fp):
        """
        与OS的一致
        :param fp:
        :return:
        """
        return os.path.isfile(fp)

    @staticmethod
    def listdir(fp, fullPath=False, ):
        """
        与OS的略有区别,可以指定多一个参数
        :param fp:
        :param fullPath:是否全路径传回去
        :return:
        """
        if os.path.exists(fp):
            if fullPath:
                return [OS.join(fp, ever) for ever in os.listdir(fp)]

            else:
                return os.listdir(fp)
        else:
            return []

    @staticmethod
    def walkdfs(walkDir, relativeDir=False, ignoreFiles=None, ignoreDirs=None, ignoreFileNames=None,
                ignoreDirNames=None, ignoreFileTypes=None):
        """

        :param walkDir:
        :param relativeDir:
        :param ignoreFiles:
        :param ignoreDirs:
        :param ignoreFileNames:
        :param ignoreDirNames:
        :param ignoreFileTypes:
        :return:
        """
        ignoreDirs = ignoreDirs or []
        ignoreFiles = ignoreFiles or []
        ignoreFileNames = ignoreFileNames or []
        ignoreDirNames = ignoreDirNames or []
        ignoreFileTypes = ignoreFileTypes or []
        filePaths = []

        def dfs(_filePath, currentDir=""):
            for ever in OS.listdir(_filePath):
                currentRelativePath = "%s/%s" % (currentDir, ever)
                currentFilePath = OS.join(_filePath, ever)
                if OS.isfile(currentFilePath):
                    skipFlag = False
                    if "." in ever:
                        fileType = ever.split(".", 1)[-1]
                        if fileType in ignoreFileTypes:
                            skipFlag = True
                    if ever in ignoreFileNames:
                        skipFlag = True
                    if currentRelativePath in ignoreFiles:
                        skipFlag = True

                    if skipFlag:
                        continue

                    if relativeDir:
                        filePaths.append(currentRelativePath)
                    else:
                        filePaths.append(currentFilePath)

                elif OS.isdir(currentFilePath):
                    if ever in ignoreDirNames:
                        continue
                    if currentRelativePath in ignoreDirs:
                        continue
                    dfs(currentFilePath, "%s/%s" % (currentDir, ever))

        dfs(walkDir)
        return filePaths

    @staticmethod
    def walk(directory, includeFile=True, includeDir=False, suffix=None, relative=False):
        """
        遍历目录
        :param str directory: 目录
        :param bool includeFile: 包括文件
        :param bool includeDir: 包括目录
        :param str suffix: 指定后缀
        :param bool relative: 是否返回相对路径
        :return:
        """

        directory = directory.replace("\\", "/")
        if os.path.exists(directory):
            prefix = ""
            if suffix:
                for root, dirs, fileNames in os.walk(directory):
                    if includeFile:
                        for fileName in fileNames:
                            filePath = os.path.join(root, fileName)
                            if filePath.endswith(suffix):
                                if relative:
                                    yield filePath.replace("\\", '/').replace(directory, prefix)
                                else:
                                    yield filePath.replace("\\", '/')
                    if includeDir:
                        for dir_ in dirs:
                            filePath = os.path.join(root, dir_)
                            if filePath.endswith(suffix):
                                if relative:
                                    yield filePath.replace("\\", '/').replace(directory, prefix)
                                else:
                                    yield filePath.replace("\\", '/')
            else:
                for root, dirs, fileNames in os.walk(directory):
                    if includeFile:
                        for fileName in fileNames:
                            filePath = os.path.join(root, fileName)
                            if relative:
                                yield filePath.replace("\\", '/').replace(directory, prefix)
                            else:
                                yield filePath.replace("\\", '/')
                    if includeDir:
                        for dir_ in dirs:
                            filePath = os.path.join(root, dir_)
                            if relative:
                                yield filePath.replace("\\", '/').replace(directory, prefix)
                            else:
                                yield filePath.replace("\\", '/')
        else:
            raise OSError("directory %s not exists" % directory)

    @staticmethod
    def remove(filePath):
        """
        调用前会先判断是否存在该路径

        :param str filePath:
        :return:
        """
        if os.path.exists(filePath):
            # try:
            os.remove(filePath)
            # except Exception:
            #     traceback.print_exc()
            #     os.system("del %s" % filePath)

    @staticmethod
    def makedirs(filePath, fileDirectory=False):
        """
        调用前会判断是否存在该路径,再创建目录
        :param str filePath:
        :param bool fileDirectory: 是否是一个文件路径
            - 若是则创建这个文件的目录
        :return:
        """
        if fileDirectory:
            fileDir = os.path.dirname(filePath)
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
        else:
            if not os.path.exists(filePath):
                os.makedirs(filePath)

    @staticmethod
    def not_exist(fp):
        """
        是否不存在该路径
        :param str fp:
        :return: bool
        :rtype:bool
        """
        return not os.path.exists(fp)

    @staticmethod
    def exists(fp):
        """
        判断是否存在,跟os行为一致
        :param str fp:
        :return: bool
        :rtype: bool
        """
        return os.path.exists(fp)

    @staticmethod
    def rename(src, des, force=True):
        """
        大部分跟os行为一致,只是多了个参数
        :param str src:
        :param str des:
        :param force:是否强制改名,也就是先删除再改名
        :return:
        """
        if force and OS.exists(des):
            OS.remove(des)
        os.rename(src, des)

    @staticmethod
    def kill(pid):
        """
        传入pid kill掉某个进程
        :param pid:
        :return:
        """
        os.kill(pid, signal.SIGINT)

    @staticmethod
    def killself(_signal=signal.SIGINT):
        """
        其实应该翻译成suicide,把当前的父进程kill了

        如果在Maya使用python调用,就会把Maya kill了,ue同理

        用来做自动化很舒服
        :return:
        """
        os.kill(os.getpid(), _signal)

    @staticmethod
    def getpid():
        return os.getpid()

    @staticmethod
    def join(*args):
        """
        跟os.join差不多,不过会将反斜杠替换了
        :param args:
        :return:
        """
        _path = os.path.join(*args)
        return _path.replace("\\", "/")
        #
        # if not _path.startswith(r"\\"):
        #     return _path.replace("\\", "/")
        # else:
        #     return r"\\"+_path[2:].replace("\\", "/")

    @staticmethod
    def getsize(filePath):
        """
        跟os一样
        :param filePath:
        :return: int
        :rtype: int
        """
        return os.path.getsize(filePath)

    @staticmethod
    def join_(*args):
        """
        跟路径无关,只是一个 斜杠的拼凑,与下列函数等价
        :param args:
        :return: str
        """
        return "/".join(args)

    @staticmethod
    def tempdir():
        """
        直接拿到C盘的TEMP目录
        :return: str
        :rtype: str
        """
        return os.path.expandvars("%TEMP%")

    @staticmethod
    def expandvars(*args):
        """
        跟 os的行为相同
        :param args:
        :return:
        """
        return os.path.expandvars(*args)

    @staticmethod
    def dirnameTimes(dirPath, times=1):
        """
        根据次数获得路径的目录
        :param str dirPath:
        :param int times:
        :return:str
        :rtype:str
        """
        _t = dirPath
        for i in range(times):
            _t = os.path.dirname(_t)
        return _t.replace("\\", '/')

    @staticmethod
    def basename(filePath, suffix=False):
        """
        os.basename的拓展,照常用就可以了
        不过有一点区别要注意
        后缀名,也就是文件的后缀.xxxx  .py 这种默认是切断的
        :param str filePath:
        :param bool suffix: 是否带文件后缀名?
        :return: str
        :rtype: str
        """
        _fp = filePath
        if os.path.isfile(_fp):
            _fp = os.path.basename(_fp)
            if not suffix:
                _fp = _fp.split(".", 1)[0]
            else:
                pass
            return _fp
        elif os.path.isdir(_fp):
            return os.path.basename(_fp)
        else:
            return os.path.basename(_fp)

    @staticmethod
    def filetype(filePath):
        """
        传入路径判断文件类型

        如果是目录则会报错,如果没有文件类型会返回空字符串

        如果没有文件类型则返回空字符串,否则返回 xxx 例如 mb,ma fbx
        :param str filePath:
        :return: str
        :rtype: str
        """
        if OS.not_exist(filePath):
            raise IOError("不存在路径%s" % filePath)
        if OS.isfile(filePath):
            bn = OS.basename(filePath, suffix=True)
            found_point = bn.rfind(".")
            if found_point == -1:
                return ""
            return bn[found_point + 1:]

        raise AttributeError("不能将目录作为路径传入")

    @staticmethod
    def new(filePath):
        """
        new 一个 0 kb 的文件
        :param str filePath:
        :return:
        """
        if os.path.exists(filePath):
            return
        os.makedirs(os.path.dirname(filePath))
        with open(filePath, 'w') as f:
            pass


class Subprocess:
    @staticmethod
    def popen(cmd, printText=True, logger=None, loggerLevel="INFO", env=None, shell=True, returnType="text"):
        """
        子进程通信的封装
        :param shell: 是否以 shell执行
        :param env: 子进程环境 若为None 则用 os.environ
        :param cmd:
        :param printText:
        :param logger:
        :param loggerLevel:
        :param str returnType: 返回的类型
            - text 代表返回文本
            - popen 代表返回子进程管道
        :return:
        """
        env = os.environ if env is None else env
        popen = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        # popen.communicate()
        texts = []
        while popen.poll() is None:
            realtime_output = popen.stdout.readline()
            if realtime_output:
                text = realtime_output.strip()
                try:
                    text = text.decode("utf8")
                    if logger:
                        logger.log(getattr(logging, loggerLevel), text)
                    texts.append(text)
                except Exception as e:
                    warnings.warn(e.__str__())
        if returnType == "text":
            return "\n".join(texts)
        elif returnType == "popen":
            return popen

    @staticmethod
    def maya(mayaPath, pyFilePath="", externalData=None, env=None,
             returnType="text",
             prompt=True, shell=True,
             noAutoloadPlugins=False,
             isUsingThread=False,
             isImmediatelyStart=True,
             isUsingBatch=False, ):
        """
        传入Maya路径和python路径可以直接调用Maya启动python代码
        :param mayaPath:
        :param pyFilePath:
        :param externalData:  传入py文件的数据
        :param env:  子进程环境
        :param str returnType:  返回的类型
        :param prompt: 是否后台
        :param noAutoloadPlugins:
        :param isUsingThread: 使用线程执行进程
        :param isImmediatelyStart: 立即执行
        :param isUsingBatch: 是否使用bat运行
        :return:
        """

        pyFilePath = OS.unixpath(pyFilePath)
        mayaPath = OS.unixpath(mayaPath)
        pythonCode = r"""import sys
        EXTERNAL_DATA={externalData}
        exec(open(r'{pyFilePath}',{encoding}).read(),globals(),locals())""" \
            .lstrip("    ").lstrip("\t").replace("\n", ";").format(pyFilePath=pyFilePath,
                                                                   externalData=externalData,
                                                                   encoding="encoding='utf8'" if sys.version_info.major == 3 else ""
                                                                   )

        melCmd = "\"python(\\\"%s\\\");\"" % pythonCode
        mayaCmd = ['"{}"'.format(mayaPath),
                   "-command",
                   melCmd,
                   "" if prompt is False else "-prompt",
                   "" if noAutoloadPlugins is False else "-noAutoloadPlugins",
                   ]

        mayaCmd = " ".join(mayaCmd)

        if isImmediatelyStart:
            if isUsingThread:
                threading.Thread(target=Subprocess.popen, args=[mayaCmd], kwargs={"returnType": returnType}).start()
            elif isUsingBatch:
                t_bat = OS.join(OS.tempdir(), "_.bat")
                open(t_bat, 'w', encoding="utf8").write(mayaCmd)
                OS.startfile(t_bat)
            else:
                return Subprocess.popen(mayaCmd, env=env, shell=shell, returnType=returnType)

        else:
            return mayaCmd

    @staticmethod
    def ue(uePath, projectPath, pyPath="", shell=True, isImmediatelyStart=True):
        """
        子进程调用ue出来
        :param str uePath:
        :param str projectPath:
        :param str pyPath:
        :return:
        """
        uePath = '"%s"' % uePath
        projectPath = '"%s"' % projectPath
        pyPath = '-ExecCmds="py %s"' % pyPath

        ueCmd = " ".join([uePath, projectPath, pyPath])
        if isImmediatelyStart:
            return Subprocess.popen(ueCmd, shell=shell)
        return ueCmd


class Shutil:
    @staticmethod
    def copyInPlace(src, des=None):
        """
        原地copy,默认名字就叫 xxx_copy
        :param des:
        :param src:
        :return: str 复制后的名字
        :rtype: str
        """
        if des is None:
            copy_index = 1
            default_des = OS.join(OS.dirnameTimes(src), OS.basename(src) + "_copy.{}".format(OS.filetype(src)))
            while OS.exists(default_des):
                default_des = OS.join(OS.dirnameTimes(src),
                                      OS.basename(src) + "_copy{}.{}".format(copy_index, OS.filetype(src)))
                copy_index += 1
            des = default_des

        Shutil.copyFile2File(src, des)
        return des

    @staticmethod
    def move(src, des):
        """
        等同 剪切
        :param src:
        :param des:
        :return:
        """
        shutil.move(src, des)

    @staticmethod
    def copytree(src, des, force=False):
        """
        复制指定目录到指定目录
        :param src:
        :param des:
        :param force:
        :return:
        """
        if force:
            Shutil.rmtree(des)
        shutil.copytree(src, des)

    @staticmethod
    def rmtree(dir_):
        """
        判断是否存在先再删除目录
        :param dir_:
        :return:
        """
        if OS.exists(dir_):
            shutil.rmtree(dir_)

    @staticmethod
    def copyFile2File(filePath, toFilePath, compare=False, shallow=False):
        """
        将文件复制到对应文件路径,
        :param str filePath:
        :param str toFilePath:
        :param bool compare:是否比较
        :return: bool|None 若比较 文件是否相等
        :rtype: bool|None
        """
        if OS.not_exist(filePath):
            raise OSError("文件不存在! {}".format(filePath))
        OS.makedirs(toFilePath, fileDirectory=True)
        if compare:
            # if pl_Hashlib.md5(filePath)==pl_Hashlib.md5(toFilePath):
            if OS.exists(toFilePath):
                if filecmp.cmp(filePath, toFilePath, shallow=shallow):
                    return True
                else:
                    shutil.copyfile(filePath, toFilePath)
                    return False
            else:
                shutil.copyfile(filePath, toFilePath)
                return False
        else:
            shutil.copyfile(filePath, toFilePath)
        return False

    @staticmethod
    def copyFile2Dir(filePath, destinationDirectory, isForce=True):
        """
        将文件复制到指定目录
        :param filePath:
        :param destinationDirectory:
        :param isForce:
        :return:
        """
        if OS.exists(filePath) and OS.isfile(filePath):
            OS.makedirs(destinationDirectory)
            targetFile = OS.join(destinationDirectory, OS.basename(filePath, suffix=True))
            if OS.unixpath(filePath).lower() == OS.unixpath(targetFile).lower():
                return targetFile

            if not OS.exists(targetFile):
                shutil.copy(filePath, destinationDirectory)
            else:
                if isForce:
                    "因为有可能是只读的,就动不了.."
                    OS.chmod(targetFile, 0o666)
                    OS.remove(targetFile)

                    shutil.copy(filePath, destinationDirectory)

            return targetFile

        else:
            if not OS.exists(filePath):
                raise AttributeError("filePath %s not found,skipped" % filePath)
            else:
                raise AttributeError("filePath must be a file,not %s" % filePath)


class DateTime:
    @staticmethod
    def now(stringFormat=True, isFloatPrecision=False):
        """
        获取当前格式化的时间
        :param bool stringFormat:使用自带的 格式化字符串
        :param bool isFloatPrecision:精确到浮点数
        :return: str
        :rtype: str
        """
        if stringFormat:
            if isFloatPrecision:
                return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        else:
            return datetime.datetime.now()

    @staticmethod
    def today():
        """
        获取今天的格式化时间
        :return: str
        :rtype: str
        """
        return datetime.datetime.now().strftime("%Y_%m_%d")

def ls_joinPaths(*args):
    joined = "/".join(args)
    if joined[0]!="/":
        joined = "/"+joined
    return joined
