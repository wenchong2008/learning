# -*- coding:utf-8 -*-

"""
__auther:super
this program must run in python2.X
"""
import re
import os
import json
from getpass import getpass

# 保存用户金额变量
USER_ACCOUNT = 0
# 保存用户购物车商品
USER_SHOPPING_CART = []
# 用户登陆标识
USER_LOGIN_STATUS = False
USER_NAME = ''
# 用户账户信息数据库
USER_INFO = os.path.join(os.path.dirname(os.path.abspath('__file__')),'userinfo.txt')


# 欢迎信息
def print_welcome_menu():
    menu_list = "=====================================================\n" \
                "=                                                   =\n" \
                "=              WELCOME TO SHOPPING MARKET           =\n" \
                "=                                                   =\n" \
                "=====================================================\n"
    return menu_list


def print_choose_menu():
    choose_menu = "\n1. 进入购物商城\n" \
                  "2. 查看账户余额\n" \
                  "3. 查看购物车\n"\
                  "4. 给账户充值\n" \
                  "5. 退出系统"
    return choose_menu


# 商品信息
def goods_list():
    goodslist = (
        {'no': '001', 'name': '联想笔记本电脑', 'price': 5000},
        {'no': '002', 'name': '手机Iphone 6S', 'price': 3000},
        {'no': '003', 'name': '耐克篮球鞋', 'price': 700},
        {'no': '004', 'name': 'Python源码分析', 'price': 80},
        {'no': '005', 'name': '三星固态硬盘', 'price': 1000},
    )
    return goodslist


# 获取汉字个数
def get_chinese_num(uchar):
    i = 0
    for utext in uchar:
        if u'\u4e00' <= utext <= u'\u9fa5':
            i += 1
    return i


# 打印商品信息
def print_goods_list(lists):
    """
    此功能模块用来打印商品信息，包括打印商场的所有商品信息、用户的购物车中的商品信息
    :param lists: 保存商品的变量(list类型) goodslist
    :return: 返回格式化后的菜单
    """
    _goodlist = lists
    print('\n|' + '商品编号'.center(16) + '|' + '商品名称'.center(23) + '|' + '商品价格(RMB)'.center(22) + '|')
    print('%s' % '-' * 53)
    for goods in _goodlist:
        chinese_num = get_chinese_num(goods['name'].decode('utf-8'))
        len_name = len(goods['name'].decode('utf-8'))
        space_str = (19 - len_name - chinese_num) * " "
        print('|%-12s|%s|%18s|' % (goods['no'], goods['name'] + space_str, str(goods['price'])))


# 登陆认证装饰器
def user_auth(func_name):
    def login(*args):
        global USER_ACCOUNT, USER_LOGIN_STATUS, USER_NAME
        if not USER_LOGIN_STATUS:
            print('请先登陆账号!')
            with open(USER_INFO,'r') as f:
                user_Info = json.loads(f.read())
                user_list = user_Info.keys()
            while not USER_LOGIN_STATUS:
                user_name = raw_input('请输入账户用户名:').strip().lower()
                user_passwd = getpass('请输入账户密码:')

                if user_name in user_list:
                    if user_passwd == user_Info[user_name]['password']:
                        USER_ACCOUNT = user_Info[user_name]['balance']
                        USER_NAME = user_name
                        USER_LOGIN_STATUS = True
                        print('\n登陆成功!\n')
                    else:
                        print('\n账号密码不正确,请重新输入!')
                        continue
                else:
                    print('\n账号不存在!')

        func_name(*args)
    return login


# 保存账户余额到文件
def update_user_info():
    global USER_NAME
    with open(USER_INFO,'r') as fr:
        user_info = json.loads(fr.read())
    user_info[USER_NAME]['balance'] = USER_ACCOUNT
    with open(USER_INFO,'w+') as fw:
        fw.write(json.dumps(user_info))


# 根据商品编号判断商品是否存在
def check_goods_id_exist(gid):
    """
    检测输入的商品编号是否存在
    :param gid: 用户输入的商品编号
    :return: 存在状态：True/False
    """
    is_exist_flag = False
    for goods in goods_list():
        if goods['no'] == gid:
            is_exist_flag = True
    return is_exist_flag


# 根据商品编号获取商品
def get_goods_by_gid(gid):
    """
    获取商品信息模块：根据用户输入商品编号获取商品信息
    :param gid: 商品编号
    :return: 商品信息字典 {'no': '004', 'name': 'Python源码分析', 'price': 80}
    """
    _good_list = goods_list()
    for goods in _good_list:
        if goods['no'] == gid:
            return goods


