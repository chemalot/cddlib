'''
Abstraction around Atom to make it independent of internal tool kit
representation

Created on Jul 1, 2018

@author: albertgo
'''

from openeye import oechem

from ..atom import BaseAtom


class Atom(BaseAtom):
    """
        Implementation of atom object that uses the openeye toolkit as internal representation.
    """
    def __init__(self, openeye_atom):
        BaseAtom.__init__(self, openeye_atom)

    @property
    def atomic_num(self) -> int:
        return self._at.GetAtomicNum()

    @property
    def symbol(self) -> str:
        return oechem.OEGetAtomicSymbol(self._at.GetAtomicNum())
