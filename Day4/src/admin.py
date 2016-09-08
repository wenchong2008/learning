# /user/bin/env python
__author__ = 'wenchong'

import json
import time
import datetime
import getpass
from config import setting, templates
from lib import common

CURRENT_USER_INFO = {"is_authenticated": False,'current_user': None}
USER_INFO = {}


def init():
    """
    初始化全局变量，将信息从文件中读取到全局变量
    """
    user_info = json.load(open(setting.CREDIT_USER))
    USER_INFO.update(user_info)


def create_user():
    """
    创建用户
    """
    # 捕获用户输入的用户名，并检查用户名是否存在，如果用户名存在则重新输入
    while True:
        username =  input('请输入用户名:').strip().lower()

        if not username:
            continue

        if 'client' in USER_INFO:
            if USER_INFO.get('client').get(username):
                print("用户名已经存在，请重新输入")
                continue
        break

    # 捕获用户输入的密码，如果两次密码相同，则对密码进行 md5 加密
    while True:
        passowrd1 = getpass.getpass("请输入密码:").strip().lower()
        passowrd2 = getpass.getpass("请再输入密码:").strip().lower()

        if passowrd1 == passowrd2:
            password = common.md5(passowrd1)
            break
        else:
            continue



    # 捕获用户输入的信用卡额度，如果输入的额度不为数字，或小于0，则重新输入
    while True:
        credit = input("请输入信用卡额度:").strip()
        try:
            credit = int(credit)
            if int(credit) <= 0:
                print("额度不能小于或等于0")
                continue
            break
        except:
            continue

    # 自动生成卡号
    # 如果 USER_INFO 中无用户信息，则生成一个固定号码的卡号，如果有用户信息，则获取所有用户中最大的卡号，加1
    if not USER_INFO.get('client'):
        card_num = setting.CREDIT_CARD_NUM + "00000001"
    else:
        cards = []
        for name in USER_INFO.get('client'):
            cards.append(USER_INFO.get('client').get(name).get('card'))
        card_num = str(int(max(cards)) + 1 )


    # 生成卡号的有效期
    enroll_date = time.strftime("%Y-%m-%d",time.localtime())
    year = int(time.strftime("%Y",time.localtime())) + setting.CREDIT_CARD_EXPIRE
    expire_date = datetime.datetime.now().replace(year=year).strftime("%Y-%m-%d")

    # 组合用户的基本信息
    base_info = {
        'username':username,    # 用户名
        'card':card_num,    # 卡号
        'password':password,    # 密码
        'credit': credit,  # 信用卡额度
        'balance': credit,  # 信用卡余额
        'must_repay': 0,    # 欠款金额
        'enroll_date': enroll_date,
        'expire_date': expire_date,
        'status': 0,  # 0 = normal  1 = locked  2 = 冻结信用卡
        'debt': [],  # 欠款记录
        'record': [],  # 交易记录
    }

    # 将新生成的用户信息写入 USER_INFO 并存入磁盘
    USER_INFO['client'][username] = base_info
    json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))

    common.log_write("用户[{}]成功创建账户:{} 卡号:{} 额度:{} ".format(
        CURRENT_USER_INFO['current_user'],username,card_num,credit,'info'))
    print("用户 [{}] 创建成功\n额度为： {}\n卡号为：{}".format(username,credit,card_num))

    input("输入任意字符返回首页")


def action_user(action='remove'):
    """
    用户操作
    """
    if action == 'remove':
        info = '删除'
    elif action == 'locked':
        info = '冻结'
    elif action == 'unlock':
        info = '解冻'

    if 'client' not in USER_INFO:
        print("目前无任何用户信息")
    else:
        print("\n请输入用户名以及对应的卡号，只有两个信息相符才能{}\n".format(info))
        username = input("用户名:")
        card = input("卡  号:")
        if username not in USER_INFO.get('client'):
            print("用户名不存在")
        else:
            if USER_INFO.get('client').get(username).get('card') == card:

                if action == 'remove':
                    del USER_INFO.get('client')[username]
                elif action == 'locked':
                    USER_INFO.get('client').get(username)['status'] = 1
                elif action == 'unlock':
                    USER_INFO.get('client').get(username)['status'] = 0
                else:
                    pass
                json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))
                common.log_write("用户[{}]成功{}用户:{},卡号:{}".format(CURRENT_USER_INFO['current_user'],info,username,card),'info')
                print("用户 {} 已成功{}。".format(username,info))

            else:
                print("用户名卡号不对应")
    input("输入任意字符返回首页")

def remove_user():
    """
    删除用户
    """
    action_user('remove')


def locked_user():
    """
    锁定用户
    """
    action_user('locked')


def unlock_user():
    """
    解锁用户
    """
    action_user('unlock')


def search_user():
    """
    搜索用户
    """
    user_input = input("请输入:").strip().lower()

    search_list = []
    for username in USER_INFO.get('client'):
        user_info = USER_INFO.get('client').get(username)
        temp_info = ""
        for k in user_info:
            temp_info += str(user_info.get(k)) + " "

        if user_input in temp_info:
            search_list.append(USER_INFO.get('client').get(username))

    print("用户名\t卡号\t\t\t额度\t余额\t注册时间\t过期时间\t状态")
    msg = "{username}\t{card}\t{credit}\t{balance}\t{enroll_date}\t{expire_date}\t{status}"


    for line in search_list:
        line = line.copy()
        if line['status'] == 0:
            line['status'] = '正常'
        elif line['status'] == 1:
            line['status'] = '冻结'
        else:
            line['status'] = '禁用'
        print(msg.format(**line))

    common.log_write("用户[{}]执行了模糊搜索,关键字[{}]".format(CURRENT_USER_INFO['current_user'],user_input))

    input("输入任意字符返回首页")


def exit_system():
    common.log_write("用户[{}]退出系统".format(CURRENT_USER_INFO['current_user']))
    exit()


def main():

    menu = """
    1、创建用户
    2、查询账户
    3、删除用户
    4、冻结用户
    5、解冻账户
    q、退出系统
    """


    action = {
        "1": create_user,
        "2": search_user,
        "3": remove_user,
        "4": locked_user,
        "5": unlock_user,
        "q": exit_system,
    }

    while True:
        print(templates.credit_admin_index.format(user=CURRENT_USER_INFO.get('current_user'),menu=menu))
        user_input = input("请选择:").strip()
        if user_input in action:
            action[user_input]()


def login():
    while True:
        username = input("请输入用户名:").strip().lower()
        password = common.md5(getpass.getpass("请输入密码:").strip())

        admin_users = USER_INFO.get("admin")
        if username not in admin_users:
            msg = "用户[{}]不存在".format(username)
            common.log_write(msg,'warning')
            print(msg)
        else:
            if password == admin_users.get(username).get('password'):
                CURRENT_USER_INFO['is_authenticated'] = True
                CURRENT_USER_INFO['current_user'] = username
                common.log_write("用户[{}]成功登陆系统".format(username))
                return True
            else:
                msg = "用户名[{}]登陆密码错误".format(username)
                common.log_write(msg,'warning')
                print(msg)


def run():
    try:
        init()
        ret = login()
        if ret:
            main()
    except KeyboardInterrupt as err:
        if CURRENT_USER_INFO['current_user']:
            common.log_write("用户[{}]退出系统".format(CURRENT_USER_INFO['current_user']))
        exit("")