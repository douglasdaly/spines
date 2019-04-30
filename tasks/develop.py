# -*- coding: utf-8 -*-
"""
Tasks related to project development.
"""
#
#   Imports
#
import os
import sys

import invoke

from .helpers import TODO_CMD
from .helpers import create_change_item
from .helpers import ctx_run
from .helpers import get_todos
from .helpers import log as hlog


#
#   Helpers
#

def log(msg, level=None):
    hlog(msg, name='develop', level=level)


def run(ctx, cmd, draft):
    return ctx_run(ctx, cmd, draft=draft, log_fn=log)


#
#   Script functions
#

@invoke.task
def todos(ctx, draft=False):
    """Compiles todos/done.txt file contents into Towncrier items"""
    log('Loading completed todo items')
    t_done = get_todos('todos/done.txt')
    if not t_done:
        log('No completed todos')
        return
    else:
        log('Loaded %s completed todos' % len(t_done))

    run(ctx, '%s report' % TODO_CMD, draft)
    run(ctx, 'git add todos/report.txt', draft)

    cnt = 0
    for i, t in enumerate(t_done):
        t_words = t.strip().split()
        t_date = t_words[1].replace('-', '')
        t_context = None
        t_ref = None
        n_str = list()
        for w in t_words[2:]:
            if w.startswith('+'):
                t_context = w[1:].lower()
            elif w.startswith('@'):
                try:
                    t_ref = int(w[1:])
                except ValueError:
                    log("Invalid @context issue number given: %s" % w,
                        level='error')
                    sys.exit(1)
            else:
                n_str.append(w)
        n_str = ' '.join(n_str)

        if t_context is None:
            log('No context given, assuming: misc', level='info')
            t_context = 'misc'
        if t_context in ('add', 'change', 'remove', 'fix', 'deprecate'):
            if not t_context.endswith('e'):
                t_context += 'e'
            if not t_context.endswith('d'):
                t_context += 'd'
        elif t_context not in ('security', 'misc'):
            log('Unknown context given, skipping: %s' % t_context,
                level='warn')
            continue

        if t_ref is None:
            t_ref = 't%s%s%s' % (t_context[0].upper(), t_date, i+1)

        if draft:
            t_file = 'changes/%s.%s' % (t_ref, t_context)
            log('Would create %s: %s' % (t_file, n_str))
        else:
            t_file = create_change_item(t_ref, t_context, n_str)
            log('Created %s: %s' % (os.path.basename(t_file), n_str))
        run(ctx, 'git add %s' % t_file, draft)
        cnt += 1

    if cnt > 0:
        tmp_str = '%s new items'
        if draft:
            tmp_str = 'Would have added %s' % tmp_str
        else:
            tmp_str = 'Added %s' % tmp_str
        log(tmp_str)

    if draft:
        log('Would clear: todos/done.txt')
    else:
        log('Clearing file: todos/done.txt')
        open('todos/done.txt', 'w').close()
    run(ctx, 'git add todos/done.txt', draft)
    run(ctx, 'git add todos/todo.txt', draft)

    return
