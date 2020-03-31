'''
Created on May 24, 2018

@author: albertgo
'''

from cddlib.util.string import strip_spaces_as_in_first_line


def test_strip_spaces_as_in_first_line():
    t='''\n            abc\n            def'''
    res = strip_spaces_as_in_first_line(t)
    assert res == 'abc\ndef'

    t='''       \n            abc\n            def'''
    res = strip_spaces_as_in_first_line(t, strip_prefix_newline=False)
    assert res == '\n     abc\n     def'
