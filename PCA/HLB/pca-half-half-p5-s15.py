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

# Loading s15 data
with open('C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 UROP Tianyi/'
          'Dimensionality Reduction/PCA/s15.txt') as s15:
    string_s15 = ''.join(s15)
    new_s15 = string_s15.strip("[]")
    no_comma_s15 = new_s15.replace(',', '')
    no_bracket_s15 = no_comma_s15.replace("[", '')
    clean_s15 = no_bracket_s15.replace("]", '')
    final_s15 = clean_s15.split()

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

# Take the first half of p5 data and the rest as s15
half_p5_s15 = HLB_p5[:460800] + HLB_s15[460800:921600]

# Fit and transform the data
x = np.reshape(half_p5_s15, (100, 9216)).T
df = pd.DataFrame(x)

# Initialize the PCA model
pca = PCA(n_components=100)
half_p5_s15_pca = pca.fit_transform(df)

# Explained variance ratio
per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)

# total_var = 0
# added_per_var = []
# for var in per_var:
#     total_var += var
#     added_per_var.append(total_var)
#
# # Plot the explained variance ratio
# num_line = [i+1 for i in range(len(per_var))]
# plt.plot(num_line, added_per_var, '-')
# plt.ylabel('Explained Variance Ratio (%)', fontsize=16)
# plt.xlabel('Summation of Principal Components', fontsize=16)
# plt.title('Explained Variance Ratio of Principal Components', fontsize=16)
# # plt.ylim([0, max(per_var)+90])
# plt.show()

# Calculate participation ratio of each principal component
total_var = np.sum(pca.explained_variance_)
part_ratio = [((i/total_var)**2)/(len(pca.components_)) for i in pca.explained_variance_]

# # Plot the participation ratio
# num_line = [i+1 for i in range(len(part_ratio))]
# plt.plot(num_line, part_ratio, '-o')
# plt.ylabel('Participation Ratio')
# plt.xlabel('Principal Component')
# plt.title('Participation Ratio of Principal Components')
# plt.ylim([0, .001])
# plt.show()

# Creating a scatter plot of the reduced data
plt.figure(figsize=(8, 6))
plt.scatter(half_p5_s15_pca[:, 0], half_p5_s15_pca[:, 1], alpha=0.20, s=10)
plt.title('Half p5, half s15 PCA', fontsize=25)
plt.xlabel("PC1", fontsize=18)
plt.ylabel("PC2", fontsize=18)
plt.xlabel('PC1 - {0}%'.format(per_var[0]), fontsize=18)
plt.ylabel('PC2 - {0}%'.format(per_var[1]), fontsize=18)

# # Labeling sequences in the scatter plot
# seq1_indices_to_label = [5394]
# seq2_indices_to_label = [5519]
#
# for index, txt in enumerate(p5_pca):
#     if index in seq1_indices_to_label:
#         plt.annotate("seq3", (p5_pca[index, 0], p5_pca[index, 1]))
#
# for index, txt in enumerate(p5_pca):
#     if index in seq2_indices_to_label:
#         plt.annotate("seq15", (p5_pca[index, 0], p5_pca[index, 1]))

plt.show()


