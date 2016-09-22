# /user/bin/env python
__author__ = 'wenchong'


import os
import sys

# 项目根目录
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)

# 用户数据文件
USER_DB_FILE = os.path.join(PROJECT_ROOT, 'database/user_db_file')

# 用户锁定文件
USER_LOCK_FILE = os.path.join(PROJECT_ROOT, 'database/user_lock_file')