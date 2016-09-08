# /user/bin/env python
__author__ = 'wenchong'


import json
import time
import datetime
from config import setting
from lib import common


USER_INFO = {}


def init():
    """
    对全局变量 USER_INFO 初始化，将数据从文件读取到全局变量
    """
    user_info = json.load(open(setting.CREDIT_USER))
    USER_INFO.update(user_info)


def create_interest():
    """
    计算利息：如果应还金额，must_repay 大于 0，则开始计算利息
        当前日期在最后还款日期之前，使用上一次的账单计算利息。
        当前日期在最后还款日期之后，使用最后一次账单计算利息
    """

    # 无用户信息
    if not USER_INFO.get('client'):
        print("无用户信息，无需生成")
    else:
        # 遍历所有的用户
        for username  in USER_INFO.get('client'):
            user_info = USER_INFO.get('client').get(username)

            if user_info.get('must_repay') <= 0:
                continue

            # 当账单数量大于 0
            if len(user_info.get('debt')) == 0:
                common.log_write("用户[{}]无账单信息".format(username))

            else:
                # 当前日期在最后还款日志之前，使用上个月的账单计算利息，反之使用最后一个账单计算利息
                last_statement = user_info.get('debt')[-1]
                repay_day = last_statement.get('statement_pdate')
                if time.strptime(time.strftime('%Y-%m-%d'),"%Y-%m-%d") > time.strptime(repay_day,"%Y-%m-%d"):
                    common.log_write("用户[{}]的利息账单为 -1".format(username))
                    statement = last_statement
                else:
                    try:
                        statement = user_info.get('debt')[-2]
                        common.log_write("用户[{}]的利息账单为 -2".format(username))
                    except:
                        common.log_write("用户[{}]的利息账单为 0".format(username))
                        statement = ""


                if statement:
                    interest = round(statement.get('statement_bill') * 0.0005,2)
                    user_info['must_repay'] += interest
                    common.log_write("用户[{}]的利息增加{}".format(username,interest))
                else:
                    common.log_write("用户[{}]无利息增加".format(username))

    json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))



def create_card_statement():
    """
    生成账单
    """

    # 检查今天是否为账单日，无不为账单日则不生成账单，直接返回
    if time.localtime().tm_mday != setting.CREDIT_BILL_DAY:
        common.log_write("今天不是账单日，无法生成账单")
        return

    # 数据库中是否有 client 类用户，如无则无需生成账单，反之则生成账单
    if not USER_INFO.get('client'):
        print("无用户信息，无需生成")
    else:
        # 设置账单开始时间为，上个月账单日的第二天
        startdate = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime(
            "%Y-%m-{}".format(setting.CREDIT_BILL_DAY + 1)
        )
        # 设置账单结束时间为本月的账单日
        enddate = time.strftime("%Y-%m-{}".format(setting.CREDIT_BILL_DAY))

        # 交易记录的结束时间为账单日的第二天之前
        record_enddate = time.strftime("%Y-%m-{}".format(setting.CREDIT_BILL_DAY + 1))

        # 遍历 USER_INFO 中的所有 client 类用户
        for username in USER_INFO.get('client'):

            user_info = USER_INFO.get('client').get(username)

            # 计算账单金额，取 must_repay 字段，如果小于或等于 0 则为 0
            statement_bill = user_info.get('must_repay')
            print(statement_bill)
            if statement_bill <= 0:
                statement_bill = 0
                continue

            # 账单日
            statement_pdate = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime(
                "%Y-%m-{}".format(setting.CREDIT_REPAY_DAY)
            )


            # 将账单周期内的所有交易记录保存在 statement_record 列表中
            if not user_info.get('record'):
                print("无消费记录")
                continue
            else:
                statement_record = []
                for record in user_info.get('record'):

                    if time.strptime(startdate,'%Y-%m-%d') \
                            <= time.strptime(record.get('time'),'%Y-%m-%d %H:%M:%S') \
                            < time.strptime(record_enddate,'%Y-%m-%d'):

                        statement_record.append(record)


            statement_dict = {
                'billdate': setting.CREDIT_BILL_DAY,
                'startdate': startdate,
                'enddate': enddate,
                'statement_bill': statement_bill,
                'statement_pdate': statement_pdate,
                'statement_record': statement_record,
            }

            # 添加账单到 debt 列表
            user_info['debt'].append(statement_dict)

        # 写入文件
        json.dump(USER_INFO,open(setting.CREDIT_USER,'w'))

def run():
    init()  # 初始化信息
    create_interest()   # 生成利息
    create_card_statement() # 生成账单



