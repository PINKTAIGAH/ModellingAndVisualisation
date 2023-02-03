import os
import numpy as np
import matplotlib.pyplot as plt

data= []
for i in os.listdir('data'):
    data.append(np.loadtxt(str('data/'+i), delimiter= ',').T)

temperature= np.arange(1, 3.2, 0.1)
energy= []
magnetisation= []

for i in range(len(data)):
    energy.append(np.average(data[i][0][:]))
    magnetisation.append(np.average(np.absolute(data[i][1][:])))


fig, (ax1, ax2)= plt.subplots(2, 1, sharex= True)
ax1.plot(temperature, np.array(energy))
ax2.plot(temperature, np.array(magnetisation))
plt.show()