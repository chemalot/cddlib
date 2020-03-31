from cddlib.chem import atom
from cddlib.chem import mol
from pytest import fixture
from pytest import raises
from importlib import import_module
from cddlib.chem.mol import BaseMol

try:
    from rdkit import Chem
except ModuleNotFoundError:
    raise ModuleNotFoundError("RDKit Toolkit not found, some tests will fail");


TEST_TOOLKIT: str = "rdkit"
"""Which toolkit to use, specify openeye or rdkit
"""




@fixture
def rd_molecule():
    rd_mol = Chem.MolFromSmiles("C1CCCCC1")
    return new_molecule_for_testing(rd_mol)


def test_mol_with_rdkit(rd_molecule):
    assert(isinstance(rd_molecule, mol.BaseMol))


def test_mol_num_atoms_with_rdkit(rd_molecule):
    assert(rd_molecule.num_atoms == 6)


def test_mol_num_bonds_with_rdkit(rd_molecule):
    assert(rd_molecule.num_bonds == 6)


def test_canonical_smiles_with_rdkit(rd_molecule):
    assert(rd_molecule.canonical_smiles == "C1CCCCC1")


def test_mol_atoms_with_rdkit(rd_molecule):
    assert(rd_molecule.atoms[0].symbol == "C")


def test_mol_set_get_item_with_rdkit(rd_molecule):
    rd_molecule["TestProp"] = "TEST"
    assert(rd_molecule["TestProp"] == "TEST")


def test_mol_raises_key_error_with_rdkit(rd_molecule):
    with raises(KeyError) as excinfo:
        test_value = rd_molecule["Test Prop"]
    assert("Test Prop" in str(excinfo.value))


def test_mol_sd_properties_with_rdkit(shared_datadir):
    sdf_mol_supplier = Chem.SDMolSupplier(str(shared_datadir /
                                              "test_CCCO_confs.sdf"))
    mol.TEST_TOOLKIT = "rdkit"
    rd_mol = new_molecule_for_testing(sdf_mol_supplier[0])
    assert(rd_mol["Total_energy"].strip() == "-6.4528")
    assert(rd_mol["MMFF Bond"].strip() == "0.1421")
    assert(tuple(rd_mol.keys()) ==
           ("MMFF VdW", "MMFF Bond", "MMFF Bend", "MMFF StretchBend",
            "MMFF Torsion", "Sheffield Solvation",
            "Ligand MMFF Intramol. Energy",
            "Total_energy"))

    assert(list(rd_mol.items()) ==
           [('MMFF VdW', '   1.7969'),
            ('MMFF Bond', '   0.1421'),
            ('MMFF Bend', '   0.2773'),
            ('MMFF StretchBend', '   0.0063'),
            ('MMFF Torsion', '  -3.9742'),
            ('Sheffield Solvation', '  -4.7012'),
            ('Ligand MMFF Intramol. Energy', '  -1.7516'),
            ('Total_energy', '  -6.4528')])



def new_molecule_for_testing(*args, **kwargs) -> BaseMol:
    """ To be used for testing only as the TOOLKIT global var needs to be set"""
    # TODO: think about making toolkit a parameter and removing global var
    
    if TEST_TOOLKIT.lower() == "openeye":
        mol_module = import_module("cddlib.chem.oechem.mol")
    elif TEST_TOOLKIT.lower() == "rdkit":
        mol_module = import_module("cddlib.chem.rdkit.mol")
    else:
        raise ValueError("TEST_TOOLKIT not recognized."
                         " Expected values are openeye or rdkit")

    instance = mol_module.Mol(*args, **kwargs)
    return instance

