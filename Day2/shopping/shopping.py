# /user/bin/env python
__author__ = 'wenchong'


import os
import json
import datetime
from login import Login


class Shopping(object):

    def __init__(self,file):
        """
            self.product_file: 商品列表文件
            self.file： 用户配置文件，用于存放用户余额以及购物车信息
            self.shopping_info: 获取 self.file 文件中的信息
        """
        self.product_file = 'product.json'
        self.file = file
        self.shopping_info = self.get_shopping_info()

    def get_product_list(self):
        """
        获取产品列表
        """
        # 如果产品列表文件不存在,返回空
        if not os.path.isfile(self.product_file):
            return

        # 返回商品列表字典
        with open(self.product_file) as product_file:
            product_dict = json.load(product_file)

        return product_dict

    def show_shopping_cart(self):
        """
        输出详细的购物车信息
        """
        print("\n%s\n" % " 购物车信息开始 ".center(70,'#'))
        shopping_cart = self.shopping_info.get('shopping_cart')
        if shopping_cart:
            print('ProductName'.center(30,'-'),'Number'.center(10,'-'),'Date'.center(20,'-'),'Price'.center(10,'-'))
            for p in shopping_cart:
                print("%s|%s|%s|%s|" %
                      (p['name'].ljust(30,),
                       str(p['number']).center(10),
                       p['time'].center(20),
                       str(p['price']).center(10))
                )
            print('ProductName'.center(30,'-'),'Number'.center(10,'-'),'Date'.center(20,'-'),'Price'.center(10,'-'))
        else:
            print("购物车为空")
        print("\n%s\n" % " 购物车信息结束 ".center(70,'#'))

    def show_balance(self):
        "输出余额信息"
        print("\n%s\n" % " 余额信息开始 ".center(20,'#'))
        print("\033[31;1m您的余额为：%s\033[0m" % self.shopping_info.get('money'))
        print("\n%s\n" % " 余额信息开始 ".center(20,'#'))


    def show_list(self,p_list,p_name="商品",back=True):
        """
        输出 p_list 列表，供用户选择
        """
        while True:
            print()
            print("请选择%s信息" % p_name)
            print()
            for k,v in enumerate(p_list,1):
                if isinstance(v,dict):
                    print("%s %s %s" %(k,v['name'].ljust(30,'-'),v['price']))
                else:
                    print(k,v)
            print()
            if back:
                print("b 返回上一级" )
            print('r 充值' )
            print('c 查询余额')
            print("v 查看购物车")
            print("q 退出整个程序\n")
            user_input = input("请输入选项对应的数字或字母：").strip().lower()

            if user_input == 'q':
                self.exit_progrom()
            elif user_input == 'b' and back:
                return -1
            elif user_input == 'v':
                self.show_shopping_cart()
                continue
            elif user_input == 'c':
                self.show_balance()
                continue
            elif user_input == 'r':
                self.recharge()
                continue
            else:
                try:
                    # 用户的输入必须为数字，并且可以正常从列表中获取到对应的值，否则需要重新选择
                    user_input = int(user_input)
                    choice = p_list[user_input-1]
                except:
                    continue
            return choice

    def get_shopping_info(self):
        """
        取出用户的购物车信息以及余额信息并返回，如果文件不存在，或文件内容不为 json 格式，则重置文件内容
        """
        dir,filename = self.file.split('/')
        if os.path.isdir(dir):
            if os.path.isfile(self.file):
                with open(self.file) as shopping_info:
                    try:
                        shopping_info = json.load(shopping_info)
                        return  shopping_info
                    except:
                        # 当用户文件不为 json 格式时，重置该文件
                        pass
        else:
            os.mkdir(dir)

        return {"money":0,"shopping_cart":[]}

    def update_shopping_info(self):
        """
        将用户信息写入磁盘
        """
        shopping_file = open(self.file,'w')
        shopping_file.write(json.dumps(self.shopping_info))
        shopping_file.close()

    def recharge(self):
        """
        用户充值界面
        """
        print("\n%s" % "欢迎进入充值界面".center(50,"*"))
        while True:

            print("\n%s %s" %('q','退出充值界面'))

            self.show_balance()

            money = input('请输入充值金额：')

            # 如果输入的为数字，则更新余额，输出余额，并提示是否继续充值
            if money.isdigit():
                money = int(money)
                self.shopping_info['money'] += money
                self.update_shopping_info()

                self.show_balance()

                info ={ 'y':"继续充值",'n':'退出充值'}
                user_input = self.user_confirmation(info)
                if user_input == 'y':
                    continue
                else:
                    print("\n%s" % "已经退出充值界面".center(50,"*"))
                    break
            elif money == 'q':
                print("\n%s" % "已经退出充值界面".center(50,"*"))
                break

            # 输入其他任何选项均提示重新输入,包括负数
            else:
                continue

    def user_confirmation(self,info):
        "需要用户输入的确认信息，并返回输入"
        while True:
            msg = ""
            for k in info:
                msg += "%s %s\n" %(k,info[k])
            msg += "\n请选择: "
            user_input = input(msg).lower().strip()
            if user_input in info:
                return user_input
            else:
                continue

    def exit_progrom(self):
        print()
        exit('已经退出全国最大的购物商城'.center(50,'-'))


    def shopping(self):
        """
        展示所有商品信息供用户选择
        """
        product_list = self.get_product_list()

        # 如果无法获取产品信息列表则退出程序
        if product_list:
            print("\n%s" % "欢迎进入购物界面".center(50,"*"))
        else:
            print("\n商品列表 %s 不存在\n" % self.product_file)
            self.exit_progrom()

        # 获取商品的类别，并循环输出，提供选择
        product_category = list(product_list.keys())

        while True:
            # 由于是第一级，所有 back=False,不提供返回上一级选项
            choice_category_1 = self.show_list(product_category,back=False)

            # 根据用户的选择，获取该类别下的所有商品新，并转换为列表
            choice_category_dict_1 = product_list.get(choice_category_1)
            choice_category_list_1 = list(choice_category_dict_1.keys())

            while True:
                # 输出商品类别
                choice_category_2 = self.show_list(choice_category_list_1)
                # 返回上一级目录
                if choice_category_2 == -1:
                    break
                else:
                    while True:
                        choice_product_list = choice_category_dict_1.get(choice_category_2)
                        choice_product = self.show_list(choice_product_list,p_name="商品")

                        if choice_product == -1:
                            break
                        else:
                            while True:
                                # 选择商品后，选择购买商品的个数
                                number = input("\nb 返回上一级\n\n请输入需要购买的数量： ").lower().strip()
                                # 如果输入的为数字
                                if number.isdigit():
                                    number = int(number)
                                    print("您需要为选择的商品[ \033[31;1m%s\033[0m ],共计 [ \033[31;1m%s\033[0m 件] 支付 [\033[31;1m%s\033[0m] 元\n" %
                                          (choice_product['name'],number,choice_product['price']*number))
                                    # 余额大于需要购买的商品总价格
                                    if self.shopping_info['money'] >= choice_product['price']*number:
                                        info = {'y':'支付','n':'重选'}
                                        user_input = self.user_confirmation(info)
                                        if user_input == 'n':
                                            break
                                        # 扣除金额，并将商品添加至购物车
                                        self.shopping_info['money'] -= choice_product['price']*number
                                        self.shopping_info['shopping_cart'].append(
                                            {
                                                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                'name': choice_product['name'],
                                                'price':choice_product['price']*number,
                                                'number':number
                                            }
                                        )
                                        # 输出购物车以及将数据写入磁盘
                                        self.show_shopping_cart()
                                        self.update_shopping_info()

                                        # 询问是否继续购物
                                        info = {'y':"继续购物",'n':'退出程序'}
                                        user_input = self.user_confirmation(info)
                                        if user_input == 'y':
                                            break
                                        else:
                                            self.exit_progrom()
                                    # 余额小于需要购买的商品总额
                                    else:
                                        print("\n\033[43;1m您的余额[ %s ]不足，必须充值后才能购物\033[0m\n" % self.shopping_info['money'])

                                        # 是否需要充值
                                        info = {"r":"充值","q":"退出","b":"返回上一级"}
                                        user_input = self.user_confirmation(info)
                                        if user_input == 'r':
                                            self.recharge()
                                            break
                                        elif user_input == 'q':
                                            self.exit_progrom()
                                        else:
                                            break
                                # 重新选择商品
                                elif number == 'b':
                                    break
                                # 输入的值不为数字
                                else:
                                    continue


def main():
    "主函数"

    # 认证入口,返回 lock 或 username，返回 lock 退出
    try:
        user_login = Login()
        username = user_login.login()
    # ctrl+C 退出程序
    except KeyboardInterrupt:
        exit("\n")

    if username != 'lock':
        # 商城入口
        try:
            print('欢迎登陆全国最大的购物商城'.center(50,'-'))
            # 获取用户的配置文件信息
            all_user_info = user_login.all_user_info
            user_conf_file = all_user_info.get(username).get('home')

            shopping = Shopping(user_conf_file)
            # 进入程序第一件事情询问是否充值
            shopping.recharge()

            # 如果余额为 0，则必须充值才能购物
            while not shopping.shopping_info['money']:
                print("\n\033[43;1m您的余额不足，必须充值后才能购物\033[0m")
                shopping.recharge()

            # 购物入口
            shopping.shopping()
            # 将数据写入磁盘
            shopping.update_shopping_info()
        # ctrl+C 退出程序
        except KeyboardInterrupt:
            print()
            exit('已经退出全国最大的购物商城'.center(50,'-'))
    else:
        exit()

if __name__ == '__main__':
    main()