# /user/bin/env python
__author__ = 'wenchong'

import re
import json
import socketserver
import subprocess


import os
# import sys
# project_root = os.path.join(os.path.dirname(__file__), os.pardir)
#
# sys.path.insert(0, project_root)

from lib.commons import log_write, md5_file
from config import setting
from src.UserAdmin import User, UserAdmin



class FTPServer(object):
    """
    FTP 服务端，包含功能：
    1、显示列表
    2、目录切换
    3、查看当前所在目录
    4、上传文件
    5、下载文件
    """

    def __init__(self, request):
        """
        初始化数据
        request 为用户连接的 socket 对象
        """
        self.request = request
        self.user = ''    # 用户对象
        self.current_dir = ''  # 用户当前所在目录，登陆成功后为 /
        self.homedir = ''  # 用户的家目录

    def send_banner(self):
        """用户连接后，输出服务器版本"""
        banner = "MyFTP Version 1.0"
        self.send_data(banner)

    def send_data(self, data):
        """发送数据，当数据不为 bytes 时自动转换后发送"""
        if type(data) != bytes:
            data = bytes(data, encoding='utf-8')

        self.request.sendall(data)

    def receive_data(self):
        """接收客户端发送的数据，每次最多接收 1024 字节，并返回"""
        receive_data = self.request.recv(1024)
        return receive_data

    def login(self):
        """User Login Method"""
        # 接收用户名和密码信息
        login_info = self.receive_data().decode()
        try:
            login_info = json.loads(login_info, encoding='utf-8')
            user_obj = UserAdmin()
            user = user_obj.login(**login_info)
            if user:
                self.user = user  # 设置 user 对象
                self.current_dir = '/'  # 设置当前目录为 /
                self.homedir = os.path.abspath(os.path.join(setting.HOMEDIR, user.homedir))  # 设置家目录
                # 登陆成功后发送 Success 给客户端
                self.send_data("Success")
                return user
        except Exception as e:
            return False

    def _get_dir(self,option):
        """
        获取用户输入的路径，在服务端找到对应的目录
        """
        # 如果用户输入的的 parameter 为空，则定义目录为 .
        dir_name_from_client = option.get('parameter') or '.'

        # 如果用户输入的 parameter 中间包含空格，则返回 None
        if len(dir_name_from_client.split("\s+")) != 1:
            return None,None

        # 需要查看的目录 = 用户家目录 + 用户当前所在目录 + 客户端发送的目录
        realpath = os.path.join(
            self.homedir,
            re.sub('^/', '', self.current_dir),  # 删除开头的 /
            re.sub('^/', '', dir_name_from_client)
        )

        # 将目录转换为绝对路径，不包含 . 或 .. 之类多余的路径
        abspath = os.path.abspath(realpath)

        # 如果需要查看的路径长度小于用户家目录长度，则将用户需要查看路径设置为家目录
        # 这里存在 bug，如果用户查看另外一个目录长度大于家目录长度就会查看到家目录以外的目录
        if not self.__is_sub_path(abspath, self.homedir):
            abspath = self.homedir

        return dir_name_from_client, abspath

    @staticmethod
    def __is_sub_path(child, parent):
        """判断 child 目录是否为 parent 的子目录"""

        child = os.path.abspath(child)
        parent = os.path.abspath(parent)
        if child.startswith(parent):
            return True
        else:
            return False

    def __get_homedir_size(self):
        """获取家目录的大小"""
        size = 0
        for root,dirs,files in os.walk(self.homedir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size

    def ls(self, option):
        """
        显示目录下的文件列表，或文件的信息
        """
        # 获取用户输入的路径，以及需要查看的真实路径
        dir_name_from_client, abspath = self._get_dir(option)

        # 如果为 None 则退出
        if not dir_name_from_client:
            self.send_data('Directory is error.')
            log_write("user [%s] command [%s %s] failed,because directory format error." % (
                self.user.username, option['action'], option['parameter'])
            )
            return

        # 如果系统路径不存在
        if not os.path.exists(abspath):
            self.send_data("Directory is not exist.")
            log_write("user [%s] command [%s %s] failed,because directory not exist." % (
                self.user.username, option['action'], option['parameter'])
            )
        else:
            res = subprocess.Popen(
                [ "ls","-ln", abspath ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # 获取命令返回结果
            file_list = res.stdout.read()

            # 如果 abspath 是一个文件时，会出现系统的绝对路径，将绝对路径替换为从家目录开始的路径
            file_list = re.sub(self.homedir,'',file_list.decode())

            # 如果目录为空
            if not file_list:
                self.send_data("Directory is NULL.")
            else:
                self.send_data(file_list)
            log_write("user [%s] command [%s %s] successfully" % (
                self.user.username, option['action'], option['parameter'])
            )

    def cd(self, option):
        """切换路径"""

        dir_name_from_client, abspath = self._get_dir(option)

        # 如果为 None, 则退出
        if not dir_name_from_client:
            self.send_data("Can not change directory to \"%s\"" % " ".join(option.get('parameter')))
            log_write("user [%s] command [%s %s] failed,because directory format error." % (
                self.user.username, option['action'], option['parameter'])
            )
            return

        # 如果 abspath 为目录
        if os.path.isdir(abspath):
            # 如果切换的目录以 / 开始，则当前目录为需要切换的目录
            if dir_name_from_client.startswith("/"):
                self.current_dir = dir_name_from_client
            else:
                self.current_dir = os.path.join(self.current_dir,dir_name_from_client)
            # 转换目录结构
            self.current_dir = os.path.realpath(self.current_dir)
            self.send_data("Change directory to %s successful." % self.current_dir)
            log_write("user [%s] command [%s %s] successfully" % (
                self.user.username, option['action'], option['parameter'])
            )
        else:
            self.send_data("Change directory to %s failed." % self.current_dir)
            log_write("user [%s] command [%s %s] failed,because %s is file." % (
                self.user.username, option['action'], option['parameter'], option['parameter'])
            )

    def pwd(self, option):
        """查看当前目录"""
        self.send_data(self.current_dir)
        log_write("user [%s] command [%s %s] successfully" % (
                self.user.username, option['action'], option['parameter']))


    def mkdir(self, option):
        # 获取用户输入的路径，以及需要查看的真实路径
        dir_name_from_client, abspath = self._get_dir(option)

        if os.path.exists(abspath):
            self.send_data(json.dumps({'status':'exist'}))
            log_write("user [%s] create dir [%s] failed, existed" % (
                self.user.username, dir_name_from_client)
            )
        else:
            os.mkdir(abspath)
            self.send_data(json.dumps({'status':'success'}))
            log_write("user [%s] create dir [%s] success" % (
                self.user.username, dir_name_from_client)
            )

    def rm(self, option):
        """删除文件或目录"""
        dir_name_from_client, abspath = self._get_dir(option)
        if not os.path.exists(abspath):
            self.send_data(json.dumps({'status':'failed', 'msg': '%s not exist' % dir_name_from_client}))
            log_write("user [%s] delete dir [%s] failed, not existed" % (
                self.user.username, dir_name_from_client)
            )
        else:
            if os.path.isfile(abspath):
                os.remove(abspath)
                self.send_data(json.dumps({'status':'success', 'msg': ''}))
                log_write("user [%s] delete file [%s] success" % (
                    self.user.username, dir_name_from_client)
                )
            else:
                try:
                    os.rmdir(abspath)
                    self.send_data(json.dumps({'status':'success', 'msg': ''}))
                    log_write("user [%s] delete dir [%s] success" % (
                        self.user.username, dir_name_from_client)
                    )
                except Exception as e:
                    self.send_data(json.dumps({'status': 'failed', 'msg': "Directory not empty."}))
                    log_write("user [%s] delete dir [%s] failed, not empty" % (
                        self.user.username, dir_name_from_client)
                    )



    def put(self, option):
        """
        上传文件，过程如下：
        1、客户端发送 {'action': 'put', 'filename': 'filename', 'size': int}
        2、服务器发送 {'status':'start'}
        3、服务器准备接收
        4、服务器打开一个临时文件 filename.tmp，存放接收的信息
        5、已经接收的大小 == int，重命名 filename.tmp 为 filename，并发送 {'status':'end'} 给客户端，表示接收成功
        """

        try:
            upload_file_name = option.get('filename')
            upload_file_size = option.get('size')
            upload_file_md5 = option.get('md5')


            if option['action'] == 'put' and upload_file_name and upload_file_size and upload_file_md5:

                filename_tmp = upload_file_name + '.tmp'

                # 组合上传文件存放的真实路径 = 用户家目录 + 当前目录 + 临时文件名
                filename_tmp_path = os.path.join(self.homedir, re.sub('^/','',self.current_dir), filename_tmp)

                # 则设置指针 seek 和 打开模式
                if os.path.isfile(filename_tmp_path):
                    seek = os.path.getsize(filename_tmp_path)
                    mode = 'ab'
                else:
                    seek = 0
                    mode = 'wb'

                # 检查是否超过磁盘配额
                homedir_size = self.__get_homedir_size()
                if homedir_size + upload_file_size > self.user.quota:
                    self.send_data(json.dumps({'status': 'quota'}))
                    return

                self.send_data(json.dumps({'status': 'start','seek': seek}))

                receive_size = seek

                # 接收文件
                with open(filename_tmp_path, mode=mode) as f:
                    while receive_size < option['size']:
                        msg_tmp = self.receive_data()
                        f.write(msg_tmp)
                        receive_size += len(msg_tmp)
                if receive_size == option['size'] and md5_file(filename_tmp_path) == upload_file_md5:
                    os.rename(filename_tmp_path, re.sub('\.tmp$','', filename_tmp_path))
                    self.send_data(json.dumps({'status':'end'}))
                    log_write("user [%s] upload file [%s] [size: %s] successfully" % (
                        self.user.username, os.path.join(self.current_dir, option['filename']),receive_size)
                    )
                else:
                    log_write("user [%s] upload file [%s] [size: %s] failed" % (
                        self.user.username, os.path.join(self.current_dir, option['filename']),receive_size)
                    )
        except:
            pass

    def get(self, option):
        """
        下载文件，过程如下：
        1、客户端发送 {'action': 'get', 'filename': filename }
        2、组合需要下载文件的真实路径 = 用户家目录 + 当前目录 + 文件名
        3、如果文件所在目录长度小于家目录长度，或文件不存在，或该路径不是一个文件，则发送 {'filename':''}，表示需要下载的文件不存在
        4、文件存在则发送 {'filename': filename,'size':int} 给客户端
        5、接收客户端发送的 {'status': 'start'}
        6、准备发送文件数据
        """
        try:
            if option['action'] == 'get' and 'filename' in option:
                # 2、组合路径
                download_file = os.path.join(self.homedir, re.sub('^/','',self.current_dir), option['filename'])
                download_file = os.path.abspath(download_file)

                # 3、判断文件
                if not (self.__is_sub_path(os.path.dirname(download_file),self.homedir)
                        or os.path.exists(download_file)
                        or os.path.isfile(download_file)
                ):
                    self.send_data(json.dumps({'filename':''}))
                    log_write("user [%s] download file [%s] is not exist." % (
                        self.user.username, option['filename'])
                    )
                else:
                    # 4、发送文件名称和大小以及文件的MD5给客户端
                    if os.path.isfile(download_file):
                        download_file_md5 = md5_file(download_file)
                        download_file_size = os.path.getsize(download_file)
                    else:
                        download_file_md5 = ''
                        download_file_size = ''
                    download_file_name = option['filename']
                    self.send_data(json.dumps({
                        'filename': download_file_name,
                        'size': download_file_size,
                        'md5': download_file_md5
                    }))

                    # 5、接收客户端发送的状态
                    receive_data = json.loads(self.receive_data().decode())
                    if receive_data.get('status') == 'start':
                        # 6、发送文件数据

                        with open(download_file, 'rb') as f:
                            # 调整 seek
                            if 'seek' in receive_data:
                                f.seek(receive_data.get('seek'))

                            # 逐行发送文件给客户端
                            for line in f:
                                self.send_data(line)

                        receive_data = json.loads(self.receive_data().decode())
                        if receive_data.get('status') == 'end':
                            log_write("user [%s] download file [%s] [size: %s] successfully" % (
                                self.user.username, option['filename'], os.path.getsize(download_file))
                            )
                        else:
                            log_write("user [%s] download file [%s] failed" % (
                                self.user.username,  option['filename'])
                            )
                    else:
                        log_write('user [%s] download file [%s] failed, is not exist' % (
                            self.user.username, option['filename']))
        except:
            pass



class MyServer(socketserver.BaseRequestHandler):

    def handle(self):

        obj = FTPServer(self.request)
        # 发送 banner
        obj.send_banner()

        log_write("{0[0]} connection".format(self.client_address))

        user = obj.login()
        if user:
            log_write("user [{}] login successfully".format(user.username))
            while True:
                receive_data = obj.receive_data().decode()
                if not receive_data:
                    break

                try:
                    option = json.loads(receive_data)
                    func = getattr(obj, option['action'])
                    func(option)
                except:
                    continue
            log_write("client {0[0]} disconnect".format(self.client_address))
        else:
            return False


def main():
    server = socketserver.ThreadingTCPServer((setting.LISTEN,setting.PORT), MyServer)
    server.serve_forever()


def run():
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()