import matplotlib.pyplot as plt
import numpy as np

data= np.loadtxt('Data/wave_contour_data.txt').T
data_reduced= [data[i].var()/2500 for i in range(data.shape[0])] 
plt.plot(np.arange(0.2,0.51,0.01), data_reduced)
plt.show()