# -*- coding: utf-8 -*-
"""
Helper functions for tasks.
"""
#
#   Imports
#
import os
import subprocess

import spines


#
#   Constants
#

VERSION = spines.__version__


#
#   Functions
#

def get_alias_cmd(alias):
    """Gets the command for the given alias (if any)"""
    res = subprocess.run(['/bin/bash', '-i', '-c', 'alias %s' % alias],
                         capture_output=True)
    if res.returncode == 0:
        s_out = res.stdout.decode('utf-8').strip()
        return s_out.split('=')[-1].strip('"').strip("'")
    return alias


def log(msg, name=None, level=None):
    """Prints output to the screen"""
    ret = ''
    if name:
        ret += "[%s] " % name.lower()
    if level:
        ret += "(%s) " % level.upper()
    print(ret + msg)


def ctx_run(ctx, cmd, draft=False, log_fn=log):
    """Helper to either run cmd or just display it"""
    if draft:
        log_fn('Would run: %s' % cmd)
        return
    return ctx.run(cmd)


def print_block(text):
    """Prints a block of text"""
    print('\n  ----- START -----')
    for line in text.split('\n'):
        print('  %s' % line)
    print('  -----  END  -----\n')


def get_todos(file, context=None, project=None):
    """Gets the todo items from file"""
    if not file.endswith('txt'):
        file = '%s.txt' % file
    if not file.startswith('todos'):
        file = os.path.join('todos/', file)

    with open(file, 'r') as fin:
        contents = fin.readlines()

    return contents


def create_change_item(reference, context, message):
    """Creates a new Towncrier change file"""
    file = os.path.join('changes', '%s.%s' % (reference, context))
    with open(file, 'w') as fout:
        fout.write(message)
    return file


#
#   Variables
#

TODO_CMD = get_alias_cmd(os.getenv('TODO_CMD', 'todo.sh'))
