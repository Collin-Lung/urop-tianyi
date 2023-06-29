import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Opening and cleaning the data
with open('C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 UROP Tianyi/'
          'Dimensionality Reduction/PCA/p5.txt') as p5:
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
pca = PCA(n_components=3)  # Set n_components to 3 for 3D plotting
p5_pca = pca.fit_transform(df)

# Creating a 3D scatter plot of the reduced data
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(p5_pca[:, 0], p5_pca[:, 1], p5_pca[:, 2], alpha=0.20, s=10)

# Set labels and title
ax.set_title('p5 PCA', fontsize=25)
ax.set_xlabel("PC1 - {0}%".format(round(pca.explained_variance_ratio_[0]*100, 2)), fontsize=18)
ax.set_ylabel("PC2 - {0}%".format(round(pca.explained_variance_ratio_[1]*100, 2)), fontsize=18)
ax.set_zlabel("PC3 - {0}%".format(round(pca.explained_variance_ratio_[2]*100, 2)), fontsize=18)

plt.show()