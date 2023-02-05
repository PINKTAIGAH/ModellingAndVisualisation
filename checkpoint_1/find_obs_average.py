import os
import numpy as np
import matplotlib.pyplot as plt
import sys

if str(sys.argv[1])== str('g'):
    flag= str('glauber')
elif str(sys.argv[1])== str('k'):
    flag= str('kawasaki')
else:
    print('Add correct flag to arguments')

data= []
for i in sorted(os.listdir(f'raw_{flag}_data')):
    data.append(np.loadtxt(str(f'raw_{flag}_data/'+i), delimiter= ',').T)
print(sorted(os.listdir(f'raw_{flag}_data')))

temperature= np.arange(1, 3.1, 0.1)


energy= []
magnetisation= []

for i in range(len(data)):
    energy.append(np.average(data[i][0][:]))
    magnetisation.append(np.average(np.absolute(data[i][1][:])))


fig, (ax1, ax2)= plt.subplots(2, 1, sharex= True)
ax1.scatter(temperature, energy)
ax2.scatter(temperature, magnetisation)
plt.show()



