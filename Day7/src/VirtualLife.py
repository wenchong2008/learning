# /user/bin/env python
__author__ = 'wenchong'


from config import setting
from src.GameUserAdmin import UserAdmin
from src.GameChangeLife import ChangeLife
from lib.commons import select_format, loading


def after(user):
    """用户第一次进入，剧情简介"""
    msg = """
    村长:
        Hi，{0} 欢迎来到屌丝逆袭游戏.

    #######################################################################
    # 你的女朋友 Liz: {0} 我们分手吧！
    #
    # {0}: .....
    #
    # {0}: 为什么？难道我对你不好吗？我们不是说好一起毕业，一起努力，一起生活的吗？
    #
    # 你的女朋友 Liz: 我觉得我们不合适，你是一个好人
    #
    # {0}: .....
    #
    # 你的女朋友 Liz：我找到了我的真爱，我很爱 Peter, 他对我很好
    #
    # {0}: ....
    #######################################################################


    于是乎你决定努力奋斗，追回 Liz 。。。

    """.format(user.name)

    print(msg)


def login_select(user_admin, menu_list):
    """程序运行后选项"""
    while True:
        select_format(menu_list)
        login_choice = input("请选择:")

        if login_choice not in map(str, range(1, len(menu_list) + 1)):
            continue

        if login_choice == "1":
            user_admin.user_register()
            continue

        elif login_choice == "2":
            user = user_admin.login()
            if user:
                return user
            continue

        else:
            exit()


def change_life_scene(user, user_db, user_db_file, menu_list):
    """通过努力改变生活部分"""
    while True:
        change_life = ChangeLife(user, user_db, user_db_file)
        # 当用户在场景 1 时
        if user.scene == 1:
            loading()
            while True:
                select_format(menu_list)
                choice = input("请选择:")

                if choice not in map(str, range(1, len(menu_list) + 1)):
                    continue

                if choice == '1':
                    change_life.change_work()

                elif choice == '2':
                    change_life.make_money()

                elif choice == '3':
                    change_life.buy_car()

                elif choice == '4':
                    change_life.buy_house()

                elif choice == '5':
                    change_life.show_info()

                elif choice == '6':
                    change_life.change_second_scene()

                elif choice == '7':
                    exit("\n再见, %s 您已经退出了游戏\n" % user.name)
        # 其他场景
        else:
            change_life.second_scene()


def main():
    login_menu = ["注册账号", "登陆游戏", "退出游戏"]
    change_life_menu = ["换个工作", "努力赚钱", "购买汽车", "购买房子", "查看信息", "下一场景", "退出游戏"]
    user_db_file = setting.USER_DB_FILE
    user_admin = UserAdmin(user_db_file)

    print("%s" % "#"*80)
    print("\n\t\t\t欢迎访问模拟人生游戏，体验屌丝逆袭的道路....\n")
    print("%s" % "#"*80)
    # 验证登录，返回 user 对象
    user = login_select(user_admin, login_menu)
    if not user:
        return False

    print("%s" % "-"*80)
    print("\n\t\t\t\t逆袭之路由此开始\n")
    print("%s" % "-"*80)

    # 如果为场景 0，则加载剧情简介
    if user.scene == 0:
        loading()
        after(user)
        user.scene = 1
    # 改变人生场景
    change_life_scene(user, user_admin.user_db, user_db_file, change_life_menu)


def run():
    try:
        main()
    except KeyboardInterrupt as e:
        exit("\n\n您已经退出了游戏\n")

    except Exception as e:
        print("异常退出: %s" % e)

