from cddlib.chem.io import get_mol_input_stream



def test_read(shared_datadir):
    sm = 0.
    with get_mol_input_stream(str(shared_datadir/'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            atms = mol.atoms
            for at in atms:
                sm += at.atomic_num
    assert 170 == sm
