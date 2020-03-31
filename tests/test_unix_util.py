'''
Created on May 24, 2018

@author: albertgo
'''
from cddlib.util.unix import exec_tcsh


def test_exec_tcsh():
    com = "ls ~;\nls -l ~"
    assert 0 == exec_tcsh(com)
