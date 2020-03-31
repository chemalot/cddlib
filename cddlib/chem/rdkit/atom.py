'''
Abstraction around RDKit Atom to make it independent

Created on Jul 1, 2018

@author: albertgo
'''

from ..atom import BaseAtom


class Atom(BaseAtom):
    """
        Atom class that uses the rdkit implementation as internal representation.
    """
    def __init__(self, rd_kit_atom):
        BaseAtom.__init__(self, rd_kit_atom)

    @property
    def atomic_num(self) -> int:
        return self._at.GetAtomicNum()

    @property
    def symbol(self) -> str:
        return self._at.GetSymbol()
