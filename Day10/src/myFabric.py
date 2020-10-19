# /user/bin/env python
__author__ = 'wenchong'


import os
import pickle
from src.HostAdmin import Host, HostAdmin
from config import setting, groups
from lib.commons import myprint
import argparse
import paramiko

from fabric.main import main

def parse_option():
    """get arguments"""
    parser = argparse.ArgumentParser()

    # -H 与 -G 必须二选一
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', dest='host', help='Hostname or IPAddress')
    group.add_argument('-G', dest='group', help='Group')

    subparsers = parser.add_subparsers(dest='subparsers_name')

    # run command, subparsers
    run_parser = subparsers.add_parser('run', help='Run command')
    run_parser.add_argument('command', help='Command for run')

    # upload  file, subparsers
    upload_parser = subparsers.add_parser('upload', help='Upload file to host or group')
    upload_parser.add_argument('localpath', help='Local path')
    upload_parser.add_argument('remotepath', help='Remote host path')

    # download file, subparsers
    download_parser = subparsers.add_parser('download', help='Download file from Host or group ')
    download_parser.add_argument('remotepath',  help='Remote host path')
    download_parser.add_argument('localpath', help='Local path')

    return parser.parse_args()


class SSH(object):
    """SSH login remote host for exec command"""
    def __init__(self, host, user, password):
        """init host, user, password, and port default 22"""
        self.host = host
        self.user = user
        self.password = password
        self.port = 22

    def connect(self):
        """Connect remote host ,return ssh object, or None"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect timeout = 10s
            ssh.connect(self.host, self.port, self.user, self.password, timeout=10)
            return ssh
        except Exception as e:
            pass

    def run(self, command):
        """exec command"""

        ssh = self.connect()
        # connect successfully

        myprint('red',"[ %s ] RUN: %s" % (self.host, command))

        if ssh:
            stdin, stdout, stderr = ssh .exec_command(command=command)
            out = stdout.readlines()
            if out:
                for line in out:
                    print("[ %s ] OUT: %s" % (self.host,line.rstrip()))

            err = stderr.readlines()
            if err:
                for line in err:
                    myprint("yellow", "[ %s ] ERR: %s" % (self.host, line.strip()))

            ssh.close()
        # connect failed
        else:
            myprint("yellow", "[ %s ] ERR: Connection Failed." % self.host)


class SFTP(object):
    """upload file to remote host , or download file from remote host"""
    def __init__(self, host, user, password):
        """init host, user, password, and port default 22"""
        self.host = host
        self.user = user
        self.password = password
        self.port = 22

    def connect(self):
        """Connect remote host ,return sftp object"""
        try:
            t = paramiko.Transport((self.host, self.port))
            t.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
        except:
            return None,None

        return sftp, t

    def upload(self, localpath, remotepath):
        """upload file to remote host"""

        myprint("red", "\n[ %s ] UPLOAD: %s to %s" %(self.host, localpath, remotepath))

        if not os.path.isfile(localpath):
            myprint("yellow", "[ %s ] ERR: %s is not file" % (self.host, localpath))

        else:
            sftp, t = self.connect()
            if sftp:
                try:
                    sftp.put(localpath=localpath, remotepath=remotepath)
                    print("[ %s ] INFO: upload %s successfully, new file %s" % (self.host, localpath, remotepath))
                except OSError as e:
                    myprint("yellow", "[ %s ] ERR: %s and %s must file" % (self.host, localpath, remotepath))
                finally:
                    t.close()
            else:
                myprint("yellow", "[ %s ] ERR: Connect Failed" % self.host)

    def download(self, localpath, remotepath):
        """download file from remote host"""
        myprint("red", "\n[ %s ] DOWNLOAD: %s" % (self.host, remotepath))
        sftp, t = self.connect()
        if sftp:
            try:
                sftp.get(remotepath=remotepath, localpath=localpath)
                print("[ %s ] INFO: download %s successfully, new file %s" %(self.host, remotepath, localpath))
            except OSError as e:
                myprint("yellow", "[ %s ] ERR: %s and %s must file" % (self.host, localpath, remotepath))
            finally:
                t.close()
        else:
            myprint("yellow", "[ %s ] ERR: Connect Failed" % self.host)


class MyFabric(object):
    """MyFabric class for exec command, upload, download on remote host"""
    def __init__(self, option):
        """
        init info:
        option: is parser_option get arguments
        hosts: operation on hosts
        hosts_dir: host info file in directory
        """
        self.option = option
        self.hosts = {}
        self.hosts_dir = setting.HOSTS_DIR
        self.get_host()

    def __get_host_obj(self, host):
        """get host info from pickle file, if host not exist, return None"""
        try:
            return pickle.load(open(os.path.join(self.hosts_dir, host), mode='rb'), encoding='utf-8')
        except:
            return None

    def get_host(self):
        """from -H or -G argument to self.hosts"""

        # if -H, one host
        if self.option.host:
            if self.option.host not in os.listdir(self.hosts_dir):
                myprint("yellow", "ERROR: Host [ %s ] is not exist." % self.option.host)
            else:

                self.hosts = {
                    self.option.host: self.__get_host_obj(self.option.host)
                }

            return

        # if -G, one group
        if self.option.group:
            if not hasattr(groups, self.option.group):
                myprint("yellow", "ERROR: Group [ %s ] is not exist." % self.option.group)
            else:
                for host in getattr(groups, self.option.group):
                    self.hosts.update({
                        host: self.__get_host_obj(host)
                    })

            return

    def run(self, host):
        """exec command"""
        ssh = SSH(host=host.host, user=host.user, password=host.password)
        ssh.run(self.option.command)

    def upload(self, sftp):
        """upload file"""
        sftp.upload(self.option.localpath, self.option.remotepath)

    @staticmethod
    def download(sftp, localpath, remotepath):
        """download file"""
        sftp.download(localpath, remotepath)

    def action(self):
        """all operation from command line"""

        # already added all hosts
        all_hosts = os.listdir(self.hosts_dir)

        for host in self.hosts:
            if host not in all_hosts:
                myprint("yellow", "\n[ %s ] ERR: not ADD." % host)

            else:
                # get host info object
                host = self.hosts.get(host)

                # if run command
                if self.option.subparsers_name == 'run':
                    self.run(host)
                # if upload or download
                else:
                    # connect sftp
                    sftp = SFTP(
                        host=host.host,
                        user=host.user,
                        password=host.password)

                    # if upload
                    if self.option.subparsers_name == 'upload':
                        self.upload(sftp)
                    # if download
                    else:

                        if len(self.hosts) == 1:
                            localpath = self.option.localpath

                        else:
                            # self.hosts > 1, localpath = localhost_host
                            if os.path.isdir(self.option.localpath):
                                myprint("yellow", "[ %s ] ERR: %s must is file" % (self.host, self.option.localpath))
                                return
                            localpath = self.option.localpath + "_" + host.host
                        self.download(sftp, localpath, self.option.remotepath)


def run():
    try:
        option = parse_option()
        obj = MyFabric(option)
        obj.action()
    except:
        exit("\n")

