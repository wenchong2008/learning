# /user/bin/env python
__author__ = 'wenchong'

import sys
import time
import pickle
import hashlib


def pkl_load_dump(pkl_file, pkl_type, pkl_data=None):
    """通过 pickle 读取和保存文件"""
    if pkl_type == 'load':
        try:
            return pickle.load(open(pkl_file, mode='rb'), encoding='utf8')
        except FileNotFoundError as e:
            return {}
    elif pkl_type == 'dump':
        pickle.dump(pkl_data, open(pkl_file, mode='wb'))


def md5_str(string):
    """ md5 加密字符串"""
    m = hashlib.md5(bytes("WenChong", encoding='utf8'))
    m.update(bytes(string, encoding='utf8'))
    return m.hexdigest()


def select_format(menu_list):
    """选项格式化"""
    print("-"*80)

    for index, item in enumerate(menu_list, start=1):
        print("%s、%s" % (index, item))

    print("-"*80)


def view_bar(num, total):
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


def loading():
    """输出进度条"""
    print("游戏加载。。。")
    for i in range(0, 101):
        time.sleep(0.05)
        view_bar(i, 100)
    print()

