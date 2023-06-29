import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap

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
        HLB_p5.append(8.45)
    elif monomer == '2':
        HLB_p5.append(11.4)
    elif monomer == '3':
        HLB_p5.append(5.12)
    elif monomer == '4':
        HLB_p5.append(18.5)

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


# Initialize the UMAP model
n_components = 2
reducer = umap.UMAP(n_components=n_components)

# Transform the data using the UMAP model
HLB_p5_umap = reducer.fit_transform(np.array(sublists).T)

# Creating a scatter plot of the reduced data
plt.scatter(HLB_p5_umap[:, 0], HLB_p5_umap[:, 1])
plt.title(f"p5 UMAP Scatter Plot with Sliding Window Analysis (Window Size = {window_size})")
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.show()
