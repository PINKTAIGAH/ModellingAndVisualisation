import numpy as np

a= np.linspace(0,100,100).reshape(10,10)
print(a)
for i, val in np.ndenumerate(a):
    print(i, val)


    

