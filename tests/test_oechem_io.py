'''
Created on Jul 2, 2018

@author: albertgo
'''
import numpy as np
try:
    from cddlib.chem.oechem.io import MolInputStream
except ModuleNotFoundError:
    raise ModuleNotFoundError("Openeye Toolkit not found, cannot run this test");



def test_read(shared_datadir):
    sm = 0.
    with MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            atms = mol.atoms
            for at in atms:
                sm += at.atomic_num
    assert 170 == sm


def test_has_next(shared_datadir):
    sm = 0.
    with MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf')) as inf:
        while inf.has_next():
            mol = inf.__next__()
            atms = mol.atoms
            for at in atms:
                sm += at.atomic_num

    assert 170 == sm


def test_coords(shared_datadir):
    sm = 0.
    with MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            sm += mol.coordinates.sum()
            
    np.testing.assert_almost_equal(sm, 115.7458003279753)
    
    sm = 0.
    with MolInputStream(str(shared_datadir/'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            coords = mol.coordinates
            coords = coords * 2.
            mol.coordinates = coords
            sm += mol.coordinates.sum()
    np.testing.assert_almost_equal(sm, 115.7458003279753*2)


def test_readC5(shared_datadir):
    inf = MolInputStream(str(shared_datadir/'C5.sdf'))
    sm = 0.
    for mol in inf:
        atms = mol.atoms
        for at in atms:
            sm += at.atomic_num
    assert 11 == sm
