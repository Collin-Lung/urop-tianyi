import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# Opening and cleaning the data
with open('C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 UROP Tianyi/'
          'Dimensionality Reduction/PCA/p5-with-block-copolymers.txt') as p5:
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
x = np.reshape(HLB_p5, (100, 9240)).T
df = pd.DataFrame(x)

# Initialize the PCA model
pca = PCA(n_components=100)
p5_pca = pca.fit_transform(df)

# Explained variance ratio
per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)

# Calculate participation ratio of each principal component
total_var = np.sum(pca.explained_variance_)
part_ratio = [((i/total_var)**2)/(len(pca.components_)) for i in pca.explained_variance_]

# Creating a scatter plot of the reduced data
plt.figure(figsize=(8, 6))

# Labeling sequences in the scatter plot
seq1_indices_to_label = [seq for seq in range(9217, 9241)]

for index, txt in enumerate(p5_pca):
    if index in seq1_indices_to_label:
        plt.scatter(p5_pca[index, 0], p5_pca[index, 1], alpha=0.50, s=10, c='red', label='Labeled')
        plt.annotate(f"{index}", (p5_pca[index, 0], p5_pca[index, 1]))
    else:
        plt.scatter(p5_pca[index, 0], p5_pca[index, 1], alpha=0.20, s=10, c='blue', label='Unlabeled')

plt.title('HLB p5 PCA', fontsize=25)
plt.xlabel("PC1 - {0}%".format(per_var[0]), fontsize=18)
plt.ylabel("PC2 - {0}%".format(per_var[1]), fontsize=18)
plt.show()
