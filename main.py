import numpy as np
import json
import os
from preprocessing.LSI import LatentConverter
from utils.Clustering import Kmeans, KNN

# initialize with a list of places
lc = LatentConverter('preprocessing/places.txt')

# load projection matrix
proj = np.load('preprocessing/proj.npy')

# get latent vector of the query
query = lc.get_latent(proj, 'reviews_guide_test.json')

# # visualize the first 3 dimensions of place vectors in latent space
# LatentConverter.visualize(np.load('preprocessing/proj.npy'), dims=(0,1,2))

# get the nearest guides to the query
guides_latent = np.load('preprocessing/guides_latent.npy').transpose()
clusters = Kmeans(guides_latent, 5)
predicts, k_nearest = KNN(query, guides_latent, 5, clusters)

# with open('preprocessing/places.txt', encoding = 'utf-8') as f:
#     places = f.readlines()

with open('preprocessing/guides.txt', encoding = 'utf-8') as f:
    guides = f.readlines()



for i in k_nearest:
    print(guides[i])

''