import numpy as np
import json
from preprocessing.LSI import LatentConverter, ReviewReader
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
k_km = 1
k_knn = 20
guides_latent = np.load('preprocessing/guides_latent.npy').transpose()
clusters = Kmeans(guides_latent, k_km)
predicts, k_nearest = KNN(query, guides_latent, k_knn, clusters)
k_nearest = k_nearest.numpy()

# get reviews and count
rr = ReviewReader('preprocessing/guides.txt', 'data/reviews_guide')
place_dict = {}
for num in k_nearest:
	for review in rr.getReviews(num):
		place = (review['place'], review['address'])
		if place not in place_dict:
			place_dict[place] = 1
		else:
			place_dict[place] += 1

# collect places and sort
thresh = 4
place_list = [place for place in place_dict.items() if place[1]>thresh]
place_list.sort(key=lambda d: d[1], reverse = True)

for place in place_list:
	print(place[1], place[0])