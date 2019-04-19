# -*- coding: utf-8 -*-
"""
Tasks related to releases.

Much of this is based of the code in the pipenv library:
    https://github.com/pypa/pipenv/blob/master/tasks/release.py
"""
#
#   Imports
#
import datetime
import glob
import os
import re

import invoke

from .helpers import VERSION
from .helpers import ctx_run
from .helpers import log as hlog
from .helpers import print_block

from .develop import todos


#
#   Helpers
#

def log(msg, level=None):
    hlog(msg, name='release', level=level)


def run(ctx, cmd, draft):
    return ctx_run(ctx, cmd, draft=draft, log_fn=log)


def insert_text(original, new, after):
    """Inserts the new text into the original"""
    ret = list()
    for line in original.split('\n'):
        ret.append(line)
        if line == after:
            for new_line in new.split('\n'):
                ret.append(new_line)
    return '\n'.join(ret)


def create_docs_changelog(new_entry, write=True):
    """Creates a new changelog rst file for the docs"""
    base_dir = 'docs/changelogs/'
    curr_files = glob.glob(os.path.join(base_dir, 'changelog_*.rst'))
    curr_files = [os.path.basename(x) for x in curr_files]

    p = re.compile(r"^changelog_(\d+)\.rst$")
    next_idx = int(sorted([p.match(f).groups()[0] for f in curr_files])[-1])+1
    new_file = os.path.join(base_dir, 'changelog_%s.rst' % next_idx)

    contents = new_entry.split('\n')
    version, date = (x.strip() for x in contents[0].split('-', maxsplit=1))
    version = version[1:-1]
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime('%B %d, %Y')

    new_contents = list()
    new_contents.append(version)
    new_contents.append("=" * len(version) + '\n')
    new_contents.append(':Release: %s' % date)
    new_contents.extend(contents[2:])
    new_contents = '\n'.join(new_contents)

    if write:
        with open(new_file, 'w') as fout:
            fout.write(new_contents)
        return new_file
    return new_contents


def convert_rst_to_markdown(content):
    """Convert an rst file to markdown"""
    ret = list()
    curr = content.splitlines(keepends=False)
    for i in range(len(curr)):
        line = curr[i].strip('>').strip()
        if line.startswith('#'):
            line = '#%s' % line
        ret.append(line)
    return '\n' + '\n'.join(ret) + '\n'


def changelog_rst_to_md(ctx, path):
    """Convert a CHANGELOG.rst to a CHANGELOG.md file"""
    content = ctx.run(
        'pandoc %s -f rst -t commonmark' % path, hide=True
    ).stdout.strip()

    content = re.sub(
        r"([^\n]+)\n?\s+\[[\\]+(#\d+)\]\(https://github\.com/douglasdaly/[\w\-]+/issues/\d+\)",  # noqa
        r"\1 \2", content, flags=re.MULTILINE
    )

    return convert_rst_to_markdown(content)


#
#   Tasks
#

@invoke.task
def changelog(ctx, draft=False):
    """Generates the CHANGELOG file"""
    todos(ctx, draft=draft)
    rel_ver = ctx.run('git rev-parse --abbrev-ref HEAD', hide=True).stdout
    if rel_ver.startswith('release') or rel_ver.startswith('hotfix'):
        rel_ver = rel_ver.split('/')[-1].strip('v')
    else:
        rel_ver = VERSION

    curr_md = open('CHANGELOG.md', 'r').read()
    if draft:
        ctx.run(f"towncrier --draft --version {rel_ver} > CHANGELOG.draft.rst",
                hide=True)
        log('Would clear changes/*')
        md_content = changelog_rst_to_md(ctx, 'CHANGELOG.draft.rst')
        new_md = insert_text(curr_md, md_content, "[//]: # (BEGIN)")
        rst_content = open('CHANGELOG.draft.rst', 'r').read()
        os.remove('CHANGELOG.draft.rst')
        log('Would create new docs/changelog file:')
        print_block(create_docs_changelog(rst_content, write=False))

    else:
        if os.path.exists('CHANGELOG.draft.md'):
            os.remove('CHANGELOG.draft.md')
            ctx.run('git add CHANGELOG.draft.md')
        ctx.run(f'towncrier --version {rel_ver} --yes', hide=True)
        ctx.run('git add changes/')
        md_content = changelog_rst_to_md(ctx, 'CHANGELOG.rst')
        new_md = insert_text(curr_md, md_content, "[//]: # (BEGIN)")
        with open('CHANGELOG.md', 'w') as fout:
            fout.writelines(new_md)
        ctx.run('git add CHANGELOG.md')
        rst_content = open('CHANGELOG.rst', 'r').read()
        os.remove('CHANGELOG.rst')
        ctx.run('git add CHANGELOG.rst')
        doc_file = create_docs_changelog(rst_content)
        ctx.run('git add %s' % doc_file)

    return
