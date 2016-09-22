# /user/bin/env python
__author__ = 'wenchong'


import os
import sys

project_root = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.insert(0, project_root)

if __name__ == "__main__":
    from src import VirtualLife
    VirtualLife.run()

