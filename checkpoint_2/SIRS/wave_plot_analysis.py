import matplotlib.pyplot as plt
import numpy as np

def generate_resampled_var(data, n=1000):
    resampled_dataset= np.random.choice(data, size=n)
    var= resampled_dataset.var()/2500
    return var

def find_indiv_error(data):
    data= np.array(data)
    return np.std(data)/np.sqrt(data.size)


def find_resampled_variance(data, n=1000, k=10000):
    variance_errors= []
    for i in range(data.shape[0]):
        bootstrapped_var= []
        for j in range(k):
            bootstrapped_var.append(generate_resampled_var(data[i][:]))
        variance_errors.append(find_indiv_error(bootstrapped_var))    
    return variance_errors

data= np.loadtxt('Data/wave_contour_data.txt').T
errors= find_resampled_variance(data)
print(errors)
data_reduced= np.var(data, axis= 1)/2500
plt.errorbar(np.arange(0.2,0.51,0.01), data_reduced, yerr= errors)
plt.title('Infection fraction varience vs Infection probability')
plt.xlabel('Infection probabiolity, p$_1$')
plt.ylabel(r'Variance of infection fraction, $\frac{<I^2>-<I>^2}{N}$')
plt.show()