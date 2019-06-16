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
k_km = 5
k_knn = 15
guides_latent = np.load('preprocessing/guides_latent.npy').transpose()
clusters = Kmeans(guides_latent, k_km)
predicts, k_nearest = KNN(query, guides_latent, k_knn, clusters)
k_nearest = k_nearest.numpy()

# guide_file_dict[(name, address)] = file_name
guide_file_dict = {}
for i in os.listdir('data/reviews_guide'):
	guide_file_dict[i.split()[2].split('=')[1].split('.')[0]] = i

# guides[number] = guide ID
with open('preprocessing/guides.txt', encoding='utf-8') as f:
	guides = f.readlines()
for n in range(len(guides)):
	guides[n] = guides[n][:-1]

# place_dict[place] = number of reviews in k_nearest
place_dict = {}
for i in k_nearest:
	with open(os.path.join('data/reviews_guide', guide_file_dict[guides[i]]), encoding='utf-8') as f:
		data = json.load(f)
	for review in data:
		place = (review['place'], review['address'])
		if place not in place_dict:
			place_dict[place] = 1
		else:
			place_dict[place] += 1

# collect places and sort
thresh = 3
place_list = [place for place in place_dict.items() if place[1]>thresh]
place_list.sort(key=lambda d: d[1], reverse = True)

for place in place_list:
	print(place[1], place[0])