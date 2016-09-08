# /user/bin/env python
__author__ = 'wenchong'

import sys
import os.path

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir)


# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 日志级别
LOG_LEVEL = 'DEBUG'
# logger.setLevel(logging._levelNames[Log_Level])

# 日志文件
LOG_FILE = os.path.join(PROJECT_ROOT,'log/credit.log')

# 信用卡用户信息
CREDIT_USER = os.path.join(PROJECT_ROOT,'db/credit_user.json')

# 信用卡卡号开头
CREDIT_CARD_NUM = '62257687'

# 信用卡失效年份
CREDIT_CARD_EXPIRE = 3

# 信用卡账户密码最大尝试次数
CREDIT_PWD_RETRY = 3

# 信用卡账单日
CREDIT_BILL_DAY = 22

# 信用卡还款日
CREDIT_REPAY_DAY = 1

