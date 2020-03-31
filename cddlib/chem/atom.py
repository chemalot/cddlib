"""Abstract base class for objects representing atoms
"""

from abc import ABCMeta
from abc import abstractmethod


class BaseAtom(metaclass=ABCMeta):
    """
        Abstract class hiding the internal representation of an atom object.
    """
    def __init__(self, native_atom_object):
        self._at = native_atom_object

    @property
    @abstractmethod
    def atomic_num(self) -> int:
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass
