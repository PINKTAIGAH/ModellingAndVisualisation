import numpy as np
import matplotlib.pyplot as plt

lattice= np.zeros((50,50))
lattice[10][10]= 1
lattice[10][11]= 1
lattice[10][12]= 1

np.savetxt('empty_blinker_lattice.txt', lattice)
plt.imshow(lattice)
plt.show()