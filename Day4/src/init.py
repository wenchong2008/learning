# /user/bin/env python
__author__ = 'wenchong'

import os
import json
import getpass
from config import setting, templates
from lib import common



def main():
    """
    初始化数据，并创建管理员账号
    """
    # 输出模板信息
    print(templates.credit_card_init)

    # 获取用户名，密码，如两次密码相同，则对密码进行 md5 加密保存，否则退出
    admin_user = input("请输入管理员用户名:").strip().lower()
    first_pwd = getpass.getpass("请输入密码:").strip()
    second_pwd = getpass.getpass("请再次输入密码:").strip()
    if first_pwd == second_pwd:
        password  = common.md5(first_pwd)

        user_info = {
            "admin": {
                admin_user:{
                    'password': password
                }
            },
            "client":{}
        }
        if os.path.isfile(setting.CREDIT_USER):
            json.dump(user_info,open(setting.CREDIT_USER,'w'))
        else:
            json.dump(user_info,open(setting.CREDIT_USER,'x'))

        common.log_write("系统初始化，成功创建管理员用户[{}]".format(admin_user))
    else:
        print("两次密码不一致，请重新操作")


def run():
    main()




