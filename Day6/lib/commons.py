# /user/bin/env python
__author__ = 'wenchong'


import logging
from config import setting

def md5(str):
    """对字符串进行 md5 加密"""
    import hashlib
    m = hashlib.md5(bytes("WenChong",encoding='utf-8'))
    m.update(bytes(str,encoding='utf-8'))
    return m.hexdigest()


def log_write(msg,level='info'):
    """
    记录日志
    """
    file_handler = logging.FileHandler(filename=setting.LOG_FILE)
    fmt = logging.Formatter(fmt=setting.LOG_FORMAT)
    file_handler.setFormatter(fmt)

    logger = logging.Logger("CreditMall")
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