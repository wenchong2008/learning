# /user/bin/env python
__author__ = 'wenchong'



import os
import sys

if __name__ == '__main__':
    PATH = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0,os.path.join(PATH,os.pardir))
    from src import select_course

    select_course.run(sys.argv)

