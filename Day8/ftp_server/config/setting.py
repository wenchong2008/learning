# /user/bin/env python
__author__ = 'wenchong'


import os

# IP
LISTEN = '127.0.0.1'
PORT = 8888

# 根目录
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)

# 用户文件
USER_FILE = os.path.join(PROJECT_ROOT, 'database','user_db_file')

# 家目录
HOMEDIR = os.path.join(PROJECT_ROOT,'homedir')

# 日志文件
LOG_FILE = os.path.join(PROJECT_ROOT, 'log', 'myFTP.log')

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 日志级别
LOG_LEVEL = 'DEBUG'