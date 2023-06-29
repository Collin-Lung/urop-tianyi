from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt
import numpy as np

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
HBL_p5 = []
for monomer in final_p5:
    if monomer == '1':
        HBL_p5.append(monomer.replace('1', '8.45'))
    elif monomer == '2':
        HBL_p5.append(monomer.replace('2', '11.4'))
    elif monomer == '3':
        HBL_p5.append(monomer.replace('3', '5.12'))
    elif monomer == '4':
        HBL_p5.append(monomer.replace('4', '18.5'))

# Fit and transform the data
reshaped_HBL_p5 = np.reshape(HBL_p5, (100, 9216)).T

# Perform ICA
ica = FastICA(n_components=2)
components = ica.fit_transform(reshaped_HBL_p5)

# Create scatter plot of the first two independent components
plt.scatter(components[:, 0], components[:, 1])
plt.xlabel("Independent component 1")
plt.ylabel("Independent component 2")

plt.show()