# 给账户充值
@user_auth
def count_add_momey():
    """
    账户充值模块：默认账户余额为0，USER_ACCOUNT 全局变量
    :return:
    """
    global USER_ACCOUNT
    add_money = raw_input('请输入您要充值的金额:').strip()

    # 输入必须为数字，检查是否合法
    while len(re.findall('[^0-9]', add_money)) > 0:
        print('\n\033[1;31m输入的金额不合法,必须为数字,请重新输入\033[0m!\n')
        add_money = raw_input('请输入您要充值的金额:').strip()

    USER_ACCOUNT += int(add_money)
    # 更新账户余额
    update_user_info()
    print('\n\033[1;32m充值成功! 您当前的账户余额为: %d 元 \033[0m\n' % USER_ACCOUNT)


# 购物车结算
@user_auth
def pay_for_shopping_cart(list_goods):
    """
    对购物车的商品进行结算,如果结算成功返回True，否则返回False
    :param list_goods: 购物车列表
    :return: True / False
    """
    global USER_ACCOUNT,USER_SHOPPING_CART
    total_fee = 0
    return_flag = False

    if not list_goods:
        print('\n\033[1;31m您当前的购物车无任何商品信息！\033[0m\n')
    else:
        # 开始对购物车的商品计算总费用
        for goods in list_goods:
            total_fee += goods['price']
        # 账户金额够的话开始扣费
        if USER_ACCOUNT >= total_fee:
            USER_ACCOUNT -= total_fee

            # 更新文件中的账户余额信息
            update_user_info()
            print('\n\033[1;32m商品结算成功!,共消费 %d 元,账户余额 %d 元\033[0m\n' % (total_fee,USER_ACCOUNT))

            # 结算成功后本次的购物车将清空,可以写入日志文件做历史记录,此功能没做
            USER_SHOPPING_CART = []
            return_flag = True
        else:
            print('\n\033[1;31m余额不足!您当前账户余额为 %d,无法结算,请先充值!\033[0m\n' % USER_ACCOUNT)

    return return_flag


@user_auth
def get_user_account():
    global USER_ACCOUNT
    print('\n\033[1;32m您当前的账户余额为 %d 元.\033[0m\n' % USER_ACCOUNT)


# 购物模块
def do_shopping():
    """
    商品购物模块,将选择的商品加入到购物车,并进行商品结算
    :return:
    """
    global USER_ACCOUNT
    # 是否继续购买商品标示
    choose_loop_flag = True

    while choose_loop_flag:
        # 打印商品菜单列表
        print_goods_list(goods_list())
        goods_no = raw_input('\n请选择要购买的商品编号(quit 返回主菜单): ').strip().lower()

        # 退出购物菜单，返回主功能菜单
        if goods_no == "quit":
            choose_loop_flag = False
            continue

        # 如果输入的商品编号不存在
        if not check_goods_id_exist(goods_no):
            print('\n\033[1;31m您输入的商品编号不存在,请重新选择\033[0m\n')
            continue
        else:
            # 获得商品信息
            choose_goods = get_goods_by_gid(goods_no)

            # 将商品保存到购物车
            USER_SHOPPING_CART.append(choose_goods)
            goods_count_in_cart = len(USER_SHOPPING_CART)
            # 打印购物车信息
            print_goods_list(USER_SHOPPING_CART)

            goon_shop_flag = raw_input(
                '\n已加入购物车,当前共%d件商品,是否继续购买[y/n]:' % goods_count_in_cart).strip().lower()
            if goon_shop_flag == 'n':
                choose_loop_flag = False
                continue
    # 如果购物车不为空
    if USER_SHOPPING_CART:
        pay_or_quit_flag = raw_input('\n 现在结算商品吗(y/n)?不结算将返回功能菜单!')
        if pay_or_quit_flag == "y":
            pay_for_shopping_cart(USER_SHOPPING_CART)


# 开始主程序
if __name__ == "__main__":
    # 用户退出系统标识
    exit_sys_flag = True
    print(print_welcome_menu())

    while exit_sys_flag:
        # 显示功能主菜单
        print(print_choose_menu())
        choose = raw_input('\n请选择功能编号[1-5]:')

        # 选择退出系统? 退出循环
        if choose == "5":
            exit_sys_flag = False
            continue

        # 不在选择的菜单中，重新选择
        if choose not in ('1', '2', '3', '4'):
            print('\n您选择的功能编号不存在,请重新选择！\n')
            continue

        # 选择购物菜单
        if choose == "1":
            do_shopping()
            continue

        # 选择查看账户余额
        if choose == "2":
            get_user_account()
            continue

        # 查看购物车
        if choose == "3":
            if len(USER_SHOPPING_CART) > 0:
                print_goods_list(USER_SHOPPING_CART)
                pay_flag = raw_input('\n现在要结算吗?(y/n):').strip().lower()
                if pay_flag == 'y':
                    pay_for_shopping_cart(USER_SHOPPING_CART)
            else:
                print('\n\033[1;31m您当前的购物车无任何商品信息！\033[0m\n')
            continue

        # 账户充值
        if choose == "4":
            count_add_momey()
            continue
