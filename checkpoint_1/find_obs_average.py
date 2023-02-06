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


temperature= np.arange(1, 3.1, 0.1)


energy= []
magnetisation= []
succeptibility= []
heat_capacity= []

for i in range(len(data)):
    energy.append(np.average(data[i][0][:]))
    magnetisation.append(np.average(np.absolute(data[i][1][:])))
    succeptibility.append((np.average(np.absolute(data[i][1][:])**2) - np.average(np.absolute(data[i][1][:]))**2)/(2500*temperature[i]))
    heat_capacity.append((np.average(np.absolute(data[i][0][:])**2) - np.average(np.absolute(data[i][0][:]))**2)/(2500*temperature[i]))

header= str('temperature, avr_energy, avr_magnetisation, heat_capacity, succeptibility')
output= np.array([temperature, energy, magnetisation, heat_capacity, succeptibility]).T
np.savetxt(f'{flag}_obvs_data.txt', output, delimiter= ',', header= header)


