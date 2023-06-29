from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Opening and cleaning data
with open("C:/Users/colli/OneDrive - Massachusetts Institute of Technology/2022-2023 "
          "UROP Tianyi/Dimensionality Reduction/PCA/p5.txt") as p5:
    string_p5 = ''.join(p5)
    new_p5 = string_p5.strip("[]")
    no_comma_p5 = new_p5.replace(',', '')
    no_bracket_p5 = no_comma_p5.replace("[", '')
    clean_p5 = no_bracket_p5.replace("]", '')
    final_p5 = clean_p5.split()

#Replacing monomers with respective HBL values
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

# Perform t-SNE on the data
x = np.reshape(HLB_p5, (100, 9216)).T
df = pd.DataFrame(x)
tsne = TSNE(n_components=2)
p5_tsne = tsne.fit_transform(df)

#Creating the scatter plot
plt.scatter(p5_tsne[:,0], p5_tsne[:,1], alpha=0.25)
plt.title("t-SNE Scatter Plot")
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")

# Labeling sequences in the scatter plot
seq1_indices_to_label = [5394]
seq2_indices_to_label = [5519]

for index, txt in enumerate(p5_tsne):
    if index in seq1_indices_to_label:
        plt.annotate("seq3", (p5_tsne[index, 0], p5_tsne[index, 1]))

for index, txt in enumerate(p5_tsne):
    if index in seq2_indices_to_label:
        plt.annotate("seq15", (p5_tsne[index, 0], p5_tsne[index, 1]))

plt.show()
