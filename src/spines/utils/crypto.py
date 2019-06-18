# -*- coding: utf-8 -*-
"""
Cryptographic utilities for Spines.
"""
from hashlib import sha256
import os
from typing import Dict
from typing import Sequence
from typing import Tuple

from .string import filter_strings


HASH_FUNCTION = sha256
HASH_EXTENSION = '.sha256'

_CHUNK_SIZE = 1024


def hash_file(
    path: str,
    *paths: Tuple[str, ...],
    binary_mode: bool = False,
    chunk_size: int = None
) -> str:
    """Calculates the hash for the given file

    Parameters
    ----------
    path : str
        Path to the file to hash.
    paths : :obj:`str`
        Additional paths to join to the `path` to the file to get the
        hash for.
    binary_mode : bool, optional
        Whether or not to read the file in binary mode (default is
        :obj:`False`).
    chunk_size : int, optional
        The number of bytes/characters to read from the file at a time.
        If :obj:`None` it will use a sensible default, if set to
        :obj:`-1` it will not read the file in chunks.

    Returns
    -------
    str
        The hash of the file given (encoded in hexadecimal form).

    Raises
    ------
    ValueError
        If the given `chunk_size` is not a valid value.

    """
    if not chunk_size:
        chunk_size = _CHUNK_SIZE
    elif chunk_size == 0 or chunk_size < -1:
        raise ValueError("Invalid chunk size given: %s" % chunk_size)

    if paths:
        path = os.path.join(path, *paths)

    def _read_helper(file_in):
        if chunk_size > 0:
            rv = file_in.read(chunk_size)
        else:
            rv = file_in.read()
        if not binary_mode:
            return rv.encode()
        return rv

    def _read_chunked(file_in, msg):
        b = _read_helper(file_in)
        while b:
            msg.update(b)
            b = _read_helper(file_in)
        return

    def _read_full(file_in, msg):
        b = _read_helper(file_in)
        msg.update(b)
        return

    read_mode = 'r'
    if binary_mode:
        read_mode += 'b'

    m = HASH_FUNCTION()
    with open(path, read_mode) as fin:
        if chunk_size > 0:
            _read_chunked(fin, m)
        else:
            _read_full(fin, m)

    return m.digest().hex()


def generate_hash_file(
    path: str,
    *paths: Tuple[str, ...],
    output: str = None,
    recurse: bool = True,
    overwrite: bool = True,
    include: [str, Sequence[str]] = None,
    exclude: [str, Sequence[str]] = None,
    binary_mode: bool = False,
    binary_include: [str, Sequence[str]] = None,
    binary_exclude: [str, Sequence[str]] = None
) -> str:
    """Generates the hash file for the given path

    Parameters
    ----------
    path : str
        Path to the file or directory to generate a hash file for.
    paths : str, optional
        Additional path components to append to `path`.
    output : str, optional
        Path to the generated hash file (defaults to the path generated
        from :function:`generate_hash_file_name`).
    recurse : bool, optional
        Whether or not to recurse subdirectories when generating the
        hash file (if the given `path` is a directory).
    overwrite : bool, optional
        Whether or not to overwrite an existing hash file for the same
        `path`.
    include : :obj:`str` or :obj:`Iterable` of :obj:`str`
        File(s), pattern(s) or regex strings to use when determining
        which files to include when generating the hash for a directory.
    exclude : :obj:`str` or :obj:`Iterable` of :obj:`str`
        File(s), pattern(s) or regex strings to use when determining
        which files to exclude when generating the hash for a directory.
    binary_mode : bool, optional
        Generate the hashes in binary mode (default is :obj:`False`).
    binary_include : :obj:`str` or :obj:`Iterable` of :obj:`str`
        File(s), pattern(s) or regex strings to use when determining
        which files to include when generating the hash in binary mode
        for a directory.
    binary_exclude : :obj:`str` or :obj:`Iterable` of :obj:`str`
        File(s), pattern(s) or regex strings to use when determining
        which files to exclude when generating the hash in binary mode
        for a directory.

    Returns
    -------
    str
        Path to the generated hash file.

    Raises
    ------
    FileExistsError
        If the `output` file already exists and `overwrite` is set to
        :obj:`False`.

    See Also
    --------
    generate_hash_file_name, hash_file

    """
    if paths:
        path = os.path.join(path, *paths)

    if not output:
        output = generate_hash_file_name(path)

    if os.path.exists(output):
        if not overwrite:
            raise FileExistsError("Hash file already exists: %s" % output)
        os.remove(output)

    if os.path.isfile(path):
        contents = _generate_hash_file_line(
            path, root=os.path.dirname(path), binary_mode=binary_mode
        )
    else:
        contents = []
        for dirpath, subdirs, filenames in os.walk(path):
            if not recurse:
                subdirs.clear()
            filt_files = _get_file_mapping(
                filenames, include=include, exclude=exclude
            )
            bin_modes = _get_file_mapping(
                filenames, default=binary_mode, include=binary_include,
                exclude=binary_exclude
            )
            for file in [k for k, v in filt_files.items() if v]:
                contents.append(_generate_hash_file_line(
                    os.path.join(dirpath, file),
                    root=path,
                    binary_mode=bin_modes[file]
                ))
        contents = ''.join(contents)

    with open(output, 'w') as fout:
        fout.write(contents)

    return output


