import unittest
import numpy as np
from visChem import utils

class TestUtilsFunctions(unittest.TestCase):

    def test_compute_tanimoto(self):
        fps = np.array([[1, 0, 1], [1, 1, 0]])
        result = utils.compute_tanimoto(fps)
        self.assertEqual(result.shape, (2, 2))

    def test_tanimoto_similarity(self):
        fp1 = np.array([1, 0, 1, 1, 0])
        fp2 = np.array([1, 1, 1, 0, 0])
        result = utils.tanimoto_similarity(fp1, fp2)
        self.assertEqual(result, 0.5)

    def test_reduce_dimensionality(self):
        dist_matrix = np.random.rand(10, 10)
        reduced = utils.reduce_dimensionality(dist_matrix)
        self.assertEqual(reduced.shape, (10, 2))

    def test_perform_clustering(self):
        embedding = np.array([[1, 2], [3, 4], [5, 6]])
        clusters = utils.perform_clustering(embedding)
        self.assertEqual(len(clusters), 3)

    def test_get_representative_structures(self):
        labels = np.array([0, 0, 1, 1, -1, 2, 2])
        np_fps = np.array([
            [1, 0, 1, 1, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 1],
            [0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 1, 0]
        ])
        smiles = ["A", "B", "C", "D", "E", "F", "G"]
        
        result = utils.get_representative_structures(labels, np_fps, smiles)
        # The expected result is based on the closest structure to the average fingerprint for each cluster
        expected = {
            0: "A",  # Because "A" and "B" are in the same cluster, but "A" is closer to the average
            1: "D",  # Similarly, "D" is closer to the average of "C" and "D"
            2: "G"   # "G" is closer to the average of "F" and "G"
        }
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
