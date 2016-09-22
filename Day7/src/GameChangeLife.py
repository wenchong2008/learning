# /user/bin/env python
__author__ = 'wenchong'

import re

from lib.commons import pkl_load_dump, select_format, loading


def callback(func):
    def wrapper(self, *args):
        ret = func(self, *args)
        pkl_load_dump(self.user_db_file, 'dump', self.user_db)
        return ret
    return wrapper


class ChangeLife(object):
    """通过努力改变人生部分"""

    def __init__(self, user, user_db, user_db_file):
        self.user = user
        self.user_db = user_db
        self.user_db_file = user_db_file

    @callback
    def change_work(self):
        """换工作"""

        work_menu = [
            "运维开发  ---- 20000",
            "JAVA开发  ---- 20000",
            "Perl开发  ---- 20000",
            "WEB开发  ---- 20000",
            ]

        for index, item in enumerate(work_menu, start=1):
            print("%s、%s" % (index, item))

        while True:
            choice = input("请选择:")
            if choice not in map(str, range(1, len(work_menu) + 1)):
                continue

            work = work_menu[int(choice) - 1]
            self.user.job, self.user.wages = re.split('\s+-+\s+',work)

            print("\n找到新的工作了，职位: %s, 工资: %s\n" % (self.user.job, self.user.wages))
            input("按回车键继续")
            break

    def __check_job(self):
        """确认工作"""
        if not self.user.job:
            print("\n请先选择一个工作！！！\n")
            input("按回车键继续")
            return False
        return True

    def __check_asset(self):
        """确认资产"""
        if not self.user.asset > 20000:
            print("\n请先工作一段时间，攒点钱。。。。\n")
            input("按回车键继续")
            return False
        return True

    @callback
    def make_money(self):
        """赚钱，粗略"""
        if self.__check_job():
            self.user.asset += int(self.user.wages)
            print("\n时间过去一段时间，恭喜您的资产增加 %s\n" % self.user.wages)
            input("按回车键继续")

    @callback
    def buy_car(self):
        """买车，粗略"""
        if self.__check_job() and self.__check_asset():
            if not self.user.car:
                self.user.car = "特斯拉 2016款 Model S P100DL"
                print("\n恭喜您购买了一辆【 特斯拉 2016款 Model S P100DL 】\n")
            else:
                print("\n您已经是有车一族！！！\n")
            input("按回车键继续")

    @callback
    def buy_house(self):
        """买房，粗略"""
        if self.__check_job() and self.__check_asset():
            if not self.user.house:
                self.user.house = "黄浦江边，江景房一套"
                print("\n恭喜您购买了一套【 黄浦江边，江景房 】\n")
            else:
                print("\n您已经有一套房\n")
            input("按回车键继续")

    def show_info(self):
        """显示角色信息"""
        print("--------- 角色信息 ---------")
        print("""
        用户名: %s
        姓名: %s
        资产: %s
        工资: %s
        房子: %s
        车子: %s
        工作: %s
        场景: 第 %s 部分
        """ % (
            getattr(self.user, "username"),
            getattr(self.user, "name"),
            getattr(self.user, "asset"),
            getattr(self.user, "wages"),
            getattr(self.user, "house", "无"),
            getattr(self.user, "car", "无"),
            getattr(self.user, "job", "无"),
            getattr(self.user, "scene"),
                            ))

        input("按回车键继续")

    @callback
    def second_scene(self):
        """第二场景"""
        menu_list = ["重现剧情", "返回上一场景", "退出游戏"]
        msg = """

        你通过努力，终于成为了一名合格的高富帅，，，，

        某天，你在同学聚会上碰到了 Liz。。。

        {0}: 最近过的还好吗？
        Liz: 不好，和你分手之后没多久，我就看清了 Peter 的真面目，他还有好几个女朋友
        {0}: ....
        Liz: {0}, 我们还能像一起说好的那样吗？
        {0}: ....
        ......

        后续剧情请关注 屌丝逆袭2

        """.format(self.user.name)
        loading()
        print(msg)

        while True:
            select_format(menu_list)

            choice = input("请选择:")

            if choice not in map(str, range(1, len(menu_list) + 1)):
                continue

            if choice == '1':
                print(msg)

            elif choice == '2':
                self.change_first_scene()
                return
            else:
                pkl_load_dump(self.user_db_file, 'dump', self.user_db)
                # print(self.user_db[self.user.username].scene)
                exit("\n再见, %s 您已经退出了游戏\n" % self.user.name)
                # return "exit"

    @callback
    def change_second_scene(self):
        """进入下一场景"""
        if self.user.asset > 20000 and self.user.house and self.user.car:
            self.user.scene = 2
            self.second_scene()

        else:
            print("\n你还是一个屌丝，继续努力吧。。。。。\n")
            input("按回车键继续")

    @callback
    def change_first_scene(self):
        """返回上一场景"""
        if self.user.scene == 2:
            self.user.scene = 1