#!/usr/bin/env python
"""
Module with string-related functions.

#
# Created by Alberto Gobbi
# Maintained by Alberto Gobbi
#
"""
import re


def strip_spaces_as_in_first_line(txt: str, strip_prefix_newline=True) -> str:
    """
    Remove leading spaces from all lines in txt.

    The number of spaces striped is equal to the number of spaces in the
    first line of the text.

    Parameters
    ----------
    txt
        The text to strip.
    strip_prefix_newline
        Flag for whether to remove all newlines from the beginning of
        txt prior to processing.

    >>> t='''\\n            abc\\n            def'''
    >>> strip_spaces_as_in_first_line(t)
    'abc\\ndef'

    Returns
    -------
    str
        txt with leading spaces stripped.
    """
    if strip_prefix_newline:
        txt = re.sub("^[\n\a\r]+", "", txt)

    m = re.search('^ +', txt, re.M)
    if not m:
        return txt
    leading_space = '^' + (m.group())
    return re.sub(leading_space, "", txt, 0, re.M)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    