# /user/bin/env python
__author__ = 'wenchong'


from src.admin import AdminUser


def main():
    """初始化管理员账号"""
    admin_obj = AdminUser()
    while True:
        if admin_obj.create():
            break


def run():
    try:
        main()
    except:
        exit('\n')

