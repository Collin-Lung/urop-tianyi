import numpy as np
import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
from sklearn.decomposition import PCA
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

# Perform K-medoids clustering with varying number of medoids
k_values = range(2, 21)  # Range of k values to test
loss_values = []  # Store loss values for each k

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

for k in k_values:
    kmedoids = KMedoids(n_clusters=k)
    kmedoids.fit(p5_pca)
    labels = kmedoids.labels_
    medoids = kmedoids.medoid_indices_
    loss = k_medoids_loss(p5_pca, medoids, labels)
    loss_values.append(loss)

# Create the line graph
plt.plot(k_values, np.log(loss_values), marker='o', linestyle='-', color='blue')
plt.xlabel("Number of Medoids", fontsize=16)
plt.ylabel("Loss", fontsize=16)
plt.title('Loss vs Number of Medoids', fontsize=23)
plt.show()