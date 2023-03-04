import matplotlib.pyplot as plt
import numpy as np

dataset= np.loadtxt('equilibration_time_dataset.txt').T
plt.hist(dataset, bins=50)
plt.show()