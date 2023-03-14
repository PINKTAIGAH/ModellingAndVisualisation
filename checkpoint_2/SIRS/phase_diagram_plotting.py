import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt


data= []
for i in sorted(os.listdir(f'Data'))[:-2]:
    file_name= f'Data/{i}'
    indv_data= np.loadtxt(file_name)[99:].T
    indv_data_averages= np.average(indv_data, axis=1)/2500
    data.append(indv_data_averages)

data= np.flip(np.array(data).T, axis=0)
print(data.shape)
plt.imshow(data, extent=[0,1,0,1], cmap='magma')
plt.colorbar()
plt.xlabel('Infection probability, p$_1$')
plt.ylabel('Succeptibility probability, p$_3$')
plt.title('Recovery probability phase diagram')
plt.show()
