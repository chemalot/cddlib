"""
Module with input/output and file-related functions.

# Created by Alberto Gobbi
# Maintained by Alberto Gobbi
#
"""

from __future__ import absolute_import, division, print_function
import sys
import os
import tempfile
import pprint


def read_file(file_path: str) -> str:
    """Return contents of file.

    Parameters
    ----------
    file_path
        Path to file to read.

    Returns
    -------
    str
        contents of file
    """
    with open(file_path, 'r') as f:
        file_string = f.read()
    return file_string


def write_file(file_path: str,
               output_string: str,
               permission: int = None) -> None:
    """Write string to file, overwriting existing files.

    Parameters
    ----------
    file_path
        Path to write file to.
    output_string
        Content to write to file.
    permission
        Numeric mode to set for file.  For possible values see Python 
        documentation for os.chmod

    Returns
    -------
    None
    """
    with open(file_path, 'w') as f:
        f.write(output_string)

    if permission:
        os.chmod(file_path, permission)


def append_to_file(file_path: str, output_string: str) -> None:
    """"Append to content to existing file.

    Parameters
    ----------
    file_path
        Path to file to which to append.
    output_string
        Content to append to file.

    Returns
    -------
    None
    """
    with open(file_path, 'a') as f:
        f.write(output_string)


def write_temp_file(output_string: str,
                    target_dir: str = None, 
                    suffix: str = '',
                    permission: int = None) -> str:
    """Write output_string to temp file. Note the file is not removed.

    Parameters
    ----------
    output_string
        the content to write to the temp file
    target_dir
        directory in which to write temp file
    suffix
        suffix/extension for the file to create; does not put a dot between
        the file name and the suffix; if you need one, put it at the
        beginning of suffix.
    permission
        Numeric mode to set for file.  For possible values see Python
        documentation for os.chmod

    Returns
    -------
    str
        Path to temporary file
    """
    fd, fp = tempfile.mkstemp(suffix=suffix,
                              prefix='tmp',
                              dir=target_dir,
                              text=True)
    write_file(fp, output_string, permission)
    os.close(fd)

    if permission is None:
        # restore permissions as of umask
        old_umask = os.umask(0)
        os.umask(old_umask)
        octal_file_chmod = int('666', 8) - old_umask
        os.chmod(fp, octal_file_chmod)
    else:
        os.chmod(fp, permission)

    return fp


def filesize(file_path: str) -> int:
    """Return the size of a file.

    Parameters
    ----------
    file_path
        path to the file for which to return size

    Returns
    -------
    int
        size of file in bytes
    """

    statinfo = os.stat(file_path)
    return statinfo.st_size


def file_greater0(file_path: str) -> bool:
    """Check whether file has size greater than 0.

    Parameters
    ----------
    file_path
        path to the file for which to check size

    Returns
    -------
    bool
        True if file size is greater than 0
    """
    return os.path.isfile(file_path) and filesize(file_path) > 0


def warn(*argv) -> None:
    """Write to stderr.

    Parameter
    ---------
    *argv
        Content to write.

    Returns
    -------
    None
    """

    print(*argv, file=sys.stderr, flush=True)


def pretty_warn(obj: object) -> None:
    """Pretty print and object to stderr.

    Parameter
    ---------
    obj
        Object to pretty print.

    Returns
    -------
    None
    """

    pp = pprint.PrettyPrinter(indent=2, stream=sys.stderr)
    pp.pprint(obj)
    sys.stderr.flush()
