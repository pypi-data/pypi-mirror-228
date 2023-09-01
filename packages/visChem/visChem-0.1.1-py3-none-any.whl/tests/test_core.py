import unittest
from visChem import core
import numpy as np

class TestCoreFunctions(unittest.TestCase):

    def test_smiles_to_mol(self):
        smiles_list = ["CCO", "CCN"]
        mols = core.smiles_to_mol(smiles_list)
        self.assertEqual(len(smiles_list), len(mols))
        self.assertTrue(all(mol is not None for mol in mols))

    def test_mol_to_fp(self):
        smiles_list = ["CCO", "CCN"]
        mols = core.smiles_to_mol(smiles_list)
        fps = core.mol_to_fp(mols)
        self.assertEqual(len(mols), len(fps))

    def test_fp_to_np(self):
        smiles_list = ["CCO", "CCN"]
        mols = core.smiles_to_mol(smiles_list)
        fps = core.mol_to_fp(mols)
        np_fps = core.fp_to_np(fps)
        self.assertEqual(len(fps), len(np_fps))
        self.assertTrue(all(isinstance(np_fp, np.ndarray) for np_fp in np_fps))

if __name__ == "__main__":
    unittest.main()

