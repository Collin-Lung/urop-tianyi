import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
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


# Select num of clusters
n_clusters = 5

# Initialize and fit the K-means model to the transformed data
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(p5_pca)

# Predict the cluster labels for each data point
labels = kmeans.predict(p5_pca)
centroids = kmeans.cluster_centers_

def kmeans_loss(X, centroids, labels):
    n = X.shape[0]
    k = centroids.shape[0]
    loss = 0
    for i in range(n):
        for j in range(k):
            if labels[i] == j:
                loss += np.linalg.norm(X[i] - centroids[j])
    return loss

# Scatter plot
plt.scatter(p5_pca[:, 0], p5_pca[:, 1], c=labels)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('K-means clustering with PCA')
# for i in range(n_clusters):
#     plt.scatter(centroids[i, 0], centroids[i, 1], marker="o", color='black')
plt.show()

# Calculate the loss of the K-means model
loss = kmeans_loss(p5_pca, centroids, labels)
print('K-means loss:', loss)