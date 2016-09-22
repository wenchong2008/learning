# /user/bin/env python
__author__ = 'wenchong'

import os
PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir)

# 管理员数据库
ADMIN_DB = os.path.join(PROJECT_ROOT,'db/admin')

# 超时
TIMEOUT = 300


# 老师的数据库
TEACHER_DB = os.path.join(PROJECT_ROOT, 'db/teaching')

# 课程数据库
COURSE_DB = os.path.join(PROJECT_ROOT, 'db/course')

# 学生数据库
STUDENT_DB = os.path.join(PROJECT_ROOT, 'db/student')

# 日志文件
LOG_FILE = os.path.join(PROJECT_ROOT, 'log/select.log')

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 日志级别
LOG_LEVEL = 'DEBUG'