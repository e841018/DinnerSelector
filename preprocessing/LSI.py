import numpy as np
import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class LatentConverter():

	def __init__(self, places_path):
		place_list = []
		with open(places_path, encoding='utf-8') as f:
			for place in f:
				place_list.append(tuple(place[:-1].split(',')))
		self.places_path = places_path
		self.place_list = place_list
		self.place_set = set(place_list)
		self.place_len = len(place_list)

	def get_normalized(self, reviewer_path):
		with open(reviewer_path, encoding='utf-8') as f:
			review_list = json.load(f)

		stars_dict = {}
		for review in review_list:
			place = (review['place'], review['address'])
			if place in self.place_set:
				stars_dict[place] = review['stars']
		if len(stars_dict)==0:
			print('Reviewer "' + reviewer_path + '":\n\tNone of the reviews overlaps with "' + self.places_path + '"')
			mean, std = 0, 0
		else:
			stars_list = list(stars_dict.values())
			mean, std = np.mean(stars_list), np.std(stars_list)

		normalized = np.zeros(self.place_len)
		for p_idx, place in enumerate(self.place_list):
			if std==0:
				normalized[p_idx] = 0
			else:
				normalized[p_idx] = (stars_dict[place]-mean)/std if place in stars_dict else 0

		return normalized

	def gen_proj(self, guides_normalized, latent_dim=20):
		u, s, vh = np.linalg.svd(guides_normalized)
		print('gen_proj: The first', latent_dim, 'latent dimensions are taken.')
		print('Singular values:\n', s)
		# guides_smoothed = np.matmul(np.matmul(u[:,:20], np.diag(s[:20])), vh[:20,:])
		# print('Smoothed:\n', guides_smoothed)
		# # for debug use
		# guides_normalized = guides_normalized.transpose()
		# guides_smoothed = guides_smoothed.transpose()
		return u[:,:latent_dim].transpose()

	def get_latent(self, proj, reviewer_path):
		return np.matmul(proj, self.get_normalized(reviewer_path))
	
	@staticmethod
	def visualize(guides_latent, dims=(0,1,2)):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		X = guides_latent[dims[0],:]
		Y = guides_latent[dims[1],:]
		Z = guides_latent[dims[2],:]
		ax.scatter(X, Y, Z)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		plt.show()

class ReviewReader():

	def __init__(self, guides_path, reviews_path):
		self.reviews_path = reviews_path
		# guide_list[<number>] = <guide ID>
		guide_list = []
		with open(guides_path, encoding='utf-8') as f:
			for i in f:
				guide_list.append(i[:-1])
		self.guide_len = len(guide_list)
		# guide_file_dict[<guide ID>] = <file name>
		guide_file_dict = {}
		for i in os.listdir(reviews_path):
			guide_file_dict[i.split()[2].split('=')[1].split('.')[0]] = i
		# file_mame[<number>] = <file name>
		file_mame = []
		for num in range(len(guide_list)):
			file_mame.append(guide_file_dict[guide_list[num]])
		self.file_name = file_mame

	def getPath(self, guideNum):
		return os.path.join(self.reviews_path, self.file_name[guideNum])

	def getReviews(self, guideNum):
		with open(self.getPath(guideNum), encoding='utf-8') as f:
			review_list = json.load(f)
		return review_list
		

if __name__ == '__main__':

	# initialize with a list of places
	lc = LatentConverter('places.txt')
	# get reviews
	rr = ReviewReader('guides.txt', '../data/reviews_guide')
	# generate all normalized vectors
	guides_normalized = np.zeros((lc.place_len, rr.guide_len))
	for g_idx in range(rr.guide_len):
		guides_normalized[:,g_idx] = lc.get_normalized(rr.getPath(g_idx))
	# generate projection matrix
	proj = lc.gen_proj(guides_normalized, latent_dim=20)
	# project guides
	guides_latent = np.matmul(proj, guides_normalized)
	# save for future use
	np.save('proj.npy', proj)
	np.save('guides_latent.npy', guides_latent)

def example_get_latent():
	# initialize with a list of places
	lc = LatentConverter('places.txt')
	# load projection matrix
	proj = np.load('proj.npy')
	# get latent vector
	return lc.get_latent(proj, '../data/reviews_guide/reviews_guide length=117 guideID=107297262039687837164.json')

def example_visualize():
	# visualize the 0th, 1st, and 2nd latent dimension
	LatentConverter.visualize(np.load('guides_latent.npy'), dims=(0,1,2))
	