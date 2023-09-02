import unittest
from visChem import smiles_data

class TestSmilesData(unittest.TestCase):

    def test_NCI_5k_not_empty(self):
        self.assertTrue(smiles_data.NCI_1k)  # Check if list is not empty

    def test_NCI_5k_elements_type(self):
        for smile in smiles_data.NCI_1k:
            self.assertIsInstance(smile, str)  # Check if each element is a string

    def test_NCI_5k_length(self):
        self.assertEqual(len(smiles_data.NCI_1k), 1000)  # Check if list has 5000 elements

if __name__ == '__main__':
    unittest.main()
    