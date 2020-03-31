from cddlib.chem.mol import from_smiles
from pytest import fixture



@fixture
def molecule():
    return from_smiles('C1CCCC1')


def test_mol(molecule):
    assert molecule.canonical_smiles == 'C1CCCC1'
    
    molecule['ID'] = "testValue"
    assert molecule['ID'] == "testValue"

