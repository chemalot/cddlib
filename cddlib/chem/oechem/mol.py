'''
Abstraction around OpenEye Toolkit Mol to make it independent

Created on Jul 1, 2018

@author: albertgo
'''

import numpy as np

from openeye import oechem
from .atom import Atom
from ..mol import BaseMol


class Mol(BaseMol):
    """
        Implementation of molecule object that uses the openeye toolkit as internal representation.
    """
    def __init__(self, oe_chem_mol):
        BaseMol.__init__(self, oe_chem_mol)

    @property
    def num_atoms(self) -> int:
        return self._mol.NumAtoms()

    @property
    def num_bonds(self) -> int:
        return self._mol.NumBonds()

    @property
    def coordinates(self) -> np.ndarray:
        """
        returns
        -------
        numpy [nAtoms,3]
        """
        ret = np.empty([self._mol.NumAtoms(), 3])
        coords_dict = self._mol.GetCoords()
        for i, at in enumerate(self._mol.GetAtoms()):
            ret[i] = coords_dict[at.GetIdx()]
        return ret

    @coordinates.setter
    def coordinates(self, positions):
        """
        Parameter
        --------
        positions; numpy [natoms,3] 
        """
        oe_coords = np.empty((self._mol.GetMaxAtomIdx(), 3))
        for i, at in enumerate(self._mol.GetAtoms()):
            oe_coords[at.GetIdx()] = positions[i] 
        self._mol.SetCoords(oe_coords.reshape(-1))

    @property
    def atom_types(self):
        """ return array of atomic numbers """
        atom_types = []
        for at in self._mol.GetAtoms():
            atom_types.append(at.GetAtomicNum())

        return atom_types

    @property
    def atom_symbols(self):
        """ return array of atomic symbols """
        atom_sym = []
        for at in self._mol.GetAtoms():
            atom_sym.append(oechem.OEGetAtomicSymbol(at.GetAtomicNum()))

        return atom_sym

    # def set_property(self, name, value):
    #     oechem.OESetSDData(self._mol, name, str(value))

    # def get_property(self, name):
    #     return oechem.OEGetSDData(self._mol, name)

    @property
    def atoms(self):
        return [Atom(at) for at in self._mol.GetAtoms()]

    @property
    def canonical_smiles(self):
        return oechem.OEMolToSmiles(self._mol)

    @property
    def title(self) -> str:
        return self._mol.GetTitle()
         

    def __contains__(self, kee:str) -> bool:
        return oechem.OEHasSDData(self._mol, kee)
    
    
    def __getitem__(self, kee:str ):
        if oechem.OEHasSDData(self._mol, kee):
            return oechem.OEGetSDData(self._mol, kee)
        else:
            raise KeyError("{} has no key {!r}".
                           format(self.__class__.__name__, kee))

    def __setitem__(self, kee, value):
        oechem.OESetSDData(self._mol, kee, str(value))

    def keys(self):
        """this is likely not threadsafe - what happens if a data pair
           is added/deleted between iterations?
        """
        for data_pair in oechem.OEGetSDDataPairs(self._mol):
            yield data_pair.GetTag()

    def items(self):
        """this is likely not threadsafe - what happens if a data pair
           is added/deleted between iterations?
        """
        data = oechem.OEGetSDDataPairs(self._mol)
        for data_pair in data:
            yield data_pair.GetTag(), data_pair.GetValue()


def from_smiles(smi:str) -> Mol:
    """ Create a molecule object from a smiles """
    mol = oechem.OEGraphMol()

    oechem.OESmilesToMol(mol, smi)
    return Mol(mol) 

        
