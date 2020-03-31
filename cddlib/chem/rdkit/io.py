#!/usr/bin/env python
"""
Module containing input/output operations using the OpenEye Toolkit.

Created on Jul 1, 2018

@author: albertgo
"""
import io
import gzip
import sys
import re
import os

from rdkit import Chem
from cddlib.chem.rdkit.mol import Mol


class MolInputStream:
    """Provide an iterator for reading molecules using RDKit

       @TODO specify format?
    """
    sdfRE = re.compile(".sdf(.gz)?$", re.I)
    smiRE = re.compile(".smi(.gz)?$", re.I)

    def __init__(self, file_path, **kwargs):

        self.file_path = file_path
        self.next_mol = None

        if MolInputStream.sdfRE.match(file_path) is not None or \
           MolInputStream.smiRE.match(file_path) is not None:
            self._in1 = None
            in_s = sys.stdin.buffer
        else:
            in_s = io.open(self.file_path, "rb")
            self._in1 = in_s

        if self.file_path.endswith("gz"):
            in_s = gzip.open(in_s, mode="rb")
            self._in2 = in_s
        else:
            self._in2 = None

        if MolInputStream.sdfRE.search(self.file_path) is not None:
            if kwargs is None: kwargs = { }
            if "removeHs" not in kwargs:
                kwargs['removeHs'] = False
            if "sanitize" not in kwargs:
                kwargs['sanitize'] = False   # this is more oelike
            
            self._in3 = Chem.ForwardSDMolSupplier(in_s, **kwargs)
            
        #elif MolInputStream.smiRE.search(self.file_path) is not None:
        #   self._in3 = Chem.SmilesMolSupplier(self._in2)
        else:
            raise Exception("Unknown file format: " + self.file_path)

    def __enter__(self):
        return self

    def has_next(self):
        if self.next_mol is not None:
            return True

        try:
            self.next_mol = Mol(self._in3.__next__())
            return True
        except StopIteration:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_mol is not None:
            res = self.next_mol
            self.next_mol = None
            return res

        return Mol(self._in3.__next__())

    def __exit__(self, *args):
        self.close()

    def close(self):
        #self._in3.close()
        if self._in2 is not None:
            self._in2.close()
        if self._in1 is not None: 
            self._in1.close()


class MolOutputStream(object):
    """
        Stream for writing molecules using the rdkit toolkit.
    """
    def __init__(self, file_path):
        self.file_path = file_path

        if self.file_path.endswith("gz"):
            if self.file_path.startswith(".sdf") or self.file_path.startswith(".smi"):
                out = os.fdopen(sys.stdout.fileno(), "wb", closefd=False)
                self._out1 = None
            else:
                out = io.open(self.file_path, "wb")
                self._out1 = out

            out = gzip.open(out, mode = 'wt')
            self._out2 = out
        else:
            if self.file_path.startswith(".sdf") or self.file_path.startswith(".smi"):
                out = sys.stdout
                self._out1 = None
            else:
                out = io.open(self.file_path, 'wt')
                self._out1 = out

            self._out2 = None
            
        if MolInputStream.sdfRE.search(self.file_path) is not None:
            self._out3 = Chem.SDWriter(out)
        elif MolInputStream.smiRE.search(self.file_path) is not None:
            self._out3 = Chem.SmilesWriter(out)
        else:
            raise Exception("Unknown file format: " + self.file_path)

    def write_mol(self, mol):
        self._out3.write(mol._mol)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._out3.close()
        if self._out2 is not None:
            self._out2.close()
        if self._out1 is not None:
            self._out1.close()


# just for demo read and write mols

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="")

    parser.add_argument('-in' ,  metavar='fileName',  dest='inFile', type=str, default=".sdf",
                        help='input file def=.sdf')

    parser.add_argument('-out' ,  metavar='fileName',  dest='outFile', type=str, default=".sdf",
                        help='input file def=.sdf')

    args = parser.parse_args()

    with MolInputStream(args.inFile) as inp,  \
         MolOutputStream(args.outFile) as out:
        for mol in inp:
            out.write_mol(mol)
    
