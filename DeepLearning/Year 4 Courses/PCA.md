```py
#######################################################################
# PCA practical
#######################################################################

#######################################################################
# 0) Create a python virtual environment for python 3.7 or greater.
# Activate the virtual env and use pip to install the below import
# dependencies. Now you can run this script from the command line.
# The pdb.set_trace function will stop you at the appropriate lines.
# To exit the pdb debugger, type "q Enter". To continue, type "c Enter".
# For help with the debugger, type "? Enter".
#######################################################################

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.datasets import fetch_olivetti_faces
from sklearn.decomposition import PCA

images_path = os.getcwd()
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=400):
    path = os.path.join(images_path, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension)

def plot_faces(faces, labels, n_cols=5, plot_label=""):
    faces = faces.reshape(-1, 64, 64)
    n_rows = (len(faces) - 1) // n_cols + 1
    plt.figure(figsize=(n_cols, n_rows * 1.1))
    for index, (face, label) in enumerate(zip(faces, labels)):
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(face, cmap="gray")
        plt.axis("off")
        plt.title(label)
    save_fig(f"{plot_label}faces", fig_extension="png")

#######################################################################
# 1) Plot the first and last 25 faces using the function plot_faces
#######################################################################

olivetti = fetch_olivetti_faces()
first_faces = olivetti.data[:25]
last_faces = olivetti.data[-25:]
print(first_faces.shape)
# Your code goes here:
# import pdb;
# pdb.set_trace()
plot_faces(faces = first_faces,labels=range(25),plot_label='first')
plot_faces(faces = last_faces,labels=range(25),plot_label='last')


#######################################################################
# 2) Use the class PCA (imported above) to calculate the principal
# components for the olivetti dataset
#######################################################################

# Your code goes here:
import pdb; pdb.set_trace()


#######################################################################
# 3) Reconstruct the olivetti dataset using only the first 80 principal
# components, using PCA.inverse_transform
#######################################################################

# Your code goes here:
import pdb; pdb.set_trace()


#######################################################################
# 4) Plot the first and last 25 reconstructed faces using the function plot_faces
#######################################################################

# Your code goes here:
import pdb; pdb.set_trace()
```
