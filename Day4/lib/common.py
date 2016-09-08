# /user/bin/env python
__author__ = 'wenchong'


import random
import logging
from config import setting


def get_chinese_num(uchar):
    """
    计算中文字符的个数
    """
    i = 0
    for utext in uchar:
        if u'\u4e00' <= utext <= u'\u9fa5':
            i += 1
    return i


def create_verification_code():
    """
    生成 4 位随机验证码
    """
    li = []
    for i in range(4):
        r = random.randrange(0,5)
        if r == 1 or r == 3:
            num = random.randrange(0,10)
            li.append(str(num))
        else:
            temp = random.randrange(65,91)
            li.append(chr(temp))

    code = "".join(li)
    return code


def md5(str):
    """
    对字符串进行 md5 加密
    """
    import hashlib
    m = hashlib.md5(str.encode('utf-8'))
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
