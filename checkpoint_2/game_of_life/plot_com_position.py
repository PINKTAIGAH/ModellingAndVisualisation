import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

data= np.loadtxt('com_dataset.txt').T
time= np.arange(0, data.size, 1)
res= stats.linregress(time, data)
print(f'The velocity of the glider is {res.slope:.2} +/- {res.stderr:.2} a.u')
plt.plot(time, data)
plt.xlabel('time, t (s)')
plt.ylabel('Center of Mass Position, x$_{COM}$ (a.u)')
plt.title('Center of mass position vs time')
plt.show()