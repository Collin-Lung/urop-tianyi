import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import pdist, squareform

sns.set(style='white', context='notebook', rc={'figure.figsize': (14, 10)})

# Opening and cleaning data
with open("C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 "
          "UROP Tianyi/Dimensionality Reduction/PCA/p5.txt") as p5:
    string_p5 = ''.join(p5)
    new_p5 = string_p5.strip("[]")
    no_comma_p5 = new_p5.replace(',', '')
    no_bracket_p5 = no_comma_p5.replace("[", '')
    clean_p5 = no_bracket_p5.replace("]", '')
    final_p5 = clean_p5.split()

# Replacing monomers with respective HBL values
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

# Converting HBL values from strings to floats
numerical_HLB_p5 = list(map(float, HLB_p5))

# Initialize the UMAP model
reducer = umap.UMAP()

# Fit and transform the data
reshaped_HLB_p5 = np.reshape(numerical_HLB_p5, (100, 9216)).T
HLB_df = pd.DataFrame(reshaped_HLB_p5)
HLB_p5_umap = reducer.fit_transform(HLB_df)

# # Marking the sequences with MD data in the scatter plot
# seq3_index = [5394]
# seq15_index = [5519]
#
# for index, txt in enumerate(HLB_p5_data_reduced):
#     if index in seq3_index:
#         plt.annotate("seq3", (HLB_p5_data_reduced[index, 0], HLB_p5_data_reduced[index, 1]))
#
# for index, txt in enumerate(HLB_p5_data_reduced):
#     if index in seq15_index:
#         plt.annotate("seq15", (HLB_p5_data_reduced[index, 0], HLB_p5_data_reduced[index, 1]))


# Creating a scatter plot of the reduced data
plt.scatter(HLB_p5_umap[:, 0], HLB_p5_umap[:, 1], alpha=.5)
plt.title("p5 UMAP Scatter Plot", fontsize=40, fontfamily="Arial")
plt.xlabel("UMAP1", fontsize=35)
plt.ylabel("UMAP2", fontsize=35)
plt.show()


# Function that calculates trustworthiness of UMAP
def trustworthiness(reshaped_HLB_p5, HLB_p5_data_reduced, n_neighbors=15):
    # Calculate the nearest neighbors in the high-dimensional space
    knn_true = NearestNeighbors(n_neighbors=n_neighbors).fit(reshaped_HLB_p5)
    true_distances, true_indices = knn_true.kneighbors(reshaped_HLB_p5)

    # Calculate the nearest neighbors in the UMAP embedding
    knn_embedded = NearestNeighbors(n_neighbors=n_neighbors).fit(HLB_p5_data_reduced)
    embedded_distances, embedded_indices = knn_embedded.kneighbors(HLB_p5_data_reduced)

    # Calculate the trustworthiness as the average of the ratio of distances in the original space and UMAP space
    trust = 0
    for i in range(len(reshaped_HLB_p5)):
        trust += np.sum(np.isin(true_indices[i], embedded_indices[i])) / n_neighbors
    trust /= len(reshaped_HLB_p5)

    return print("Trustworthiness: ", trust)
trustworthiness(reshaped_HLB_p5, HLB_p5_umap, n_neighbors=15)
# For trustworthiness, a score closer to 1 indicates that the UMAP is preserving the local distances well.
# However, a score close to 1 doesn't necessarily mean that the UMAP is a good representation of the data.


# Calculate pairwise distances in the high-dimensional and low-dimensional spaces
high_d_distances = squareform(pdist(reshaped_HLB_p5, 'euclidean'))
low_d_distances = np.linalg.norm(HLB_p5_umap[:, np.newaxis] - HLB_p5_umap, axis=-1)

# Calculate the continuity value
continuity = np.corrcoef(high_d_distances.flatten(), low_d_distances.flatten())[0, 1]
print(f"Continuity: {continuity:.2f}")

# A value of continuity close to 1 indicates a good preservation of the relationships between nearby data points in
# the reduced dimensional space, while a value closer to 0 indicates that the relationships may have been lost or
# distorted.
# However, a value of continuity close to 1 may not always be desired as it may result in over-representation of
# some data points and under-representation of others.
