#/user/bin/env python
__author__ = 'wenchong'


import sys
from setting import menu_list


def showlist(menu,name,back=True):
    """
    用于根据列表输出选项，并提示用户选择
    :param menu: type is list,传入可显示的列表
    :param name: 定义列表的属性，是属于城市，区，或公司
    :param back: 定义是否需要出现返回上一级菜单
    :return:返回用户选择的选项
    """
    while True:
        print("\n请选择 %s 信息: \n" % name)
        for k,v in enumerate(menu,1):
            print(k,v)
        print()
        if back:
            print("b 返回上一级")
        print("q 退出程序\n")
        user_input = input("请输入选项对应的数字或字母：").strip().lower()

        if user_input == 'q':
            sys.exit()
        elif user_input == 'b' and back:
            return -1
        else:
            try:
                # 用户的输入必须为数字，并且可以正常从列表中获取到对应的值，否则需要重新选择
                user_input = int(user_input)
                choice = menu[user_input-1]
            except:
                continue
        return choice

def main():
    """
    入口函数，依次选择城市，区，公司信息，最后输出公司所在城市，区，以及公司的员工信息
    """
    try:
        while True:
            citys = list( menu_list.keys() )
            city = showlist(citys,name='城市',back=False)

            while True:
                areas = list( menu_list[city].keys() )
                area = showlist(areas,name='区')
                # 当选择范围上一级时，跳出本次循环
                if area == -1:
                    break
                else:
                    while True:
                        companys = list( menu_list[city][area].keys() )
                        company = showlist(companys,name='公司')
                        # 当选择范围上一级时，跳出本次循环
                        if company == -1:
                            break
                        else:
                            users = menu_list[city][area][company]
                            # print() 函数的 end 参数默认为 "\n",这里定义为空，表示不换行
                            print("\n城市: %s\n区: %s\n公司: %s \n总人数: %s\n分别为: " %(city,area,company,len(users)),end="")
                            for user in users:
                                print(user,"",end="")
                            print('\n')
                            sys.exit()
    except KeyboardInterrupt:
        print()
        sys.exit(1)

if __name__ == '__main__':
    main()
