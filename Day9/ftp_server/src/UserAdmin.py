# /user/bin/env python
__author__ = 'wenchong'


import os
import getpass

from lib.commons import pkl_load_dump, md5_str, log_write
from config import setting


class User(object):
    """FTP User Info"""
    def __init__(self, username, password, homedir, quota):
        self.username = username
        self.password = password
        self.homedir = homedir
        self.quota = quota


class UserAdmin(object):

    def __init__(self):
        self.pkl_file = setting.USER_FILE
        self.user_db = pkl_load_dump(self.pkl_file, 'load')

    @staticmethod
    def __fetch_password():
        while True:
            password1 = getpass.getpass("密码:")
            password2 = getpass.getpass("密码确认:")
            if password1 == password2:
                return md5_str(password1)
            else:
                print("\n两次密码不一致，请重新输入！！！\n")

    @staticmethod
    def __fetch_quota():
        """获取磁盘配置"""
        while True:
            quota = input("配额(MB):").strip()
            try:
                quota = int(quota)*1024*1024
                return quota
            except:
                continue

    def __is_registered(self, username):
        if username in self.user_db:
            return True
        return False

    def user_register(self):
        """注册用户"""
        username = input("用户名:")

        if self.__is_registered(username):
            print("用户名已经存在，请重新注册")
            input("按回车键继续")
            return False

        password = self.__fetch_password()

        # 磁盘配额
        quota = self.__fetch_quota()

        homedir = username

        # 创建用户对象
        user = User(username, password, homedir, quota)
        # 更新到文件
        self.user_db.update({username: user})

        # 创建用户目录
        if not os.path.isdir(os.path.join(setting.HOMEDIR,username)):
            os.mkdir(os.path.join(setting.HOMEDIR,username))
        log_write("user [%s] is registered" % username)
        pkl_load_dump(self.pkl_file, 'dump', pkl_data=self.user_db)

    def login(self, username, password):
        """用户登录，返回 user 对象"""
        if not self.__is_registered(username):
            log_write("user [%s] is not exist." % username)
            return False

        user = self.user_db.get(username)
        if user.password != md5_str(password):
            log_write("user [%s] login failed by wrong password" % username)
            return False

        return user


def main():
    obj = UserAdmin()
    obj.user_register()


def run():
    try:
        main()
    except:
        pass

if __name__ == '__main__':
    main()