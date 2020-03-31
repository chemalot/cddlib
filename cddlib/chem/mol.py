"""Abstact base class for objects representing molecules
"""


from abc import ABCMeta
from abc import abstractmethod
from importlib import import_module
import numpy as np
from cddlib.chem.atom import BaseAtom
from typing import List
from cddlib.chem.toolkit import TOOLKIT



class BaseMol(metaclass=ABCMeta):
    """Abstract base class for toolkit agnostic molecule representation.
    """
    
    def __init__(self, native_mol_object, isomeric_smiles=True):
        """Constructor for molecules.

        Parameters
        ----------
        native_mol_object
            Toolkit molecule object wrapped by BaseMol; either an
            oechem.GraphMol or rdkit.Chem.rdchem.Mol
        isomeric_smiles
            Flag for whether to generate isomeric SMILES when 
            canonical_smiles is called

        Returns
        -------
        BaseMol derived object
            Wrapped molecule
        """

        assert native_mol_object is not None, "Invalid None molecule"
        self._mol = native_mol_object
        self._isomeric_smiles = isomeric_smiles

    
    @property
    @abstractmethod
    def num_atoms(self) -> int:
        """Number of atoms in molecule.
        """
        pass

    @property
    @abstractmethod
    def num_bonds(self) -> int:
        """Number of bonds in molecule.
        """
        pass

    @property
    @abstractmethod
    def coordinates(self) -> np.ndarray:
        """Return a numpy array containing atomic coordinates.
        @TODO numpy array or generator? 
        returns
        -------
        numpy [nAtoms,3]
        """
        pass

    @coordinates.setter
    @abstractmethod
    def coordinates(self, positions:np.ndarray):
        pass

    @property
    @abstractmethod
    def atoms(self) -> List[BaseAtom]:
        pass

    @property
    @abstractmethod
    def atom_symbols(self) -> List[str]:
        """ return array of atomic symbols """
        pass
    
    @property
    @abstractmethod
    def atom_types(self) -> List[int]:
        """ return array of atomic numbers """
        pass
    
    @property
    def isomeric_smiles(self) -> bool:
        """ True if the isomeric smiles will be returned when calling canonical_smiles """ 
        return self._isomeric_smiles

    @isomeric_smiles.setter
    def isomeric_smiles(self, value: bool):
        """ True means the isomeric smiles will be returned when calling canonical_smiles """ 
        self._isomeric_smiles = value

    @property
    @abstractmethod
    def canonical_smiles(self):
        pass
    
    
    @property
    @abstractmethod
    def title(self) -> str:
        pass
    
    @abstractmethod
    def __contains__(self, kee):
        pass
        
    def get(self, name, default):
        if name in self: return name
        return default
    
    @abstractmethod
    def __getitem__(self, kee):
        pass

    @abstractmethod
    def __setitem__(self, kee, value):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def items(self):
        pass


def from_smiles(smi:str) -> BaseMol:
    if TOOLKIT.lower() == "openeye":
        mol_module = import_module("cddlib.chem.oechem.mol")
    elif TOOLKIT.lower() == "rdkit":
        mol_module = import_module("cddlib.chem.rdkit.mol")
    else:
        raise ValueError("TOOLKIT not recognized."
                         " Expected values are openeye or rdkit")

    return mol_module.from_smiles(smi)
