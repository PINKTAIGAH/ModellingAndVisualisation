import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def retrieve_flag():
    #===================================================
    # Identify and return flag set by user
    if str(sys.argv[1])== str('g'):
        flag= str('glauber')
    elif str(sys.argv[1])== str('k'):
        flag= str('kawasaki')
    else:
        print('Add correct flag to arguments')
        sys.exit()
    return flag

def read_raw_data():
    #===================================================
    # Read and retrun raw data from txt files
    flag= retrieve_flag()
    data= []
    for i in sorted(os.listdir(f'raw_{flag}_data')):
        data.append(np.loadtxt(str(f'raw_{flag}_data/'+i), delimiter= ',').T)
    return data, flag

def calculate_obs(data):
    #===================================================
    # Calculate relevant observables from draw data
    energy= []
    magnetisation= []
    succeptibility= []
    heat_capacity= []
    temperature= np.arange(1, 3.1, 0.1)
    for i in range(len(data)):
        energy.append(np.average(data[i][0][:]))
        magnetisation.append(np.average(np.absolute(data[i][1][:])))
        succeptibility.append((np.average(np.absolute(data[i][1][:])**2)\
            - np.average(np.absolute(data[i][1][:]))**2)/(2500*temperature[i]))
        heat_capacity.append((np.average(np.absolute(data[i][0][:])**2)\
            - np.average(np.absolute(data[i][0][:]))**2)/(2500*temperature[i]**2))
    return temperature, energy, magnetisation, succeptibility, heat_capacity

def energy_resample(data):
    #===================================================
    # Generate 1000 resampled energy data sets @ each temp
    # via the bootstrap method    
    total_energy_resampled_data= []
    for i in range(len(data)):
        temp_resampled_data= []
        for j in range(k):
            bootstrap_resample= np.random.choice(data[i][0][:], size= n)
            temp_resampled_data.append(bootstrap_resample)
        total_energy_resampled_data.append(temp_resampled_data)
    return np.array(total_energy_resampled_data)

def find_energy_errors(resampled_energy, temperature):
    #===================================================
    # Find errors for heat capacity and energy errors
    energy_averages= []
    heat_capacity_averages= []
    print(resampled_energy.shape)
    for i in range(resampled_energy.shape[0]):
        energy_temp_averages= []
        for j in range(resampled_energy.shape[1]):
            energy_temp_averages.append(np.average(resampled_energy[i][j]))
        energy_averages.append(energy_temp_averages)  
    print(np.array(energy_averages))
    
    '''
    for i in range(resampled_energy.shape[0]):

        resampled_heat_capacity[i]= np.std(resampled_heat_capacity[i])
        resampled_energy[i]= np.std(resampled_energy[i])
    '''



def magnetisation_resample(data):
    #===================================================
    # Generate 1000 resampled magnetisation data sets @ each temp
    # via the bootstrap method       
    total_magnetisation_resampled_data= []
    for i in range(len(data)):
        temp_resampled_data= []
        for j in range(k):
            bootstrap_resample= np.random.choice(data[i][0][:], size= n)
            temp_resampled_data.append(bootstrap_resample)
        total_magnetisation_resampled_data.append(temp_resampled_data)
    return np.array(total_magnetisation_resampled_data).shape

def write_obs_data(flag, temperature, energy, magnetisation, succeptibility, heat_capacity):
    #===================================================
    # Write calculated obs data to txt
    header= str('temperature, avr_energy, avr_magnetisation, heat_capacity, succeptibility')
    output= np.array([temperature, energy, magnetisation, heat_capacity, succeptibility]).T
    np.savetxt(f'{flag}_obvs_data.txt', output, delimiter= ',', header= header)

def main():
    global k,n
    n,k= 1000, 1000
    data, flag= read_raw_data()
    temp, energy, mag, chi, c_v= calculate_obs(data)
    energy_resampled_data= energy_resample(data)
    find_energy_errors(energy_resampled_data, temp)
    write_obs_data(flag, temp, energy, mag, chi, c_v) 

if __name__== '__main__':
    main()