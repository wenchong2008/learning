# /user/bin/env python
__author__ = 'wenchong'


import json
import time
import getpass
from lib import common
from config import setting, templates

CURRENT_USER_INFO = {"is_authenticated": False,'current_user': None}
USER_INFO = {}


def init():
    """
    初始化全局变量，将信息从文件中读取到全局变量
    """
    user_info = json.load(open(setting.CREDIT_USER))
    USER_INFO.update(user_info)


def statement(username,money):
    """
    信用卡还款，删除账单
    """

    user_info = USER_INFO.get('client').get(username)

    # 该用户所有的账单信息，账单的顺序为从旧到新
    debts = user_info.get('debt')

    # 遍历所有的账单信息，如果存款金额大于等于账单信息则删除该账单
    for debt in debts:
        if money >= debt['statement_bill']:
            debts.remove(debt)
            money = money - debt['statement_bill']
    # 写入文件
    json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))


def record_add(action,money,username=None,commission=0,description=""):
    """
    添加交易记录
    :param action: 交易类型
    :param money: 交易金额
    :param username: 用户名
    :param commission: 手续费
    :param description: 描述信息
    """
    # 定义记录格式
    record = {
        'time': time.strftime("%Y-%m-%d %H:%M:%S"),
        'action': action,
        'money': money,
        'commission': commission,
        'description': description,
    }
    if not username:
        username = CURRENT_USER_INFO['current_user']
    # 添加记录到 record 列表字段，并写入文件
    USER_INFO['client'][username]['record'].append(record)
    json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))

def transfer():
    """
    转账给其他用户
    """
    print("\n请输入用户名以及对应的卡号，只有两个信息相符才能转账\n")
    to_user = input("用户名:")
    to_card = input("卡  号:")

    # 判断用户是否存在
    if to_user not in USER_INFO.get('client'):
        print("对方用户名不存在")
    else:
        # 判断用户对应的卡号是否相同
        if to_card != USER_INFO.get('client').get(to_user).get('card'):
            print("用户名卡号不匹配，无法操作")
        else:
            # 获取转账金额
            while True:
                to_num = input("请输入转账金额:")
                try:
                    to_num = float(to_num)
                    break
                except:
                    continue
            # 判断用户余额是否大于需要转账的金额
            if USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).get('balance') < to_num:
                print("您的信用卡余额不足，无法进行转账")
            else:
                # 登陆用户的余额减少，对方用户余额增加
                USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user'))['balance'] -= to_num
                USER_INFO.get('client').get(to_user)['balance'] += to_num
                # 为两个用户记录交易信息
                record_add(action='转账',money=to_num,description='给{}转账'.format(to_user))
                record_add(
                    action='存入',money=to_num,username=to_user,
                    description='从{}转入'.format(CURRENT_USER_INFO['current_user'])
                )
                # 修改两个用户的 must_repay 字段
                USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user'))['must_repay'] += to_num
                statement(to_user,to_num)
                USER_INFO.get('client').get(to_user)['must_repay'] -= to_num
                # 写入日志
                json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))
                common.log_write("用户[{}]成功给[{}]转账[{}],手续费[0]".format(CURRENT_USER_INFO['current_user'],to_user,to_num))
                print("成功给[{}]转账[{}],手续费[0]".format(to_user,to_num))

    input("输入任意字符返回首页")


def withdraw():
    """
    提现
    """
    # 获取提现金额
    while True:
        num = input("请输入需要提现的金额:").strip()
        try:
            num = float(num)
            break
        except:
            continue

    # 允许提现的金额为信用额度的 50%
    allow_withdraw_num = USER_INFO.get('client').get(CURRENT_USER_INFO['current_user']).get('credit') * 0.5
    # 判断提现金额是否大于允许提现金额
    if num > allow_withdraw_num:
        print("您的的提现金额不能超过额度的 50%")
    else:
        # 判断提现金额与手续费相加是否大于余额
        if num * 1.05 > USER_INFO.get('client').get(CURRENT_USER_INFO['current_user']).get('balance'):
            print("您的信用卡余额不足，无法提现")
        else:
            # 用户余额减去提现金额与手续费
            USER_INFO.get('client').get(CURRENT_USER_INFO['current_user'])['balance'] -= round(num * 1.05,2)
            commission= round(num * 0.05,2)
            # 用户 must_repay 字段增加提现金额与手续费
            USER_INFO.get('client').get(CURRENT_USER_INFO['current_user'])['must_repay'] += round(num * 1.05,2)

            # 记录交易信息，以及日志，并写入文件
            record_add(action='提现',money=num,commission=commission)
            json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))
            common.log_write("用户[{}]成功提现[{}],手续费[{}]".format(CURRENT_USER_INFO['current_user'],num,commission))
            print("您已成功提现[{}],手续费[{}]".format(num,commission))

    input("输入任意字符返回首页")




