import numpy as np
import json
from preprocessing.LSI import LatentConverter, ReviewReader
from utils.Clustering import Kmeans, KNN
from utils.Filtering import *

# initialize with a list of places
lc = LatentConverter('preprocessing/places.json')

# load projection matrix
proj = np.load('preprocessing/proj.npy')

# get latent vector of the query
query_name = 'MVNLab'
# query_name = 'huzixiao'
query = lc.get_latent(proj, query_name+'.json')

# # visualize the first 3 dimensions of place vectors in latent space
# LatentConverter.visualize(np.load('preprocessing/proj.npy'), dims=(0,1,2))

# get the nearest guides to the query
k_km = 1
k_knn = 30
guides_latent = np.load('preprocessing/guides_latent.npy').transpose()
clusters = Kmeans(guides_latent, k_km)
predicts, k_nearest = KNN(query, guides_latent, k_knn, clusters)
k_nearest = k_nearest.numpy()

# get reviews and count
guides_normalized = np.load('preprocessing/guides_normalized.npy')
rr = ReviewReader('preprocessing/guides.txt', 'data/reviews_guide')
place_dict = {}
for gNum in k_nearest:
	for review in rr.getReviews(gNum):
		place = (review['place'], review['address'])
		if place not in lc.place2idx:
			continue
		score = guides_normalized[lc.place2idx[place],gNum]
		if place not in place_dict:
			place_dict[place] = [score,1]
		else:
			place_dict[place][0] += score
			place_dict[place][1] += 1

# collect places and rank for the first time
def key1(i):
	review_count = i[1][1]
	average = i[1][0]/i[1][1]
	return 0.1*review_count+average
place_list = sorted(place_dict.items(), key=key1, reverse=True)
print('idx\taverage\tcount\tscore\tplace')
for i in place_list[:50]:
	place = i[0]
	review_count = i[1][1]
	average = i[1][0]/i[1][1]
	score = 0.1*review_count+average
	place_idx = lc.place2idx[i[0]]
	print(str(place_idx) +'\t'+str(average)[:4] +'\t'+str(0.1*review_count)[:3] +'\t'+str(score)[:4] +'\t'+str(place))

corpus_path = 'data/place_dict.json'
reviewContent_path = 'data/review_list.json'
querys = ['冷氣','涼']
coupus, review_list, places = Load_All_Info(json_path=corpus_path, pickle_path=reviewContent_path)
scoreboard = FilteringAndRanking(querys=querys, places=places, corpus=coupus, review_list=review_list)


candidates = []
with open(query_name+'.txt', encoding='utf-8') as f:
	for line in f.readlines()[1:]:
		line = line.split()
		c = {}
		c['idx'] = int(line[0])
		c['average'] = float(line[1])
		c['count'] = float(line[2])
		c['name'] = lc.place_list[c['idx']][0]
		c['score_keyword'] = scoreboard[c['name']] if c['name'] in scoreboard else 0
		candidates.append(c)

def key2(c):
	return c['average']+0.1*c['count']+c['score_keyword']
candidates.sort(key=key2, reverse=True)

''