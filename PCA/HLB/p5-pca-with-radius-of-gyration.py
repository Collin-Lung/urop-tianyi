import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

# numerical_p5 = list(map(float, HLB_p5))

# Fit and transform the data
x = np.reshape(HLB_p5, (100, 9216)).T
df = pd.DataFrame(x)

# Initialize the PCA model
pca = PCA(n_components=2)
pca.fit(df)
p5_pca = pca.transform(df)

# Explained variance ratio
per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)

# Load radius of gyration
radius_of_gyration = np.loadtxt("MMA_rgi_1.txt")

# Creating a scatter plot of the reduced data
plt.figure(figsize=(8, 6))
plt.scatter(p5_pca[:, 0], p5_pca[:, 1], c=radius_of_gyration)
#### Change to 20 sequences

plt.title('p5 PCA with Color Coded by Radius of Gyration')
plt.xlabel('First Principle Component - {0}%'.format(per_var[0]))
plt.ylabel('Second Principle Component - {0}%'.format(per_var[1]))
plt.colorbar()

plt.show()