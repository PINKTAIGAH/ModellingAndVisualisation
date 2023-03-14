import matplotlib.pyplot as plt
import numpy as np

def function(x, mean):
    return()*()


dataset= np.loadtxt('equilibration_time_dataset.txt').T
plt.hist(dataset[dataset<4000], bins=50)
plt.xlabel('Equilibration time, t$_{eq}$ (a.u)')
plt.ylabel('Frequnecy (counts)')
plt.title('Equilibration time of random 50 x 50 lattice')
plt.show()