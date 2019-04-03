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
import parver

from spines import __version__


#
#   Helpers
#

def log(msg):
    print('[release] %s' % msg)


def print_block(msg):
    print('\n  ----- START -----')
    for line in msg.split('\n'):
        print('  %s' % line)
    print('  -----  END  -----\n')


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
    curr = content.split('\n')
    print(content)
    for i in range(len(curr)):
        line = curr[i].strip('>')
        nxt = curr[i+1] if i+1 < len(curr) else None

        if all(x in ('-', '=') for x in line):
            continue
        if nxt:
            if all(x == '=' for x in nxt):
                line = "## %s\n" % line
            elif all(x == '-' for x in nxt):
                line = "### %s\n" % line
        ret.append(line)
    return '\n'.join(ret) + '\n\n'


def changelog_rst_to_md(ctx, path):
    """Convert a CHANGELOG.rst to a CHANGELOG.md file"""
    content = ctx.run(
        'pandoc %s -f rst -t markdown' % path, hide=True
    ).stdout.strip()
    content = re.sub(
        r"([^\n]+)\n?\s+\[[\\]+(#\d+)\]\(https://github\.com/douglasdaly/[\w\-]+/issues/\d+\)",
        r"\1 \2", content, flags=re.MULTILINE
    )
    return convert_rst_to_markdown(content)


#
#   Tasks
#

@invoke.task
def changelog(ctx, draft=False):
    """Generates the CHANGELOG file"""
    curr_md = open('CHANGELOG.md', 'r').read()
    if draft:
        ctx.run("towncrier --draft > CHANGELOG.draft.rst")
        log('Would clear changes/*')
        md_content = changelog_rst_to_md(ctx, 'CHANGELOG.draft.rst')
        new_md = insert_text(curr_md, md_content, "[//]: # (BEGIN)")
        with open('CHANGELOG.draft.md', 'w') as fout:
            fout.writelines(new_md)
        log('Generated: CHANGELOG.draft.md')
        ctx.run('git add CHANGELOG.draft.md')
        rst_content = open('CHANGELOG.draft.rst', 'r').read()
        os.remove('CHANGELOG.draft.rst')
        log('Would create new docs/changelog file:')
        print_block(create_docs_changelog(rst_content, write=False))

    else:
        ctx.run('git rm CHANGELOG.draft.md')
        ctx.run('towncrier --yes')
        ctx.run('git add changes/')
        md_content = ctx.run(
            'pandoc CHANGELOG.rst -f rst -t markdown', hide=True
        ).stdout.strip()
        new_md = insert_text(curr_md, md_content, "[//] # (BEGIN)")
        with open('CHANGELOG.md', 'w') as fout:
            fout.writelines(new_md)
        ctx.run('git add CHANGELOG.md')
        rst_content = open('CHANGELOG.rst', 'r').read()
        os.remove('CHANGELOG.rst')
        doc_file = create_docs_changelog(rst_content)
        ctx.run('git add %s' % doc_file)

    return

