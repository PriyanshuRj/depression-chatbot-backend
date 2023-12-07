import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import pickle
import os

CLASSES_PATH = os.path.join('labels_das.pkl')
classes = pickle.load(open(CLASSES_PATH,'rb'))

file_path = 'confusion_matrix.txt'

# Read the file and convert each line to a list of integers
with open(file_path, 'r') as file:
    lines = file.readlines()

# Convert each line to a list of integers
matrix = [list(map(int, line.strip().split())) for line in lines]

# Now 'matrix' is a list of lists of integers
print(len(matrix[0]))
print(len(classes[:129]))
cfm = matrix
classes = classes[:129]

df_cfm = pd.DataFrame(cfm, index = classes, columns = classes)
plt.figure(figsize = (32,32))
cfm_plot = sn.heatmap(df_cfm, annot=True)
cfm_plot.figure.savefig("cfm.png")