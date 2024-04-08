# -*- coding: utf-8 -*-
"""NN1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JqjmgporpQ2dQKZz7OA4FwqD3MmK4rDD
"""

#mounting google driv
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#change directory 
# %cd /content/drive/MyDrive/DMV

from sklearn.neural_network import MLPClassifier
import numpy as np

# Load training data
train_data = np.loadtxt("atriskstudentstrain.csv", delimiter=",", skiprows=1)
X_train = train_data[:, :-1]
y_train = train_data[:, -1]

# Define the model
model = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Load test data
test_data = np.loadtxt("atriskstudentstest.csv", delimiter=",", skiprows=1)
X_test = test_data[:, :-1]
y_test = test_data[:, -1]

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.3f}")