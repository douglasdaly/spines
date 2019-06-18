# -*- coding: utf-8 -*-
"""
Utilities for working with strings.
"""
import difflib
from fnmatch import fnmatch
import re
from textwrap import dedent
from typing import Iterable as T_Iterable
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union
import unicodedata

from .._vendored import autopep8 as _v_autopep8


INDENT_TAB = '    '


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Slugifys the given string

    Convert to ASCII if 'allow_unicode' is False. Convert spaces to
    hyphens. Remove characters that aren't alphanumerics, underscores,
    or hyphens. Convert to lowercase. Also strip leading and trailing
    whitespace.

    .. note::
        Modified (barely) from the Django project:
        https://github.com/django/django/blob/master/django/utils/text.py

    Parameters
    ----------
    value : str
        String to slugify.
    allow_unicode : bool, optional
        Whether or not to allow unicode characters.

    Returns
    -------
    str
        Slugified string.

    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')\
                           .decode('ascii')
    value = re.sub(r'[^\w\s-]', '_', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_diff(a: [str, T_Iterable[str]], b: [str, T_Iterable[str]], n=3):
    """Gets the differences between text data

    Parameters
    ----------
    a : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to compare from.
    b : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to compare with.
    n : int, optional
        Lines of context to show around differences.

    Returns
    -------
    str
        Differences between the texts.

    """
    if isinstance(a, str):
        a = a.splitlines()
    if isinstance(b, str):
        b = b.splitlines()
    return ''.join(
        difflib.context_diff(a, b, fromfile='Current', tofile='New', n=n)
    )


def get_changes(
    a: [str, T_Iterable[str]],
    b: [str, T_Iterable[str]]
) -> List[tuple]:
    """Gets the full set of changes required to go from a to b

    Parameters
    ----------
    a : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to start from.
    b : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to get changes to get to.

    Returns
    -------
    :obj:`list` of :obj:`tuple`
        List of five-tuples of operation, from start index, from end
        index, to start index and to end index.

    """
    if not isinstance(a, str):
        a = '\n'.join(a)
    if not isinstance(b, list):
        b = '\n'.join(b)
    s = difflib.SequenceMatcher(None, a, b)
    return s.get_opcodes()


def format_code_style(code: str) -> str:
    """Formats the given code to be PEP8 compliant

    Parameters
    ----------
    code : str
        Code to format to PEP8 standards using autopep8.

    Returns
    -------
    str
        The formatted code.

    """
    return _v_autopep8.fix_code(dedent(code))


def filter_strings(
    strings: [str, Sequence[str]],
    pattern: [str, Sequence[str]],
    *patterns: Tuple[Union[str, Sequence[str]], ...]
) -> Sequence[str]:
    """Filters the given strings using the given pattern(s)

    Parameters
    ----------
    strings : :obj:`str` or :obj:`Iterable` of :obj:`str`
        String(s) to filter.
    pattern : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Pattern to filter with, can be other string(s), patterns using
        UNIX-style wild-cards or regex strings.
    patterns : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Additional pattern(s) to filter with.

    Returns
    -------
    :obj:`list` of :obj:`str`
        The strings from the given `strings` which matched the
        filters given.
    """
    if isinstance(pattern, str):
        pattern = [pattern]
    for p in patterns:
        if isinstance(p, str):
            pattern.append(p)
        else:
            pattern.extend(p)

    filtered = []
    for s in strings:
        for p in pattern:
            if s == p or fnmatch(s, p) or re.match(s, p):
                filtered.append(s)
    return filtered
