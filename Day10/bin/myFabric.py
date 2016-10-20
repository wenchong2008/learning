# /user/bin/env python
__author__ = 'wenchong'


import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
sys.path.insert(0, PROJECT_ROOT)

if __name__ == '__main__':
    from src import MyFabric
    from src.HostAdmin import Host
    MyFabric.run()