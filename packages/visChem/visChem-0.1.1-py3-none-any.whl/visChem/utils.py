from scipy.spatial.distance import pdist, squareform
import umap
import hdbscan
import numpy as np

def compute_tanimoto(all_fps):
    """
    Compute the Tanimoto similarity matrix for a list of fingerprints.
    
    Parameters:
    - all_fps (list): List of molecular fingerprints.
    
    Returns:
    - np.array: Tanimoto similarity matrix.
    """

    return 1 - squareform(pdist(all_fps, metric="jaccard"))

def tanimoto_similarity(fp1, fp2):
    """
    Compute the Tanimoto similarity between two fingerprints.
    
    Parameters:
    - fp1, fp2 (np.array): Two molecular fingerprints for comparison.
    
    Returns:
    - float: Tanimoto similarity score between the two fingerprints.
    """

    intersect = np.dot(fp1, fp2)
    return intersect / (np.sum(fp1) + np.sum(fp2) - intersect)

def reduce_dimensionality(dist_matrix, n_neighbors=2, min_dist=0.1, random_state=2):
    """
    Reduce the dimensionality of a distance matrix using UMAP.
    
    Parameters:
    - dist_matrix (np.array): Distance matrix to be reduced in dimension.
    - n_neighbors (int): Number of neighbors considered for manifold approximation. Default is 2.
    - min_dist (float): Minimum distance between points in the low-dimensional space. Default is 0.1.
    - random_state (int): Seed used for reproducibility. Default is 2.
    
    Returns:
    - np.array: Reduced-dimension representation of the distance matrix.
    """

    return umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, metric='precomputed', random_state=random_state).fit_transform(dist_matrix)

def perform_clustering(embedding, min_cluster_size=3, min_samples=10):
    """
    Perform HDBSCAN clustering on an embedding.
    
    Parameters:
    - embedding (np.array): Low-dimensional representation of data.
    - min_cluster_size (int): Minimum size of clusters. Default is 3.
    - min_samples (int): Minimum number of samples in a dense region. Default is 10.
    
    Returns:
    - list: Cluster labels for each data point in the embedding.
    """

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, gen_min_span_tree=True)
    return clusterer.fit_predict(embedding)