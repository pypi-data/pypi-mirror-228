
# visChem v0.1

Steve Niu[^1]

`visChem` is a Python module designed for visualizing chemical space using UMAP and clustering techniques. This tool facilitates the transformation of chemical structures into a 2D space and visualizes clusters of similar compounds.


## Installation

1. Clone the repository:
```
git clone visChem  | cd visChem
```

2. Install the required packages:
```
pip install -r requirements.txt
```

**Note**: Some packages like `rdkit` might require special installation instructions. Please refer to their official documentation for details.

## Usage

1. Prepare your data file, e.g., 'NCI/first_200.props.sdf'.
2. Run the `example.py` script:
```
python example.py
```

This script will execute the main function which:  
- Reads the SMILES from the data file.  
- Converts SMILES to molecular representations.  
- Generates molecular fingerprints.  
- Computes Tanimoto similarity.  
- Reduces dimensionality using UMAP.  
- Performs clustering.  
- Visualizes the chemical structures in the clustered chemical space below.
![output](output_image.png)

Refer to `example.py` for details and any potential modifications you might want to make for your specific use case.

[^1]: Safety Assessment, <niu.steve@gene.com>