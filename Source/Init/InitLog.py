import logging
from logging.handlers import RotatingFileHandler

def fmt_filter(record):
    record.levelname = '[%s]' % record.levelname
    record.funcName = '[%s]' % record.funcName
    return True
def init_logger(file_path):
    logger = logging.getLogger(name=__name__)  # 不加名称设置root logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)05d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # 添加 %f 以包含微秒
    )
    logger.addFilter(fmt_filter)
    # 使用FileHandler输出到文件
    # fh = logging.FileHandler(file_path, encoding='utf-8')


    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # # 写入文件，如果文件超过100个Bytes，仅保留5个文件。
    rh = RotatingFileHandler(
        file_path, maxBytes=1024*1024, backupCount=5,encoding='utf-8')
    rh.setLevel(logging.DEBUG)
    rh.setFormatter(formatter)
    # 设置后缀名称，跟strftime的格式一样
    logger.addHandler(rh)


    # 添加两个Handler
    logger.addHandler(ch)
    # logger.addHandler(fh)


    return logger
