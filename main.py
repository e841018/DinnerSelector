import numpy as np
from preprocessing.LSI import LatentConverter
from utils.Clustering import Kmeans

# # initialize with a list of places
# lc = LatentConverter('preprocessing/places.txt')
# # visualize the 0th, 1st, and 5th latent dimension
# lc.visualize(np.load('preprocessing/guides_latent.npy'), dims=(0,1,2))

# # initialize with a list of places
# lc = LatentConverter('preprocessing/places.txt')
# # load projection matrix
# proj = np.load('preprocessing/proj.npy')
# # get latent vector
# print(lc.get_latent(proj, 'data/reviews_guide/reviews_guide length=117 guideID=107297262039687837164.json'))

# guides_latent = np.load('preprocessing/guides_latent.npy').transpose()[:,:2]
# predict = Kmeans(guides_latent, k=5)