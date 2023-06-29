import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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


sublists = [HLB_p5[i:i+100] for i in range(0, len(HLB_p5), 100)]

# Sliding window operation on all sequences
sw_sublists = []
window_size = 5
for sublist in sublists:
    sw_sublist = []
    for i in range(0, 100 - window_size + 1):
        sw_seq = (np.float(sublist[i]) + np.float(sublist[i+1]) + np.float(sublist[i+2])
                  + np.float(sublist[i+3]) + np.float(sublist[i+4])) / 5
        sw_sublist.append(sw_seq)
    sw_sublists.append(sw_sublist)

pca = PCA(n_components=2)
pca.fit(np.array(sublists).T)

# Extract the explained variance ratio for the first and second principal components
per_var = np.round(pca.explained_variance_ratio_, decimals=2)
first_var = per_var[0]
second_var = per_var[1]

# Create a scatter plot of the PCA components
plt.scatter(pca.components_[0], pca.components_[1], s=10.0, alpha=0.2)
plt.title(f'HLB p5 PCA SW (Window Size = {window_size})', fontsize=23)
plt.xlabel('PC1 - {0}%'.format(first_var*100), fontsize=13)
plt.ylabel('PC2 - {0}%'.format(second_var*100), fontsize=13)
plt.show()
