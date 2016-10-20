# /user/bin/env python
__author__ = 'wenchong'

import os
import re
import json
import socket
import getpass


class FTPClient(object):
    """
    FTP 客户端，功能如下：
    1、显示列表
    2、目录切换
    3、查看当前所在目录
    4、上传文件
    5、下载文件
    """
    def __init__(self, host, port=8888):
        """初始化信息"""
        self.host = host  # FTP 服务器地址
        self.port = port  # FTP 服务器端口
        self.sk = socket.socket()  # socket 对象
        self.connect()  # 连接服务器

    def show_info(self):
        """显示连接信息"""
        print("Connected to %s" % self.host)

    def connect(self):
        """连接服务器
        """
        try:
            self.sk.connect((self.host, self.port))
        except ConnectionRefusedError as e:
            print("%s by %s:%s" %(e, self.host, self.port))
            return
        except Exception as e:
            print(e)
            return

    def send_data(self, data):
        """发送数据给服务器，如果数据不为 bytes 则自动转换"""
        if type(data) != bytes:
            data = bytes(data, encoding='utf-8')

        self.sk.sendall(data)

    def receive_data(self):
        """接收服务器发送的数据"""
        return self.sk.recv(1024)

    def put(self, option):
        """
        上传文件到服务器
        1、获取上传的文件路径，并检查是否存在，是否为不为目录
        2、获取上传的文件名
        3、发送 tag 给服务器
        4、接收服务器的数据 {'status': 'start'}，并发送文件内容给服务器
        """
        file = option.get('parameter')

        if len(file.split("\s+")) != 1:
            print("上传文件格式错误")
            return False

        if not os.path.exists(file):
            print("文件不存在")
            return False

        if os.path.isdir(file):
            print("不能上传目录")
            return False

        # 2、获取文件名
        filename = os.path.basename(file)

        # 3、发送 tag
        tag = {
            'action': 'put',
            'filename': filename,
            'size': os.path.getsize(file)
        }

        self.send_data(json.dumps(tag))

        # 4、发送数据
        receive_data = self.receive_data()
        if json.loads(receive_data.decode()).get('status') == 'start':
            with open(file, mode='rb') as f:
                for line in f:
                    self.send_data(line)

            receive_data = self.receive_data()
            if json.loads(receive_data.decode()).get('status') == 'end':
                print("上传成功")

    def get(self, option):
        """
        下载文件：
        1、检查下载的文件格式
        2、获取文件名
        3、发送 tag 给服务器
        4、接收服务器发送的数据 {'filename':'filename', 'size': int}
        5、发送 {'status': 'start'} 等待接收数据
        6、接收的数据 == 文件大小，接收成功
        """
        # 1
        file = option.get('parameter')

        if len(file.split("\s+")) != 1:
            return

        # 2
        filename = os.path.basename(file)
        # 3
        tag = {
            'action': 'get',
            'filename': filename
        }
        self.send_data(json.dumps(tag))

        # 4
        receive_data = self.receive_data()
        receive_data = json.loads(receive_data.decode())
        if receive_data.get('filename') == filename and 'size' in receive_data:
            # 5
            self.send_data(json.dumps({'status':'start'}))
            receive_size = 0
            with open(filename+'.tmp', 'wb') as f:
                while receive_size < receive_data['size']:
                    receive_tmp = self.receive_data()
                    f.write(receive_tmp)
                    receive_size += len(receive_tmp)
            # 6
            if receive_size == receive_data['size']:
                print("下载成功")
                self.send_data(json.dumps({'status':'end'}))
                os.rename(filename+'.tmp', filename)
            else:
                pass
        else:
            print("文件不存在")

    def login(self):
        """登陆"""
        username = input('Name:').strip()
        password = getpass.getpass('Password:').strip()
        if username and password:
            login_info = {'username': username, 'password': password}
            self.send_data(json.dumps(login_info))
            receive_data = self.receive_data()
            if receive_data:
                return True
            else:
                return False
        else:
            return False

    def simple_action(self, option):
        """
        简单操作，发送数据给服务器，输出接收的数据
        """
        self.send_data(json.dumps(option))
        receive_data = self.receive_data()
        print(receive_data.decode())

    def ls(self,option):
        """显示目录信息"""
        self.simple_action(option)

    def cd(self, option):
        """切换目录"""
        self.simple_action(option)

    def pwd(self, option):
        """查看当前目录"""
        self.simple_action(option)

    def close(self):
        """退出客户端"""
        self.sk.close()


def main():
    # 实例化 FTPClient 对象
    ip = input('FTPServer IP:')
    obj = FTPClient(ip, port=8888)

    # 输出服务器的版本信息
    print(obj.receive_data().decode())

    # 认证
    if not obj.login():
        print("Login faild, Please try again.")
    else:
        print("Login successful")
        # 获取用户输入，并调整格式发送给服务器
        while True:
            cmd = input("ftp> ").strip()
            # 输入内容为空
            if not cmd:
                continue

            # 输入 exit 退出客户端
            if cmd == 'exit':
                print('Goodbye.')
                break

            # 格式化命令
            cmd = re.split("\s+", cmd)
            if len(cmd) == 1:
                parameter = ""
            else:
                parameter = cmd[1]

            option = {"action": cmd[0].lower(), 'parameter': parameter}

            # 执行对应的方法
            func = getattr(obj, option.get('action'))
            if func:
                func(option)
            else:
                print("命令功能未实现")
                continue

    obj.close()

def run():
    try:
        main()
    except:
        exit('\n')


# if __name__ == '__main__':
#     ip = '127.0.0.1'
#     main()



