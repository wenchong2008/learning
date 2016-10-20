# /user/bin/env python
__author__ = 'wenchong'


def myprint(code,msg):

    colors = {
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
    }

    print("\033[%sm%s\033[0m" % (colors.get(code), msg))

