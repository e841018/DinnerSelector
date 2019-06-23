import numpy as np
import json
from preprocessing.LSI import LatentConverter, ReviewReader
from utils.Clustering import Kmeans, KNN, distance_Cos

# initialize with a list of places
lc = LatentConverter('preprocessing/places.json')

# load projection matrix
proj = np.load('preprocessing/proj.npy')

# get latent vector of the query
query = lc.get_latent(proj, 'huzixiao.json')
# query = lc.get_latent(proj, 'MVNLab.json')

# get the nearest guides to the query
k_knn = 30
places_latent = np.load('preprocessing/proj.npy').transpose()
predicts, k_nearest = KNN(query, places_latent, k_knn, distance=distance_Cos)
k_nearest = k_nearest.numpy()

# get reviews and count
rr = ReviewReader('preprocessing/guides.txt', 'data/reviews_guide')
place_dict = {}
for num in k_nearest:
	print(lc.place_list[num])