def repay():
    """
    还款
    """
    while True:
        num = input("请输入还款金额")
        try:
            num = float(num)
            break
        except:
            continue

    USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user'))['balance'] += num
    USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user'))['must_repay'] -= num
    record_add(action='存入',money=num)
    statement(CURRENT_USER_INFO.get('current_user'),num)
    json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))
    common.log_write("用户[{}]成功还款[{}]元".format(CURRENT_USER_INFO['current_user'],num))
    print("还款成功")

    input("输入任意字符返回首页")


def account_info():
    """
    查看账户信息
    """

    user_info = USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).copy()
    if user_info['status'] == 2:
        user_info['status'] = "冻结"
    elif user_info['status'] == 0:
        user_info['status'] = "正常"
    print(templates.account_info.format(**user_info))
    common.log_write("用户[{}]查询了信息".format(CURRENT_USER_INFO['current_user']))

    input("输入任意字符返回首页")


def pay_check():
    """
    查看账单信息
    """
    statement_reports = USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).get('debt')

    print(templates.credit_statement_report.format(
        card=USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).get('card'))
    )
    print("开始时间\t结束时间\t账单日\t还款日\t需还款")
    for statement_report in statement_reports:
        print("{startdate}\t{enddate}\t{billdate}\t{statement_pdate}\t{statement_bill}\n".format(**statement_report))

    common.log_write("用户[{}]查询了账单".format(CURRENT_USER_INFO['current_user']))

    input("输入任意字符返回首页")

def record_show():
    """
    查看交易详情
    """

    print(templates.credit_statement_detail.format(
        card=USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).get('card'))
    )
    record_lists = USER_INFO.get('client').get(CURRENT_USER_INFO.get('current_user')).get('record')
    for record in record_lists:
        print("{time}\t{action}\t\t{money}\t{commission}\t{description}".format(**record))

    print()

    common.log_write("用户[{}]查询了交易记录".format(CURRENT_USER_INFO['current_user']))

    input("输入任意字符返回首页")

def main():

    menu = """
    1、我的信用卡
    2、提现
    3、转账
    4、还款
    5、账单
    6、交易记录
    q、退出
    """

    action = {
        "1": account_info,
        "2": withdraw,
        "3": transfer,
        "4": repay,
        "5": pay_check,
        "6": record_show,
        "q": exit
    }

    while True:
        print(templates.credit_client_index.format(user=CURRENT_USER_INFO.get('current_user'),menu = menu))

        user_input = input("请选择:")
        if user_input in action:
            action[user_input]()


def login():
    while True:
        username = input("请输入用户名:").strip().lower()
        password = common.md5(getpass.getpass("请输入密码:").strip())

        if 'client' not in USER_INFO:
            print("系统中暂时无用户信息")
        else:
            client_user = USER_INFO.get('client')
            if username not in client_user:
                msg = "用户[{}]不存在".format(username)
                common.log_write(msg,'warning')
                print(msg)

            else:
                if client_user.get(username).get('status') == 1:
                    msg = "用户[{}]已被锁定，请联系管理员".format(username)
                    common.log_write(msg,'warning')
                    print(msg)
                else:
                    if password == client_user.get(username).get('password'):
                        CURRENT_USER_INFO['current_user'] = username
                        CURRENT_USER_INFO['is_authenticated'] = True
                        common.log_write('用户[{}]成功登入系统'.format(username))
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