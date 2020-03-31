'''
Abstraction around RDKit Mol to make it independent

Created on Jul 1, 2018

@author: albertgo
'''

import numpy as np
from rdkit import Chem
from rdkit.Geometry.rdGeometry import Point3D

from .atom import Atom
from ..mol import BaseMol


class Mol(BaseMol):
    """
        Class implementing a molecule using rdkit as the internal represenation.
    """
    def __init__(self, rd_kit_mol):
        BaseMol.__init__(self, rd_kit_mol)

    @property
    def num_atoms(self):
        return self._mol.GetNumAtoms()

    @property
    def num_bonds(self):
        return self._mol.GetNumBonds()

    @property
    def coordinates(self):
        """
        returns
        -------
        numpy [nAtoms,3]
        """
        return self._mol.GetConformer().GetPositions()

    @coordinates.setter
    def coordinates(self, positions):
        """
        Parameter
        --------
        positions; numpy [natoms,3]
        """
        conf = self._mol.GetConformer()
        for i, p in enumerate(positions.astype(np.float64)):
            p3d = Point3D(p[0], p[1], p[2])
            conf.SetAtomPosition(i, p3d)

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
            atom_sym.append(at.GetSymbol())

        return atom_sym

    @property
    def atoms(self):
        return [Atom(at) for at in self._mol.GetAtoms()]

    @property
    def canonical_smiles(self, isomeric=True) -> str:
        return Chem.MolToSmiles(self._mol, isomeric)

    @property
    def title(self) -> str:
        return self._mol.GetProp('_Name')
         

    def __contains__(self, kee:str) -> bool:
        return self._mol.HasProp(kee)
    
    
    def __getitem__(self, kee):
        if self._mol.HasProp(kee):
            return self._mol.GetProp(kee)
        else:
            raise KeyError("{} has no key {!r}".
                           format(self.__class__.__name__,
                                  kee))

    def __setitem__(self, kee, value):
        self._mol.SetProp(kee, str(value))

    def keys(self):
        return tuple(self._mol.GetPropNames())

    def items(self):
        return self._mol.GetPropsAsDict().items()
    
    
def from_smiles(smi:str) -> Mol:
    """ Create a molecule object from a smiles """
    return Mol( Chem.MolFromSmiles(smi) )


