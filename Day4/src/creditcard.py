# /user/bin/env python
__author__ = 'wenchong'


from src import admin, client, crontab, init


def run(args):

    msg = "\n\t{0[0]} admin\n\t{0[0]} client\n\t{0[0]} crontab\n\t{0[0]} init\n".format(args)

    if len(args) != 2:
        print(msg)
    else:
        if args[1] == 'admin':
            admin.run()
        elif args[1] == 'client':
            client.run()
        elif args[1] == 'crontab':
            crontab.run()
        elif args[1] == 'init':
            init.run()
        else:
            print(msg)



