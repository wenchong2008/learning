# /user/bin/env python
__author__ = 'wenchong'

import os, sys
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
sys.path.insert(0, PROJECT_ROOT)

import getpass
import pickle
from config import setting, groups
import argparse


def parse_option(flag=None):
    """get arguments"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparsers_name')

    # add
    add_parser = subparsers.add_parser('add', help='Add Hostname or IPAddress')
    add_parser.add_argument('-H', '--host', dest='host', required=True, help='Hostname or IPAddress to Add')
    add_parser.add_argument('-u', '--username', default='root', dest='user', help='Host for user')
    add_parser.add_argument('-p', '--password', dest='password', help='Host for password')

    # list
    list_parser = subparsers.add_parser('list', help="List Host or group")
    group = list_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', action='store_true', dest='show_host', help='Show host list')
    group.add_argument('-G', action='store_true', dest='show_group', help='Show host group')

    if flag:
        parser.parse_args(['-h'])

    return parser.parse_args()


class Host(object):
    """host info object"""
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password


class HostAdmin(object):
    """host admin clas"""
    def __init__(self):
        self.hosts_dir = setting.HOSTS_DIR
        self.option = self.get_option()

    @staticmethod
    def get_option():
        option = parse_option()
        return option

    def add(self):
        """add host"""
        host_file = os.path.join(self.hosts_dir, self.option.host)
        if os.path.exists(host_file):
            while True:
                r = input("Host file already exist，cover？(y/n):").strip()
                if r == 'n':
                    return
                elif r == 'y':
                    break

        host_obj = Host(self.option.host, self.option.user, self.option.password)
        pickle.dump(host_obj, open(host_file, mode='wb'))

    def show_host(self):
        """show all host"""
        hosts = os.listdir(self.hosts_dir)
        for host in hosts:
            print(host)

        print("Total Host: %s" % len(hosts))

    def show_group(self):
        """show all group"""
        all_group = dir(groups)

        for group in dir(groups):
            if group.startswith("__"):
                all_group.remove(group)

        for group in all_group:
            print("%s:" % group)
            for host in getattr(groups, group):
                if host in os.listdir(self.hosts_dir):
                    print("\t%s" % host)
                else:
                    print("\t%s\tNot Exist" % host)

    def action(self):
        """operation"""
        if self.option.subparsers_name == 'add':
            while not self.option.password:
                self.option.password = getpass.getpass("Password: ").strip()

            self.add()

        elif self.option.subparsers_name == 'list':
            if self.option.show_host:
                self.show_host()
            else:
                self.show_group()
        else:
            parse_option(flag=True)


def run():
    try:
        obj = HostAdmin()
        obj.action()
    except:
        exit("\n")

