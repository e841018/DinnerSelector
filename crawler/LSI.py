import numpy as np
import json
import os
from os import listdir
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

data_path = '../data/reviews_guide'

guide_file_dict = {}
guide_file_list = listdir(data_path)
for i in guide_file_list:
	guide_file_dict[i.split()[2].split('=')[1].split('.')[0]] = i

guide_list = []
with open('guides.txt', encoding='utf-8') as f_guides:
	for i in f_guides:
		guide_list.append(i[:-1])

place_list = []
with open('places.txt', encoding='utf-8') as f_places:
	for i in f_places:
		place_list.append(tuple(i[:-1].split(',')))
place_set = set(place_list)

guides_normalized = np.zeros((len(place_list), len(guide_list)))
for g_idx, guide in enumerate(guide_list):
	guide_path = os.path.join(data_path, guide_file_dict[guide])
	with open(guide_path, encoding='utf-8') as f:
		review_list = json.load(f)
	
	stars_dict = {}
	for review in review_list:
		place = (review['place'], review['address'])
		if place in place_set:
			stars_dict[place] = review['stars']
	assert len(stars_dict)!=0
	stars_list = list(stars_dict.values())
	mean = np.mean(stars_list)
	std = np.std(stars_list)

	for p_idx, place in enumerate(place_list):
		if std==0:
			guides_normalized[p_idx][g_idx] = 0
		else:
			guides_normalized[p_idx][g_idx] = (stars_dict[place]-mean)/std if place in stars_dict else 0.0

u, s, vh = np.linalg.svd(guides_normalized)
latent_dimension = 20
proj = u[:,:latent_dimension].transpose()
guides_latent = np.matmul(proj, guides_normalized)

np.save('guides_normalized.npy', guides_normalized)
np.save('singular_values.npy', s)
np.save('proj.npy', proj)
np.save('guides_latent.npy', guides_latent)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = len(guide_list)
xs = guides_latent[0,:]
ys = guides_latent[1,:]
zs = guides_latent[2,:]
ax.scatter(xs, ys, zs, marker='^')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

'wait'




