# /user/bin/env python
__author__ = 'wenchong'


import pickle
import hashlib
import logging
from config import setting


def pkl_load_dump(pkl_file, pkl_type, pkl_data=None):

    if pkl_type == 'load':
        try:
            return pickle.load(open(pkl_file, mode='rb'), encoding='utf-8')
        except Exception as e:
            log_write(e)
            return {}
    elif pkl_type == 'dump':
        pickle.dump(pkl_data, open(pkl_file, mode='wb'))


def md5_str(string):

    m = hashlib.md5(bytes('WenChong', encoding='utf-8'))
    m.update(bytes(string, encoding='utf-8'))
    return m.hexdigest()


def md5_file(file):
    """获取文件的 md5 值"""
    m = hashlib.md5()
    with open(file, mode='rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()


def log_write(msg,level='info'):
    """
    记录日志
    """
    file_handler = logging.FileHandler(filename=setting.LOG_FILE)
    fmt = logging.Formatter(fmt=setting.LOG_FORMAT)
    file_handler.setFormatter(fmt)

    logger = logging.Logger("MyFTP")
    logger.setLevel(logging._nameToLevel[setting.LOG_LEVEL])
    logger.addHandler(file_handler)

    logger_dict = {
        'info':logger.info,
        'debug':logger.debug,
        'critical':logger.critical,
        'warning':logger.warning,
        'error':logger.error,
        }
    if level in logger_dict:
        logger_dict[level](msg)
    else:
        msg = "[level:{}]不存在 msg:".format(level) + msg
        logger.warning(msg)
