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
for i in os.listdir(f'raw_{flag}_data'):
    data.append(np.loadtxt(str(f'raw_{flag}_data/'+i), delimiter= ',').T)


temperature= np.arange(1, 3.2, 0.1)

'''
energy= []
magnetisation= []

for i in range(len(data)):
    energy.append(np.average(data[i][0][:]))
    magnetisation.append(np.average(np.absolute(data[i][1][:])))
'''

fig, (ax1, ax2)= plt.subplots(2, 1, sharex= True)
for i in range(len(data)):
    ax1.scatter(np.arange(0,len(data[i][0])), data[i][0][:])
    ax2.scatter(np.arange(0,len(data[i][0])), np.absolute(data[i][1][:]))
    ax1.set_title(str(temperature[i]))
    plt.show()


