'''
Created on Mar 2, 2019

@author: albertgo
'''

from typing import Generic, TypeVar, List

T = TypeVar('T')

class PushbackIterator(Generic[T]):
    """ Wraps an iterator adding the pushback() method
    """
    
    def __init__(self, iterator):
        """
        Parameter
        --------
        iterator: iterator to be wrapped
        """
        
        self.__dict__['_iterator'] = iterator
        self.__dict__['_pushed']   = []
        
    def pushback(self, item:T):
        """ return item to the top of the iterator """
        
        self._pushed.append(item)
        
    def __next__(self) -> T:
        if len(self._pushed):
            return self._pushed.pop()
        else:
            return self._iterator.__next__()

    def has_next(self) -> bool:
        if len(self._pushed): return True

        try:
            self.pushback(self._iterator.__next__())
        except StopIteration:
            return False
        return True

    
    def __iter__(self):
        return self


    def __getattr__(self, attr):
        return getattr(self._iterator, attr)

    def __setattr__(self, attr, value):
        return setattr(self._iterator, attr, value)