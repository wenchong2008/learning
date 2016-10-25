# /user/bin/env python
__author__ = 'wenchong'

import sys
import getpass
import paramiko
import os
import socket
from src.Models import ModelAdmin
from paramiko.py3compat import u

import termios
import tty
import select


class Jump(object):

    def __init__(self):
        self.user = None
        self.host = None
        self.modeladmin = ModelAdmin()


    def login(self):
        """Login to JumpServer"""
        username = input('User Name: ').strip()
        password = getpass.getpass('Password: ').strip()

        user_obj = self.modeladmin.get_user(username)

        if user_obj:
            if user_obj.password == password:
                self.user = user_obj
                return True
            else:
                print('Password Error.')
        else:
            print('User Name Not Exist.')

    def select_host(self):
        """Select Server For Jump"""
        hosts = []
        for group in self.user.groups:
            for hostuser in group.hostusers:
                if hostuser not in hosts:
                    hosts.append(hostuser)

        for index, obj in enumerate(hosts, 1):
            print('{}、IPAddress: {}\tHostName:{}\tHostUser:{}'.format(
                index, obj.host.ip_address, obj.host.hostname, obj.username
            ))

        while True:
            try:
                user_input = input('Select: ').strip()
                host = hosts[int(user_input) - 1]
                self.host = host
                return host
            except Exception:
                pass

    def login_server(self):
        """通过 key 认证登陆到远程服务器"""
        transport = paramiko.Transport((self.host.host.ip_address, 22))
        transport.start_client()

        transport.auth_password(username=self.host.username, password=self.host.password)

        # 打开一个通道
        channel = transport.open_session()
        # 获取一个终端
        channel.get_pty()
        # 激活器
        channel.invoke_shell()

        return channel

    def posix_shell(self,channel):
            """启用 Linux shell"""

            # 获取之前的 tty
            fd = sys.stdin.fileno()
            oldtty = termios.tcgetattr(fd)

            try:
                tty.setraw(fd)
                tty.setcbreak(fd)

                channel.settimeout(0.0)

                command_list = []
                tab_flag = False

                while True:
                    r_list, w_list, e_list = select.select([channel, sys.stdin], [], [], 1)
                    if channel in r_list:
                        try:
                            x = u(channel.recv(1024))
                            if len(x) == 0:
                                print("\r\n*** EOF\r\n")
                                break

                            # 输入 tab 后的返回值如果不换行则记录为命令[补全命令]
                            if tab_flag:
                                if not x.startswith("\r\n"):
                                    command_list.append(x)
                                tab_flag = False

                            sys.stdout.write(x)
                            sys.stdout.flush()
                        except socket.timeout:
                            pass

                    if sys.stdin in r_list:
                        x = sys.stdin.read(1)

                        if len(x) == 0:
                            break

                        # 用户输入 tab 键
                        if x == "\t":
                            tab_flag = True
                        else:
                            command_list.append(x)

                        if x == '\r':
                            command = ''.join(command_list)
                            # 发送的命令为空，即只有回车时忽略记录日志
                            if command != '\r':
                                # print(command)
                                self.modeladmin.add_log(user=self.user.id,host_user=self.host.id,command=command)
                            command_list.clear()

                        channel.sendall(x)

            finally:
                # 恢复之前的 tty
                termios.tcsetattr(fd, termios.TCSADRAIN, oldtty)


def run():

    try:
        jump = Jump()

        if jump.login():
            if jump.select_host():
                channel = jump.login_server()
                jump.posix_shell(channel)
    except KeyboardInterrupt:
        exit('\n')
    except Exception as e:
        print(e)
