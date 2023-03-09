import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt


data= []
for i in sorted(os.listdir(f'Data'))[:-1]:
    file_name= f'Data/{i}'
    indv_data= np.loadtxt(file_name).T
    indv_data_averages= np.average(indv_data, axis=1)
    data.append(indv_data_averages)

data= np.array(data)
plt.imshow(data)
plt.show()
