# /user/bin/env python
__author__ = 'wenchong'

import getpass
from lib.commons import md5_str, pkl_load_dump


class User(object):
    """用户信息"""
    country = "中国"
    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
        self.asset = 0
        self.wages = 0
        self.house = None
        self.car = None
        self.job = None
        self.scene = 0


class UserAdmin(object):
    """用户管理"""
    def __init__(self, user_db_file):
        self.pkl_file = user_db_file
        self.user_db = pkl_load_dump(self.pkl_file, 'load')

    @staticmethod
    def __fetch_password():
        """获取密码并进行 md5 加密"""
        while True:
            password1 = getpass.getpass("密码:")
            password2 = getpass.getpass("确认密码:")
            if password1 == password2:
                password = md5_str(password1)
                return password

    def __is_registered(self, username):
        """确认用户是否已被注册"""
        if username in self.user_db:
            return True
        return False

    def user_register(self):
        """注册用户"""
        print("---------- 新用户注册 ----------")

        username = input("用户名:")

        if self.__is_registered(username):
            print("用户名已经存在，请重新注册")
            input("按回车键继续")
            return False

        password = self.__fetch_password()
        name = input("姓名:")
        # 创建用户对象
        user = User(username, password, name)
        # 更新到文件
        self.user_db.update({username: user})
        pkl_load_dump(self.pkl_file, 'dump', pkl_data=self.user_db)

    def login(self):
        """用户登录，返回 user 对象"""
        username = input("用户名:")
        password = getpass.getpass("密码:")

        if not self.__is_registered(username):
            print("用户名不存在，请重新登录！！！")
            return False

        user = self.user_db.get(username)
        if user.password != md5_str(password):
            print("密码错误，请重新登录！！！")
            return False

        return user



