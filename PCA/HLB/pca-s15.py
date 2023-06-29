import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Opening and cleaning the data
with open('C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 UROP Tianyi/'
          'Dimensionality Reduction/PCA/s15.txt.txt') as s15:
    string_s15 = ''.join(s15)
    new_s15 = string_s15.strip("[]")
    no_comma_s15 = new_s15.replace(',', '')
    no_bracket_s15 = no_comma_s15.replace("[", '')
    clean_s15 = no_bracket_s15.replace("]", '')
    final_s15 = clean_s15.split()

#Replacing monomer type with respective HBL values
HLB_s15 = []
for monomer in final_s15:
    if monomer == '1':
        HLB_s15.append(monomer.replace('1', '8.45'))
    elif monomer == '2':
        HLB_s15.append(monomer.replace('2', '11.4'))
    elif monomer == '3':
        HLB_s15.append(monomer.replace('3', '5.12'))
    elif monomer == '4':
        HLB_s15.append(monomer.replace('4', '18.5'))

# numerical_s15 = [eval(monomer) for monomer in final_s15]

#Fit and transform the data
x = np.reshape(HLB_s15, (100, 11976)).T
df = pd.DataFrame(x)

#Initialize the PCA model
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(df)
s15_pca = pca.transform(df)

#Explained variance ratio
per_var = np.round(pca.explained_variance_ratio_* 100, decimals = 1)

#Creating a scatter plot of the reduced data
plt.figure(figsize=(8, 6))
plt.scatter(s15_pca[:, 0], s15_pca[:, 1], alpha=0.20, s=10)
plt.title('s15 PCA', fontsize=25)
plt.xlabel('PC1 - {0}%'.format(per_var[0]), fontsize=18)
plt.ylabel('PC2 - {0}%'.format(per_var[1]), fontsize=18)

plt.show()