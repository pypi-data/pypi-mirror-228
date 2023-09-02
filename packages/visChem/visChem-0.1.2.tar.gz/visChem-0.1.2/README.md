# visChem v0.1.2

Steve Niu[^1]

`visChem` is a Python module designed for visualizing chemical space using UMAP and clustering techniques. This tool facilitates the transformation of chemical structures into a 2D space and visualizes clusters of similar compounds.


## Installation
Install using pypi
```
pip install visChem==0.1.2
```

Install using conda
```
conda install -c stevexniu vischem=0.1.2
```

**Note**: Some packages like `rdkit` might require special installation instructions. Please refer to their official documentation for details.

## Usage

1. See `example.py` for details.
2. Run ```python example.py```.

The `example.py` script will execute the main function which:  
- Load example 1000 SMILES from RDKit NCI/first_5K.smi.  
- Converts SMILES to molecular representations.  
- Generates molecular fingerprints.  
- Computes Tanimoto similarity.  
- Reduces dimensionality using UMAP.  
- Performs clustering.  
- Visualizes the chemical structures in the clustered chemical space below.

![output](output_image.png)

Refer to `example.py` for details and any potential modifications you might want to make for your specific use case.

[^1]: Safety Assessment, niu.steve@gene.com