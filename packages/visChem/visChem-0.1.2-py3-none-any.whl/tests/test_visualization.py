import unittest
import numpy as np
from visChem import visualization
import matplotlib
matplotlib.use('Agg')

class TestVisualizationFunctions(unittest.TestCase):

    def test_plot_chemical_structures(self):
        embedding = np.array([[1, 2], [3, 4], [5, 6]])
        labels = np.array([0, 1, 1])
        unique_labels = np.array([0, 1])
        colors = ['red', 'blue']
        representative_structures = {0: "CCO", 1: "CCN"}

        # Check if function runs without errors
        try:
            visualization.plot_chemical_structures(embedding, labels, unique_labels, colors, representative_structures)
            result = True
        except:
            result = False
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
