# /user/bin/env python
__author__ = 'wenchong'


import os
import sys

if __name__ == '__main__':
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
    from src import creditcard

    creditcard.run(sys.argv)