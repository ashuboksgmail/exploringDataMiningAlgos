# -*- coding: utf-8 -*-
"""KMeans2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cYnodg8mo5LmtAZk7xAUA34qU2uWFNsw
"""



#mounting google driv
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#change directory 
# %cd /content/drive/MyDrive/DMV

#import necessary libraries
import numpy as np
import csv
import matplotlib.pyplot as plt

#read data from csv, 
#store data in numpy array called data
#skip the comlun name of data
data = np.genfromtxt('Household_Wealth.csv', delimiter=',', skip_header=1)

#calculate mean and standard deviation 
#z-score normalization
#store the data in new array scaled_data
mean = np.mean(data, axis=0)
std = np.std(data, axis=0)
scaled_data = (data - mean) / std

def k_means(data, k):
    # Initialize the centroids randomly
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    
    # Loop until convergence
    for i in range(100):
        # Assign each data point to the closest centroid
        distances = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        pred_y = np.argmin(distances, axis=0)
        
        # Update the centroids to the mean of the assigned data points
        for j in range(k):
            centroids[j] = np.mean(data[pred_y == j], axis=0)
        
        # Compute the within-cluster sum of squares
        wcss = np.sum((data - centroids[pred_y])**2)
        
        # Stop if the within-cluster sum of squares does not change much
        if i > 0 and np.abs(wcss - prev_wcss) < 1e-5:
            break
        
        prev_wcss = wcss
        
    return centroids, pred_y

#define function for dunn index 
def dunn_index(data, pred_y):
    # Calculate the distance between each pair of clusters
    cluster_distances = np.zeros((len(np.unique(pred_y)), len(np.unique(pred_y))))
    for i, i_cluster in enumerate(np.unique(pred_y)):
        for j, j_cluster in enumerate(np.unique(pred_y)):
            if i != j:
                i_indices = np.where(pred_y == i_cluster)[0]
                j_indices = np.where(pred_y == j_cluster)[0]
                cluster_distances[i, j] = np.sqrt(((data[i_indices][:, np.newaxis, :] - data[j_indices][np.newaxis, :, :])**2).sum())

    # Calculate the minimum distance between pairs of clusters
    min_cluster_distances = np.min(cluster_distances[np.nonzero(cluster_distances)])

    # Calculate the maximum distance within clusters
    max_intra_cluster_distance = np.max([np.sqrt(((data[np.where(pred_y == cluster_index)] - np.mean(data[np.where(pred_y == cluster_index)], axis=0))**2).sum(axis=1)).max() for cluster_index in np.unique(pred_y)])

    return min_cluster_distances / max_intra_cluster_distance

#define function for inertia
def inertia(data, pred_y, centroids):
    squared_distances = np.zeros(len(data))
    for i in range(len(data)):
        centroid_index = pred_y[i]
        distance = np.linalg.norm(data[i] - centroids[centroid_index])
        squared_distances[i] = distance ** 2
    return np.sum(squared_distances)

#loop k values from 2 to 10
for k in range(2, 11):
    #clustering using the K-mean function
    centroids, pred_y = k_means(scaled_data, k)
   
    #calculate dunn index
    dunn = dunn_index(scaled_data, pred_y)

    # Calculate the inertia
    inertia_val = inertia(scaled_data, pred_y, centroids)


    #print dunn index and inertia
    print(f"K = {k}, Dunn index: {dunn:.4f}, Inertia: {inertia_val:.4f}")