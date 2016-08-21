#/usr/bin/env python
__author__ = 'wenchong'

import getpass
import sys

def get_all_user():
    """
    获取用户信息，并存储在 all_user_info 字典中返回
    """
    all_user_info = []
    with open('userinfo') as users_info:
        for user_info in users_info:
            info = {}
            user_info = user_info.strip().split(":")
            info['name'] = user_info[0]
            info['pwd'] = user_info[1]
            info['status'] = user_info[2]
            all_user_info.append(info)
    return all_user_info

def lock_user(name):
    """
    锁定用户，即在用户行的最后增加 "!"， 如已经用户已经锁定则跳过
    """
    user_info = open('userinfo').readlines()
    for i in range(len(user_info)):
        if user_info[i].startswith("%s:" % name):
            if user_info[i].endswith(":!") or user_info[i].endswith(":!\n"):
                break
            if i == len(user_info) -1:
                user_info[i] = user_info[i].strip()+"!"
            else:
                user_info[i] = user_info[i].strip()+"!"+"\n"
    user_file = open('userinfo','w')
    user_file.writelines(user_info)
    user_file.close()

def check(username,password):
    """
    检查用户名信息，如用户已被锁定，则返回 lock，否则再次检查用户名密码是否匹配，如匹配返回 success，否则返回 error
    """
    all_user_info = get_all_user()
    for info in all_user_info:
        if info['name'] == username:
            if info['status'] == "!":
                print("用户已被锁定，请联系管理员解锁账号")
                return "lock"
            if info['pwd'] == password:
                print("欢迎来到美丽的天堂")
                return "success"
    return 'error'



def login():
    username = input("请输入用户名： ").strip()
    for i in range(3):
        password = getpass.getpass("请输入密码：").strip()

        status = check(username,password)
        if status == 'lock'  or status == 'success':
            break
        else:
            print("用户名或密码错误，请重新输入！")
    else:
        lock_user(username)
        print("三次密码错误，账号已被锁定")

def main():
    login()

if __name__ == '__main__':
    main()
