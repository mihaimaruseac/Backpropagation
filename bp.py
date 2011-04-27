#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import sys

import src.gui

def usage():
    print './bp.py : Backpropagation for predictions'

if __name__ == '__main__':
    if len(sys.argv) == 1:
       src.gui.main()
    else:
        usage()


