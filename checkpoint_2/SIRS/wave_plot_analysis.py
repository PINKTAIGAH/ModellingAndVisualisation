import matplotlib.pyplot as plt
import numpy as np

def one():
    total_energy_resampled_data= []
    for i in range(len(data)):
        temp_resampled_data= []
        for j in range(k):
            bootstrap_resample= np.random.choice(data[i][0][:], size= n)
            temp_resampled_data.append(bootstrap_resample)
        total_energy_resampled_data.append(temp_resampled_data)
    return np.array(total_energy_resampled_data)


def find_resampled_variance(data, n=10000, k=10000):
    total_resampled_data= []
    for i in range(data.shape[0]):
        infected_resampled_data= []
        for j in range(k):
            bootstrap_resample= np.random.choice(data[i][:], size=n)
            infected_resampled_data.append(bootstrap_resample)
        total_resampled_data.append(infected_resampled_data)
    return np.array(total_resampled_data)





data= np.loadtxt('Data/wave_contour_data.txt').T
resample_data= find_resampled_variance(data)
data_reduced= [data[i].var()/2500 for i in range(data.shape[0])] 
plt.plot(np.arange(0.2,0.51,0.01), data_reduced)
plt.title('Infection fraction varience vs Infection probability')
plt.xlabel('Infection probabiolity, p$_1$')
plt.ylabel('Variance of infection fraction')
plt.show()