import numpy as np
import matplotlib.pyplot as plt

data= np.loadtxt('Data/immunity_data.txt').T
plotter= np.average(data, axis= 1)/2500
plt.scatter(np.arange(0, 1, 0.05), plotter, marker='x')
plt.title('Average infection fraction vs immunity fraction')
plt.xlabel('Immunity fraction, f$_{im}$')
plt.ylabel(r'Average infection fraction, $\frac{<I>}{N}$')
plt.show()