from rdkit import Chem, DataStructs, RDConfig
from rdkit.Chem import AllChem, PandasTools
import numpy as np
import os 

def get_smiles(dataset):
    """
    Load a dataset and extract SMILES strings.
    
    Parameters:
    - dataset (str): Name of the dataset to be loaded.
    
    Returns:
    - list: List of SMILES strings from the dataset.
    """

    drugs_frame = PandasTools.LoadSDF(os.path.join(RDConfig.RDDataDir, dataset))
    return drugs_frame["SMILES"].tolist()

def smiles_to_mol(smiles_list):
    """
    Convert a list of SMILES strings to molecular objects.
    
    Parameters:
    - smiles_list (list): List of SMILES strings.
    
    Returns:
    - list: List of molecular objects corresponding to the input SMILES strings.
    """

    return [Chem.MolFromSmiles(smile) for smile in smiles_list]

def mol_to_fp(mols_list, radius=3, nBits=2048):
    """
    Convert a list of molecular objects to fingerprints.
    
    Parameters:
    - mols_list (list): List of molecular objects.
    - radius (int): Radius of the Morgan fingerprint. Default is 3.
    - nBits (int): Number of bits in the fingerprint. Default is 2048.
    
    Returns:
    - list: List of fingerprints corresponding to the input molecules.
    """

    return [AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits) for mol in mols_list]

def fp_to_np(fp_list):
    """
    Convert a list of fingerprints to a numpy array.
    
    Parameters:
    - fp_list (list): List of molecular fingerprints.
    
    Returns:
    - np.array: Numpy array of the fingerprints.
    """

    np_fps = []
    for fp in fp_list:
        arr = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(fp, arr)
        np_fps.append(arr)
    return np.array(np_fps)