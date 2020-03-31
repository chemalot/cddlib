'''
Created on Jul 2, 2018

@author: albertgo
'''
import pytest
try:
    from cddlib.chem.rdkit.io import MolInputStream
except ModuleNotFoundError:
    raise ModuleNotFoundError("RDKit Toolkit not found, cannot run this test");



def test_read(shared_datadir):
    inf = MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf'))
    sm = 0.
    for mol in inf:
        atms = mol.atoms
        for at in atms:
            sm += at.atomic_num
    assert 170 == sm


def test_has_next(shared_datadir):
    inf = MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf'))
    sm = 0.
    while inf.has_next():
        mol = inf.__next__()
        atms = mol.atoms
        for at in atms:
            sm += at.atomic_num

    assert 170 == sm


def test_readC5(shared_datadir):
    inf = MolInputStream(str(shared_datadir/'C5.sdf'))
    sm = 0.
    for mol in inf:
        atms = mol.atoms
        for at in atms:
            sm += at.atomic_num
    assert 11 == sm
