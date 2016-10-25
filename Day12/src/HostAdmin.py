# /user/bin/env python
__author__ = 'wenchong'


# import os
# import sys
#
# PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
# sys.path.insert(0, PROJECT_ROOT)

import sys
from src.Models import ModelAdmin


def user_select(msg):
    """select y/n"""
    result = {
        'y': True,
        'n': False
    }

    while True:
        user_input = input(msg).strip().lower()
        if user_input in result:
            return result.get(user_input)


def add_host(model_admin):
    """ add host"""
    print('\nAdd Host Information To System:\n')

    ip_address = input('IP Address: ')

    host_obj = model_admin.get_host_for_ip(ip_address)
    if host_obj:
        print('IP Address: %s\tHostName: %s' % (host_obj.ip_address, host_obj.hostname))
        print('Users Info:')
        for index, obj in enumerate(host_obj.host_users, 1):
            print(index, obj.username)

    if user_select("Add Host and Username? (y/n):"):

        if hasattr(host_obj, 'hostname'):
            hostname = input('Hostname(%s): ' % host_obj.hostname).strip() or host_obj.hostname
        else:
            hostname = input('Hostname: ').strip()
        username = input('Username: ').strip()
        password = input('Password: ').strip()

        model_admin.add_host(hostname=hostname, ip_address=ip_address, username=username, password=password)

        print('Add Host Information To System Successfully!\n')


def add_group(model_admin):
    """add group"""
    print('\nAdd Group And Bind Host To Group:\n')
    group_name = input('GroupName: ').strip()

    group_obj = model_admin.add_group(group_name)

    if group_obj.hostusers:
        print('Users for Host Already In Group: ')
        for index, obj in enumerate(group_obj.hostusers, 1):
            print('{}、IP Address: {}\tUsername: {}'.format(index, obj.host.ip_address, obj.username))

    if user_select("Add HostUser To Group?(y/n): "):
        if len(model_admin.get_host_user()) == len(group_obj.hostusers):
            print('All HostUser in Group {}'.format(group_name))
            return
        for index, obj in enumerate(model_admin.get_host_user(), 1):
            if obj not in group_obj.hostusers:
                print('{}、IP Address: {}\tUsername: {}'.format(index, obj.host.ip_address, obj.username))

        while True:
            try:
                user_input = input('Select: ').strip()
                host_user_obj = model_admin.get_host_user()[int(user_input) - 1]
                break
            except Exception:
                pass
        group_obj.hostusers.append(host_user_obj)
        model_admin.commit()

        print('Add Group And Bind Host To Group Successfully!\n')


def add_user(model_admin):
    """add user"""
    print('\nAdd User For System And Bind To Group:\n')
    user_name = input('Username: ').strip()
    password = input('Password: ').strip()

    user_obj = model_admin.add_user(user_name, password)

    if user_obj.groups:
        print('User Already in Group: ')
        for index, obj in enumerate(user_obj.groups, 1):
            print('{}、GroupName: {}'.format(index, obj.name))

    if user_select('Add User to Group:(y/n): '):

        if len(model_admin.get_group()) == len(user_obj.groups):
            print('User [{}] in All Group!'.format(user_name))
            return

        for index, obj in enumerate(model_admin.get_group(), 1):
            if obj not in user_obj.groups:
                print('{}、GroupName: {}'.format(index, obj.name))
        while True:
            try:
                user_input = input('Select: ').strip()
                group_obj = model_admin.get_group()[int(user_input) - 1]
                break
            except Exception:
                pass

        user_obj.groups.append(group_obj)
        model_admin.commit()
        print('Add User For System And Bind To Group Successfully!\n')


def user_info(model_admin):
    """show User info"""
    user_name = input('User Name: ').strip()

    user_obj = model_admin.get_user(user_name)
    if user_obj:

        print('User Name: {}'.format(user_obj.name))
        for group_obj in user_obj.groups:
            print('\tGroup Name:{}'.format(group_obj.name))
            for hostuser_obj in group_obj.hostusers:
                print('\t\tIP Address:{}\tHostName:{}\tUserName:{}'.format(
                    hostuser_obj.host.ip_address, hostuser_obj.host.hostname, hostuser_obj.username))


def help_info():
    print("""
    python {} [host|group|user|info]
    """.format(sys.argv[0]))


def run():
    try:
        model_admin = ModelAdmin()
        if len(sys.argv) == 2:
            if sys.argv[1] == 'host':
                add_host(model_admin)
            elif sys.argv[1] == 'group':
                add_group(model_admin)
            elif sys.argv[1] == 'user':
                add_user(model_admin)
            elif sys.argv[1] == 'info':
                user_info(model_admin)
            else:
                help_info()
        elif len(sys.argv) == 1:
            add_host(model_admin)
            add_group(model_admin)
            add_user(model_admin)
        else:
            help_info()
    except KeyboardInterrupt:
        exit('\n')
    except Exception as e:
        print(e)


if __name__ == '__main__':

    run()
