# -*- coding: utf-8 -*-
"""
Helper functions for tasks.
"""
#
#   Imports
#
import os

import spines


#
#   Variables
#

VERSION = spines.__version__


#
#   Helpers
#

def log(msg, name=None, level=None):
    """Prints output to the screen"""
    ret = ''
    if name:
        ret += "[%s] " % name
    if level:
        ret += "(%s) " % level
    print(ret + msg)


def print_block(text):
    """Prints a block of text"""
    print('\n  ----- START -----')
    for line in text.split('\n'):
        print('  %s' % line)
    print('  -----  END  -----\n')
