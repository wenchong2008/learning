#/usr/bin/env python
__author__ = 'wenchong'

import  getpass

class Login:

    def __init__(self):
        self.userconf_file = 'userinfo'
        self.all_user_info = self.get_users_info()

    def get_users_info(self):
        """
        获取用户信息，并存储在 all_user_info 字典中返回
        """
        all_user_info = {}
        with open(self.userconf_file) as users_info:
            for user_info in users_info.readlines():
                user_info = user_info.strip().split(":")
                info = {
                    'name': user_info[0],
                    'pwd': user_info[1],
                    'status': user_info[2],
                    'home': user_info[3],
                }
                all_user_info[user_info[0]] = info
        return all_user_info

    def lock_user(self,name):
        """
        锁定用户，即在用户行的最后增加 "!"， 如已经用户已经锁定则跳过
        """

        # for user_info in self.all_user_info:
        #     if user_info['name'] == name:
        #         user_info['status'] = '!'
        #         break

        user_info = self.all_user_info.get(name)
        if user_info:
            user_info['status'] = '!'


        user_file = open(self.userconf_file,'w')
        for name in self.all_user_info:

            user_info = ":".join(
                [
                    self.all_user_info[name]['name'],
                    self.all_user_info[name]['pwd'],
                    self.all_user_info[name]['status'],
                    self.all_user_info[name]['home'],
                ])
            user_file.write("%s\n" % user_info)
        user_file.close()

    def check(self,username,password):
        """
        检查用户名信息，如用户已被锁定，则返回 lock，否则再次检查用户名密码是否匹配，如匹配返回 success，否则返回 error
        """

        user_info = self.all_user_info.get(username)
        if user_info:
            if user_info.get('status') == "!":
                print("用户已被锁定，请联系管理员解锁账号")
                return "lock"
            if user_info.get('pwd') == password:
                return username

        return 'error'

        # for info in self.all_user_info:
        #     if info['name'] == username:
        #         if info['status'] == "!":
        #             print("用户已被锁定，请联系管理员解锁账号")
        #             return "lock"
        #         if info['pwd'] == password:
        #             return username
        # return 'error'

    def login(self):
        username = ''
        while not username:
            username = input("请输入用户名： ").strip()
        for i in range(3):
            password = getpass.getpass("请输入密码：").strip()

            status = self.check(username,password)
            if status == 'error':
                continue
            else:
                return status
        else:
            self.lock_user(username)
            print("三次密码错误，账号已被锁定")
            return 'lock'



def main():
    user_login = Login()
    status = user_login.login()
    print(status)

if __name__ == '__main__':
    main()





