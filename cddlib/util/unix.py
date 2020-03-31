#!/usr/bin/env python
#
# Created by Alberto Gobbi
# Maintained by Alberto Gobbi
#

"""
This module provides unix specific functions.

"""
from __future__ import print_function
import subprocess
import sys
from cddlib.util.io import warn


def is_unix() -> bool:
    """Check whether running under linux system.

    @TODO - include Mac/Darwin?

    Paramters
    ---------
    None

    Returns
    -------
    bool
        True if running on Linux; False otherwise.
    """
    return sys.platform.startswith("linux")


def exec_tcsh(cmd: str, fail_on_error: bool = False) -> int:
    """
    Execute command using tcsh.

    Parameters
    ----------
    cmd
        Command to execute
    fail_on_error:
        Flag for whether script should exit on error in executing cmd.
        If True the script will exit on error

    Returns
    -------
    int
        Exit code from command.
    
    >>> com = '''ls ~/.login;\\nls -l ~/.login'''
    >>> exec_tcsh(com)
    0
    
    """
    if not is_unix():
        return 0   # fake execution on windows for debugging
    
    ex = subprocess.call(("/bin/tcsh", "-fc", cmd))
    if ex != 0 and fail_on_error:
        warn("Error executing command:\n%s\n" % cmd)
        exit(1)
    return ex


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
