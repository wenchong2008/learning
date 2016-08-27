# /user/bin/env python
__author__ = 'wenchong'

import os
import json
import datetime


CONFIG_FILE = 'conf/haproxy.cfg'
CONFIG_FILE_NEW = 'conf/haproxy.conf_new'
CONFIG_FILE_BAK = 'conf/haproxy.conf_bak'
FORMAT_RECORD = """{"backend": "www.wenchong.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}"""


def get_input():
    """
    获取用户需要进行的操作，并返回
    """
    op_dict = {
        'add_config':'添加记录',
        'del_config':'删除记录',
        'get_config':'获取记录'
    }

    op_list = sorted(op_dict.keys())

    for index,op in enumerate(op_list,1):
        print("{}、{}".format(index,op_dict[op]))

    user_input = input("请选择：").strip()
    while True:
        if user_input.isdigit():
            index = int(user_input)-1
            if index < len(op_list):
                user_input = op_list[index]
                return user_input
        user_input = input("您输入的编号不存在，请重新输入: ").strip()


def get_json():
    """
    捕获用户输入，并检查 json 格式
    :return:
    """
    print("格式如：%s" %FORMAT_RECORD)
    user_input = input("请输入要操作的配置: ").lower().strip()
    # 检查用户输入的格式是否为 json 格式，并且包含指定的 key，否则重新输入
    while True:
        try:
            backend_info = json.loads(user_input)
            record = backend_info['record']
            return backend_info,record['server'],record['weight'],record['maxconn']
        except:
            backend_info = input("[q = 退出]输入的格式不为 JSON 格式，请重新输入：").lower().strip()
            if backend_info == 'q':
                return


def get_backend_server(backend):
    """
    获取 backend 下的记录
    :param backend: 域名
    :return: backend 下的所有 server 信息列表
    """

    flag = False
    servers_info = {}

    with open(CONFIG_FILE) as config:
        for line in config:
            line = line.strip()
            if line == 'backend %s' % backend:
                flag = True
                continue
            if line.startswith('backend'):
                flag = False

            if flag and line:
                ip = line.split()[2]
                servers_info[ip] = line
    return servers_info


def show_backend(backend):
    """
    根据 backend 输出记录
    :param backend: backend 名称
    :return:
        如果 backend 下有 server list 则返回 True，否则返回 False
    """
    servers_info = get_backend_server(backend)

    if servers_info:
        servers_info = servers_info.values()

        print(backend.center(70,'-'))
        print("HostName".center(20,'-'),'IP'.center(20,'-'),'Weight'.center(10,'-'),'MaxConn'.center(10,'-'))

        for server_info in servers_info:
            server_info = server_info.split()
            print(server_info[2].center(20),server_info[2].center(20),server_info[4].center(10),server_info[6].center(10))
        return True
    else:
        return False


def backup():
    """
    备份配置文件
    """
    os.rename(CONFIG_FILE,"%s-%s" %(CONFIG_FILE_BAK,datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    os.rename(CONFIG_FILE_NEW,CONFIG_FILE)


def get_config():
    """
    获取 backend 下的记录并输出
    """

    print("获取记录".center(70,'#'))
    backend = input("请输入 backend：").lower().strip()

    while True:

        show_config_result = show_backend(backend)

        if show_config_result:  # 如果有 server list 输出，则跳出循环
            break

        # 如果无 server list 输出则重新输入 backend
        backend = input("[q = 退出]您输入的域名不存在，请重新输入：").lower().strip()
        if backend == 'q':
            break


def add_config():
    """
    添加记录
    """

    print("添加记录".center(100,'-'))
    user_input = get_json()

    if not user_input:
        exit()

    backend_info,ip,weight,maxconn = user_input

    backend_domain = backend_info.get('backend')
    record = "server %s %s weight %s maxconn %s" %(ip,ip,weight,maxconn)

    # 根据 backend_domain 获取 backend 下的 server list
    servers_info = get_backend_server(backend_domain)

    # 如果 backend 不存在，则在配置文件的最后新增 backend 和 server
    if not servers_info:
        with open(CONFIG_FILE) as f_online, open(CONFIG_FILE_NEW,'x') as f_new:
            for line in f_online:
                f_new.write(line)
            f_new.write("\n\nbackend %s\n" % backend_domain)
            f_new.write(" "*8+record)

    # 如果 backend 存在
    else:
        # 如果需要添加的 IP 在 server list 已经存在，但是record 中的 wight 和 maxconn 与需要添加的同，则按照需要添加的修改
        if ip in servers_info:
            if not servers_info.get(ip) == record:
                servers_info[ip] = record

        # 如果需要添加的 IP 地址不在 server list 中，则新增
        else:
            servers_info[ip] = record

        # 打开新老文件
        with open(CONFIG_FILE) as f_online, open(CONFIG_FILE_NEW,'x') as f_new:

            flag = False

            for line in f_online:
                # 逐行读取文件时，如果等于 backend domain，则将 flag 标记为 True
                if line.strip() == 'backend %s' % backend_domain:
                    flag = True
                    f_new.write(line)

                    # 将 server list 逐行写入新文件
                    for k in servers_info:
                        f_new.write(" "*8+servers_info.get(k)+'\n')
                    continue

                # 如果该行已 backend 开头，flag 标记为 False
                if line.strip().startswith('backend'):
                    flag = False

                # 如果 flag 不为 True 时，写入新文件，否则不做操作
                if not flag:
                    f_new.write(line)

    # 备份文件，并输出添加完成的 server list
    backup()
    show_backend(backend_domain)


def del_config():
    """
    根据 backend 和 IP 地址进行删除 backend 下的记录
    :return:
    """

    # 用户输入新的配置，并检查是否包含指定的 key，否则重新输入
    print("删除记录".center(100,'-'))

    user_input = get_json()

    if not user_input:
        exit()

    backend_info,ip,weight,maxconn = user_input

    # 定义 backend 域名以及获取 server list
    backend_domain = backend_info.get('backend')
    servers_info = get_backend_server(backend_domain)

    # 如果 backend 不存在，则重新输入
    if not servers_info:
        exit("backend %s 不存在" % backend_domain)

    # 如果 backend 存在
    else:
        # 如果需要删除的 IP 在 server list 中，则在 server_info 字典中删除该 key，否则重新输入或退出
        if ip in servers_info:
            del servers_info[ip]
        else:
            print("backend %s 下无该记录" % backend_domain)
            show_backend(backend_domain)
            exit()

        with open(CONFIG_FILE) as f_online, open(CONFIG_FILE_NEW,'x') as f_new:
            flag = False

            for line in f_online:
                if line.strip() == 'backend %s' % backend_domain:
                    flag = True
                    # 如果删除掉 server 之后的 server list 不为空，则在新文件中写入 backend 和 server list
                    # 否则直接跳过，不做操作
                    if servers_info:
                        f_new.write(line)

                        # 逐行写入 server list
                        for k in servers_info:
                            f_new.write(" "*8+servers_info.get(k)+'\n')

                    continue

                # 如果 backend 开头，则 flag 为 False
                if line.strip().startswith('backend'):
                    flag = False

                if not flag:
                    f_new.write(line)

        # 备份文件，并输出删除后的配置
        backup()

        if servers_info:
            show_backend(backend_domain)
        else:
            print("backend %s 下 的最后一条记录已经被删除。" % backend_domain)


def main():
    try:
        user_input = get_input()
        if user_input == 'get_config':
            get_config()
        elif user_input == 'add_config':
            add_config()
        elif user_input == 'del_config':
            del_config()
    except KeyboardInterrupt:
        print()
        exit()


if __name__ == '__main__':
    main()