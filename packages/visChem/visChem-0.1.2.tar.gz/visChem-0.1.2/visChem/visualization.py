import matplotlib.pyplot as plt
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from adjustText import adjust_text
    
def plot_chemical_structures(embedding, labels, unique_labels, colors, representative_structures, img_size=(300, 300), zoom_factor=0.5, font_size=20, plot_size=(20, 15), save_path=None):
    """
    Visualize chemical structures in a 2D embedding space.
    
    Parameters:
    - embedding (np.array): 2D array representing the embedding of chemical structures.
    - labels (list): Cluster labels for each data point in the embedding.
    - unique_labels (list): Unique cluster labels.
    - colors (list): Colors corresponding to each cluster.
    - representative_structures (dict): Dictionary of representative chemical structures for each cluster.
    - img_size (tuple): Size of the image for each chemical structure. Default is (300, 300).
    - zoom_factor (float): Zoom factor for the images. Default is 0.5.
    - font_size (int): Font size for the cluster labels. Default is 20.
    - plot_size (tuple): Size of the final plot. Default is (20, 15).
    - save_path (str, optional): If provided, saves the plot to the specified path.
    
    Returns:
    - None
    """

    fig, ax = plt.subplots(figsize=plot_size)
    texts = []
    avg_positions = []

    unique_labels = np.unique(labels)
    for cluster, smiles in representative_structures.items():
        avg_position = embedding[labels == cluster].mean(axis=0)
        avg_positions.append(avg_position)

    avg_positions = repel_positions(avg_positions, threshold=5, adjustment=0.5)

    for (label, color) in zip(unique_labels, colors):
        if label == -1:  # Noise
            continue
        idx = labels == label
        plt.scatter(embedding[idx, 0], embedding[idx, 1], s=100, label=f'Cluster {label}', c=[color], alpha=1, edgecolors='black', linewidths=0.5)

    for i, (cluster, smiles) in enumerate(representative_structures.items()):
        mol = Chem.MolFromSmiles(smiles)
        img = mol_to_image(mol, img_size)
        avg_position = avg_positions[i]
        imagebox = OffsetImage(img, zoom=zoom_factor, resample=True, clip_path=None)
        ab = AnnotationBbox(imagebox, avg_position, frameon=True, bboxprops=dict(edgecolor="black", boxstyle="round,pad=0.3"))
        ax.add_artist(ab)
        texts.append(ax.text(avg_position[0], avg_position[1], str(cluster), fontsize=font_size))

    adjust_text(texts)
    plt.title('UMAP projection of the chemical space (structures)', fontsize=30)
    ax = plt.gca()
    ax.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()

def mol_to_image(mol, size=(100, 100)):
    """
    Convert a molecule object to an image representation.
    
    Parameters:
    - mol (rdkit.Chem.rdchem.Mol): An RDKit molecule object.
    - size (tuple, optional): The desired size of the output image. Defaults to (300, 300).
    
    Returns:
    - PIL.PngImagePlugin.PngImageFile: An image representation of the molecule.
    """

    img = Draw.MolToImage(mol, size=size)
    
    # Convert white pixels to transparent
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    
    return img

def repel_positions(positions, threshold=0.5, adjustment=0.2):
    """
    Adjust the given positions of points to minimize overlap, using a repulsion algorithm.
    
    Parameters:
    - positions (list of tuple): A list of (x, y) tuples representing initial positions.
    - k (float, optional): A constant factor for the repulsion calculation. Defaults to 0.1.
    - iterations (int, optional): The number of iterations to perform the adjustment. Defaults to 50.
    
    Returns:
    - list of tuple: A list of (x, y) tuples representing the adjusted positions.
    """

    adjusted_positions = positions.copy()
    for i, pos1 in enumerate(positions):
        for j, pos2 in enumerate(positions):
            if i != j:  # don't compare a position to itself
                distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
                if distance < threshold:
                    direction = np.array(pos1) - np.array(pos2)
                    direction = direction / np.linalg.norm(direction)  # normalize to get unit direction vector
                    adjusted_positions[i] = pos1 + direction * adjustment
    return adjusted_positions