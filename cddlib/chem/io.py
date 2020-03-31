'''Module to provide input/output operations for the generic (toolkit agnostic)
   chemistry api.

Created on Feb 13, 2019

@author: albertgo
'''

from abc import ABCMeta
from abc import abstractmethod
from collections import deque
from importlib import import_module
import os
from cddlib.chem.mol import BaseMol
from cddlib.chem.toolkit import TOOLKIT
        

"""str: Specify which chemistry toolkit to use values are openeye or rdkit.
"""


def get_mol_input_stream(*args, **kwargs):
    """ create an input stream for molecules.
        Depending on the TOOLKIT variable this will be either rdkit or openeye.
    """
    
    io_module = _import_iomodule(TOOLKIT)
    instance = io_module.MolInputStream(*args, **kwargs)
    return instance


def get_mol_output_stream(*args, **kwargs):
    """ create an ouptu stream for molecules.
        Depending on the TOOLKIT variable this will be either rdkit or openeye.
    """
    
    io_module = _import_iomodule(TOOLKIT)
    instance = io_module.MolOutputStream(*args, **kwargs)
    return instance


class BaseMolInputStream(metaclass=ABCMeta):
    """
        Base Class for reading molecule objects
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def close(self):
        pass


class MemMolStream(object):
    '''
    Mol Stream that holds a list of molecules in memory
    '''

    def __init__(self, init_list: list = []):
        '''
        Initialize this in memory MolStream

        Arguments
        ---------
        init_list
            list of Mol's to be in the stream, you may also use add_mol
            later.

        '''
        self._mols = deque(init_list)

    def add_mol(self, mol:BaseMol) -> None:
        """Add molecule to the internal list.

        Parameters
        ----------
        mol
            Molecule to append.

        Returns
        -------
        None
        """
        self._mols.append(mol)

    def __enter__(self):
        return self

    def has_next(self) -> bool:
        """Check whether iterator still has molecules.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True is molecules still in list; False otherwise
        """
        if len(self._mols) > 0:
            return True
        return False

    def __iter__(self) -> BaseMol:
        return self

    def __next__(self) -> BaseMol:
        try:
            return self._mols.popleft()
        except IndexError:
            raise StopIteration()

    def __exit__(self, *args):
        self.close()

    def close(self) -> None:
        """Terminate the iterator and free the list of molecules.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._mols = None


def _import_iomodule(TOOLKIT: str):
    if TOOLKIT == "openeye":
        io_module = import_module("cddlib.chem.oechem.io")
    elif TOOLKIT == "rdkit":
        io_module = import_module("cddlib.chem.rdkit.io")
    else:
        raise ValueError(f"TOOLKIT ({TOOLKIT}) not recognized."
                          " Expected values are openeye or rdkit."
                          " You can specify the 'CDDLIB_TOOLKIT' environment variable" )
    return io_module
