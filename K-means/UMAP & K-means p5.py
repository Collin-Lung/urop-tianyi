import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap
from sklearn.cluster import KMeans

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

# Select num of clusters
n_clusters = 3

# Initialize and fit the K-means model to the transformed data
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(HLB_p5_umap)

# Predict the cluster labels for each data point
labels = kmeans.predict(HLB_p5_umap)
centroids = kmeans.cluster_centers_

# Creating a scatter plot of the reduced data
plt.scatter(HLB_p5_umap[:, 0], HLB_p5_umap[:, 1], c=labels)
plt.title("p5 UMAP Scatter Plot")
plt.xlabel("UMAP Dimension 1")
plt.ylabel("UMAP Dimension 2")
plt.show()