import unittest
import numpy as np
from visChem import utils

class TestUtilsFunctions(unittest.TestCase):

    def test_compute_tanimoto(self):
        fps = np.array([[1, 0, 1], [1, 1, 0]])
        result = utils.compute_tanimoto(fps)
        self.assertEqual(result.shape, (2, 2))

    def test_tanimoto_similarity(self):
        fp1 = np.array([1, 0, 1])
        fp2 = np.array([1, 1, 0])
        similarity = utils.tanimoto_similarity(fp1, fp2)
        self.assertTrue(0 <= similarity <= 1)

    def test_reduce_dimensionality(self):
        dist_matrix = np.random.rand(10, 10)
        reduced = utils.reduce_dimensionality(dist_matrix)
        self.assertEqual(reduced.shape, (10, 2))

    def test_perform_clustering(self):
        embedding = np.array([[1, 2], [3, 4], [5, 6]])
        clusters = utils.perform_clustering(embedding)
        self.assertEqual(len(clusters), 3)

if __name__ == "__main__":
    unittest.main()

