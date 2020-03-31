"""
Module containing input/output operations using the OpenEye Toolkit.

Created on Jul 1, 2018

@author: albertgo
"""

from openeye import oechem

from ..io import BaseMolInputStream
from cddlib.chem.oechem.mol import Mol


class MolInputStream(BaseMolInputStream):
    """Provide an iterator for reading molecules using the OpenEye Toolkit

       @TODO specify format?
    """

    def __init__(self, file_path: str):
        BaseMolInputStream.__init__(self, file_path)
        self.ifs = oechem.oemolistream(file_path)
        self.next_mol = None

    def has_next(self) -> bool:
        if self.next_mol is not None:
            return True

        mol = oechem.OEGraphMol()
        if oechem.OEReadMolecule(self.ifs, mol):
            self.next_mol = Mol(mol)
            return True
        else:
            return False

    def __next__(self):
        if not self.has_next():
            raise StopIteration()

        res = self.next_mol
        self.next_mol = None
        return res

    def close(self):
        if self.ifs is not None:
            self.ifs.close()
        self.ifs = None



class MolOutputStream(object):
    """Class for writing molecules to file using the OpenEye Toolkit.

       @TODO specify format?
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.ofs = oechem.oemolostream(file_path)

    def write_mol(self, mol):
        oechem.OEWriteMolecule(self.ofs, mol._mol)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.ofs.close()
    

