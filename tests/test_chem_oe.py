from cddlib.chem import atom
from cddlib.chem import mol
from pytest import fixture
from pytest import raises
from importlib import import_module
from cddlib.chem.mol import BaseMol

try:
    from openeye import oechem
except ModuleNotFoundError:
    raise ModuleNotFoundError("Openeye Toolkit not found, some tests will fail");

TEST_TOOLKIT: str = "openeye"
"""Which toolkit to use, specify openeye or rdkit
"""


@fixture
def oe_molecule():
    oe_mol = oechem.OEGraphMol()
    oechem.OESmilesToMol(oe_mol, "C1CCCCC1")
    return new_molecule_for_testing(oe_mol)


def test_mol_with_openeye(oe_molecule):
    assert(isinstance(oe_molecule, mol.BaseMol))


def test_mol_num_atoms_with_openeye(oe_molecule):
    assert(oe_molecule.num_atoms == 6)


def test_mol_num_bonds_with_openeye(oe_molecule):
    assert(oe_molecule.num_bonds == 6)


def test_canonical_smiles_with_openeye(oe_molecule):
    assert(oe_molecule.canonical_smiles == "C1CCCCC1")


def test_mol_atoms_with_openeye(oe_molecule):
    assert(oe_molecule.atoms[0].symbol == "C")


def test_mol_raises_key_error_with_openeye(oe_molecule):
    with raises(KeyError) as excinfo:
        test_value = oe_molecule["Test Prop"]
    assert("Test Prop" in str(excinfo.value))


def test_mol_set_get_item_with_openeye(oe_molecule):
    oe_molecule["TestProp"] = "TEST"
    assert(oe_molecule["TestProp"] == "TEST")


def test_mol_sd_properties_with_openeye(shared_datadir):
    ifs = oechem.oemolistream(str(shared_datadir / "test_CCCO_confs.sdf"))
    mol.TEST_TOOLKIT = "openeye"
    new_mol = oechem.OEGraphMol()
    oechem.OEReadMolecule(ifs, new_mol)
    oe_mol = new_molecule_for_testing(new_mol)
    assert(oe_mol["Total_energy"].strip() == "-6.4528")
    assert(oe_mol["MMFF Bond"].strip() == "0.1421")
    assert(tuple(oe_mol.keys()) ==
           ("MMFF VdW", "MMFF Bond", "MMFF Bend", "MMFF StretchBend",
            "MMFF Torsion", "Sheffield Solvation",
            "Ligand MMFF Intramol. Energy",
            "Total_energy"))

    assert(list(oe_mol.items()) ==
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