def _generate_hash_file_line(path, root=None, binary_mode=False):
    """Generates a single line for the hash file"""
    f_hash = hash_file(path, binary_mode=binary_mode)
    if root:
        f_name = path.replace(root, '').strip(os.sep)
    else:
        f_name = os.path.basename(path).strip(os.sep)
    if binary_mode:
        mode_str = '*'
    else:
        mode_str = ' '
    return f"{f_hash} {mode_str}{f_name}\n"


def _get_file_mapping(
    filenames: Sequence[str],
    default: bool = True,
    include: [str, Sequence[str]] = None,
    exclude: [str, Sequence[str]] = None
) -> Dict[str, bool]:
    """Helper to get a mapping of file to value for the given filters"""
    if include:
        inc_files = filter_strings(filenames, include)
    else:
        inc_files = []
    if exclude:
        exc_files = filter_strings(filenames, exclude)
    else:
        exc_files = []

    ret = {}
    for file in filenames:
        if file in inc_files:
            ret[file] = True
        elif file in exc_files:
            ret[file] = False
        else:
            ret[file] = default
    return ret


def load_hashes(path, *paths: Tuple[str, ...]) -> Dict[str, Tuple[bool, str]]:
    """Loads the hashes from the given file

    Parameters
    ----------
    path : str
        Path to the file or directory to load hashes from.
    paths : str, optional
        Additional path(s) to the file or directory to join to get the
        path of the file to load the hashes from.

    Returns
    -------
    :obj:`dict` of :obj:`str` to :obj:`tuple` of (:obj:`str`,
    :obj:`bool`)
        Dictionary of file to a tuple of the hash value and whether or
        not the hash was done in binary form.

    """
    if paths:
        path = os.path.join(path, *paths)

    if os.path.isdir(path):
        path = os.path.join(path, os.path.basename(path) + HASH_EXTENSION)

    ret = {}
    with open(path, 'r') as fin:
        for line in fin.readlines():
            h_str, f_str = line.split()
            bin_mode = False
            if f_str.startswith("*"):
                bin_mode = True
                f_str = f_str[1:]
            ret[f_str] = (bin_mode, h_str)
    return ret


def verify_hashes(
    path: str,
    *paths: Tuple[str, ...],
    hash_path: str = None,
    recurse: bool = True,
    ignore_missing: bool = False
) -> Dict[str, bool]:
    """Verifies the hashes for the given path

    Parameters
    ----------
    path : str
        Path to the file or directory to verify.
    paths : str, optional
        Additional paths to the file or directory to join.
    hash_path : str, optional
        File containing the hashes to verify with.  If not provided an
        attempt will be made to find the correct one.
    recurse : bool, optional
        Whether or not, when verifying a directory, to also recursively
        verify any sub-directories.
    ignore_missing : bool, optional
        Whether or not to include files which do not have hash file
        entries in the results (the default is :obj:`False`, include
        missing files in the results).  If this option is set the value
        for any missing files will be :obj:`False`.

    Returns
    -------
    :obj:`dict` of :obj:`str` to :obj:`bool`
        Dictionary of files and whether or not they were verified with
        the hashes.

    """
    if paths:
        path = os.path.join(path, *paths)

    if not hash_path:
        hash_path = find_hash_file(path)
    if not hash_path:
        raise FileNotFoundError(
            "Could not find the hash file, please provide the hash_path"
        )
    l_hashes = load_hashes(hash_path)

    if os.path.isfile(path):
        bin_mode, l_hash = l_hashes.get(os.path.basename(path), (False, None))
        if l_hash and l_hash == hash_file(path, binary_mode=bin_mode):
            return {path: True}
        else:
            return {path: False}

    ret = {}
    for dirpath, subdirs, filenames in os.walk(path):
        if not recurse:
            subdirs.clear()
        for file in filenames:
            if file.endswith(HASH_EXTENSION):
                continue
            f_path = os.path.join(dirpath, file)
            f_name = f_path.replace(path, '', 1).strip(os.path.sep)
            if f_name not in l_hashes.keys():
                if ignore_missing:
                    continue
                ret[f_name] = False
            else:
                f_mode, f_hash = l_hashes[f_name]
                ret[f_name] = f_hash == hash_file(f_path, binary_mode=f_mode)
    return ret


def find_hash_file(path: str, *paths: Tuple[str, ...]) -> str:
    """Finds the relevant hash file for the given path

    Parameters
    ----------
    path : str
        Path to the file or directory to verify.
    paths : str, optional
        Additional paths to the file or directory to join.

    Returns
    -------
    str
        The path to the hash file (if it exists, :obj:`None` otherwise).

    """
    if paths:
        path = os.path.join(path, *paths)

    file_name = generate_hash_file_name(path)
    if os.path.exists(file_name):
        return file_name

    path = os.path.dirname(path)
    file_name = generate_hash_file_name(path)
    if os.path.exists(file_name):
        return file_name

    return


def generate_hash_file_name(path: str, *paths: Tuple[str, ...]) -> str:
    """Generates the name for the hash file for the given path

    Parameters
    ----------
    path : str
        Path to the file or directory to generate a hash file name for.
    paths : str, optional
        Additional paths to the file or directory to join.

    Returns
    -------
    str
        The generated hash file path.

    """
    if os.path.isfile(path):
        return path + HASH_EXTENSION
    return os.path.join(path, os.path.basename(path) + HASH_EXTENSION)
