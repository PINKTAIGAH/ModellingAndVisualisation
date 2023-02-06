import os
import sys
import matplotlib.pyplot as plt
import numpy as np

if str(sys.argv[1])== str('g'):
    flag= str('glauber')
elif str(sys.argv[1])== str('k'):
    flag= str('kawasaki')
else:
    print('Add correct flag to arguments')

data= np.loadtxt(str(f'{flag}_obvs_data.txt'), delimiter= ',').T

plt.scatter(data[0], data[1], marker= 'x')
plt.xlabel('Temperature, T (a.u.)')
plt.ylabel('Average energy, $\overline{E}$ (a.u.)')
plt.title(f'Average energy vs temperature for {flag} dynamics')
plt.xticks(np.arange(min(data[0]), max(data[0])+0.2, 0.2))
plt.savefig(f'figures/{flag}_energy.png')
plt.show()

plt.clf()

plt.scatter(data[0], data[2], marker= 'x')
plt.xlabel('Temperature, T (a.u.)')
plt.ylabel('Average magnetisation, $\overline{M}$ (a.u.)')
plt.title(f'Average magnetisation vs temperature for {flag} dynamics')
plt.xticks(np.arange(min(data[0]), max(data[0])+0.2, 0.2))
plt.savefig(f'figures/{flag}_magnetisation.png')
plt.show()

plt.clf()

plt.scatter(data[0], data[3], marker= 'x')
plt.xlabel('Temperature, T (a.u.)')
plt.ylabel('Specific heat capacity $C_v$ (a.u.)')
plt.title(f'Specific heat capacity vs temperature for {flag} dynamics')
plt.xticks(np.arange(min(data[0]), max(data[0])+0.2, 0.2))
plt.savefig(f'figures/{flag}_heat_capacity.png')
plt.show()

plt.clf()

plt.scatter(data[0], data[4], marker= 'x')
plt.xlabel('Temperature, T (a.u.)')
plt.ylabel('Succeptibility $\chi$ (a.u.)')
plt.title(f'Succeptibility vs temperature for {flag} dynamics')
plt.xticks(np.arange(min(data[0]), max(data[0])+0.2, 0.2))
plt.savefig(f'figures/{flag}_Succeptibility.png')
plt.show()