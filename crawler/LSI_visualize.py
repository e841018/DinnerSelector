import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dims = [3,4,5]

guides_latent = np.load('guides_latent.npy')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = guides_latent.shape[1]
xs = guides_latent[dims[0],:]
ys = guides_latent[dims[1],:]
zs = guides_latent[dims[2],:]
ax.scatter(xs, ys, zs, marker='^')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()