# /user/bin/env python
__author__ = 'wenchong'


import time
import sys


def view_process(num, total):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    # \r 表示将指针移动到开始
    n = int(rate_num/2)
    s = "%s%s" %("="*n, rate_num)
    r = '\r%s%%' % (s, )
    # 输出时不换行
    sys.stdout.write(r)
    # 刷新输出内容
    sys.stdout.flush()


def md5_file(file):
    """获取文件的 md5"""
    import hashlib
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()


