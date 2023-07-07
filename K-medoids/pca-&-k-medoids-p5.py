import numpy as np
import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
import pandas as pd

# Opening and cleaning the data
with open("C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 "
          "UROP Tianyi/Dimensionality Reduction/PCA/p5.txt") as p5:
    string_p5 = ''.join(p5)
    new_p5 = string_p5.strip("[]")
    no_comma_p5 = new_p5.replace(',', '')
    no_bracket_p5 = no_comma_p5.replace("[", '')
    clean_p5 = no_bracket_p5.replace("]", '')
    final_p5 = clean_p5.split()

# Replacing monomer type with respective HLB values
HLB_p5 = []
for monomer in final_p5:
    if monomer == '1':
        HLB_p5.append(monomer.replace('1', '8.45'))
    elif monomer == '2':
        HLB_p5.append(monomer.replace('2', '11.4'))
    elif monomer == '3':
        HLB_p5.append(monomer.replace('3', '5.12'))
    elif monomer == '4':
        HLB_p5.append(monomer.replace('4', '18.5'))

# Fit and transform the data
x = np.reshape(HLB_p5, (100, 9216)).T
df = pd.DataFrame(x)

# Initialize the PCA model
pca = PCA(n_components=2)
p5_pca = pca.fit_transform(df)

# K-medoids clustering
k = 20 # Set number of clusters
kmedoids = KMedoids(n_clusters=k)
kmedoids.fit(p5_pca)

# Get the cluster labels and medoids
labels = kmedoids.labels_
medoids = kmedoids.medoid_indices_
medoid_coords = p5_pca[medoids, :]

def k_medoids_loss(data, medoids, labels):
    """
    Computes the loss function for k-medoids clustering.

    Parameters:
        data (ndarray): The data points, shape (n_samples, n_features).
        medoids (ndarray): The current medoids indices, shape (n_clusters,).
        labels (ndarray): The cluster assignments for each data point, shape (n_samples,).

    Returns:
        float: The value of the loss function.
    """
    n_samples = data.shape[0]
    loss_value = 0

    for i in range(n_samples):
        cluster = labels[i]
        medoid_idx = medoids[cluster]
        medoid_distances = np.linalg.norm(data[labels == cluster] - data[medoid_idx], axis=1)
        loss_value += np.sum(medoid_distances)

    return loss_value

loss = k_medoids_loss(p5_pca, medoids, labels)
print(f"Loss: {loss}")

fig, ax = plt.subplots()
plt.scatter(p5_pca[:, 0], p5_pca[:, 1], c=labels, s=10, alpha=.50)
plt.scatter(medoid_coords[:, 0], medoid_coords[:, 1], marker='x', s=25, linewidths=1, color='black')
plt.xlabel("PC1", fontsize=16)
plt.ylabel("PC2", fontsize=16)
plt.title('K-medoids Clustering with PCA', fontsize=23)

# Compute and plot boundaries for each medoid cluster
for medoid_index in medoids:
    medoid_label = labels[medoid_index]
    cluster_points = p5_pca[labels == medoid_label]
    hull = ConvexHull(cluster_points)
    boundary_points = cluster_points[hull.vertices]
    boundary_points = np.append(boundary_points, [boundary_points[0]], axis=0)
    ax.plot(boundary_points[:, 0], boundary_points[:, 1], color='black', linewidth=2)


# Get the avg mma_rgi for each sequence
avg_mma_rgi_list = []
for file in range(1, 21):
    with open(f"C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 "
              f"UROP Tianyi/Dimensionality Reduction/MMA_Rg_20seq/MMA_rgi_{file}.txt") as file:
        mma_rgi = []
        for rgi in file:
            mma_rgi.append(float(rgi.strip()))

        avg_mma_rgi = sum(mma_rgi) / 10
        avg_mma_rgi_list.append(avg_mma_rgi)

# Label seq with rgi data
seq1_indices_to_label = [4760, 4776, 5394, 5560, 5886, 644, 7906, 7964, 9091, 986]

seq2_indices_to_label = [90, 9182, 1753, 499, 5519, 8872, 5917, 517, 1, 727]

# for index, txt in enumerate(p5_pca):
#     if index in seq1_indices_to_label:
#         plt.annotate(f"seq{index}", (p5_pca[index, 0], p5_pca[index, 1]))

# for index, txt in enumerate(p5_pca):
#     if index in seq2_indices_to_label:
#         plt.annotate(f"seq{index}", (p5_pca[index, 0], p5_pca[index, 1]))

plt.show()