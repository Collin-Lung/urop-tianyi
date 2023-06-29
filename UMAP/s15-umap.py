import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap

sns.set(style='white', context='notebook', rc={'figure.figsize': (14, 10)})

#Opening and cleaning data
with open("/Users/colli/OneDrive - Massachusetts Institute of Technology/IAP 2023/Dimensionality Reduction/PCA/s15.txt") as s15:
    string_s15 = ''.join(s15)
    new_s15 = string_s15.strip("[]")
    no_comma_s15 = new_s15.replace(',', '')
    no_bracket_s15 = no_comma_s15.replace("[", '')
    clean_s15 = no_bracket_s15.replace("]", '')
    final_s15 = clean_s15.split()

#Replacing monomer type with respective HBL values
HBL_s15 = []
for monomer in final_s15:
    if monomer == '1':
        HBL_s15.append(monomer.replace('1', '8.45'))
    elif monomer == '2':
        HBL_s15.append(monomer.replace('2', '11.4'))
    elif monomer == '3':
        HBL_s15.append(monomer.replace('3', '5.12'))
    elif monomer == '4':
        HBL_s15.append(monomer.replace('4', '18.5'))

#Initialize the UMAP model
reducer = umap.UMAP()

#Fit and transform the data
x = np.reshape(HBL_s15, (100, 11976)).T
df = pd.DataFrame(x)
embedding = reducer.fit_transform(df)

#Creating a scatter plot of the reduced data
plt.scatter(embedding[:, 0], embedding[:, 1])
plt.title("s15 UMAP Scatter Plot")
plt.xlabel("UMAP Dimension 1")
plt.ylabel("UMAP Dimension 2")

plt.show()