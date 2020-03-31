'''
Created on Mar 2, 2019

@author: albertgo
'''
from cddlib.util.iterate import PushbackIterator


    
def test_pushback_iter():
    it = "string".__iter__()
    pb_it = PushbackIterator(it)
    
    assert 's' == pb_it.__next__()
    pb_it.pushback('S')
    
    assert "".join(pb_it) == 'String'
    
    assert pb_it.has_next() is False
    
    pb_it.pushback('z')
    assert pb_it.has_next()
    assert 'z' == pb_it.__next__()
