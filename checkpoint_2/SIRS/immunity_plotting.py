import numpy as np
import matplotlib.pyplot as plt

data= np.loadtxt('Data/immunity_data.txt').T
plotter= [np.average(data[i])/2500 for i in range(data.shape[0])]
plt.plot(np.arange(0, 1, 0.05), plotter)
plt.show()