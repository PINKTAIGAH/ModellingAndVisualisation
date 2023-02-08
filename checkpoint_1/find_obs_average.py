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
        succeptibility.append((np.average(np.absolute(data[i][1][:]**2))\
            - np.average(np.absolute(data[i][1][:]))**2)/(2500*temperature[i]))
        heat_capacity.append((np.average(np.absolute(data[i][0][:]**2))\
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
    return np.array(total_magnetisation_resampled_data)


def find_energy_errors(data, raw_resampled_energy, temperature):
    #===================================================
    # Find errors for heat capacity and energy errors
    heat_capacity_resampled= np.empty(raw_resampled_energy.shape[:2])
    heat_capacity_error= []
    energy_error=[]

    for i in range(raw_resampled_energy.shape[0]):
        for j in range(raw_resampled_energy.shape[1]):
            
            heat_capacity_resampled[i][j]= (np.average(np.absolute(raw_resampled_energy[i][j][:]**2))\
            - np.average(np.absolute(raw_resampled_energy[i][j][:]))**2)/(2500*temperature[i]**2)
    
    for i in range(raw_resampled_energy.shape[0]):
        c_averages= []
        for j in range(raw_resampled_energy.shape[1]):
            c_averages.append(np.average(heat_capacity_resampled[i][j]))
        c_averages= np.array(c_averages)
        heat_capacity_error.append(np.std(c_averages))  
        energy_error.append(np.std(data[i][0])/np.sqrt(data[i].shape[1]))
    
    return np.array(energy_error), np.array(heat_capacity_error)

def find_magnetisation_errors(data, raw_resampled_mag, temperature):
    #===================================================
    # Find errors for succeptibility and magnetisation errors
    succeptibility_resampled= np.empty(raw_resampled_mag.shape[:2])
    succeptibility_error= []
    magnetisation_error=[]

    for i in range(raw_resampled_mag.shape[0]):
        for j in range(raw_resampled_mag.shape[1]):
            
            succeptibility_resampled[i][j]= (np.average(np.absolute(raw_resampled_mag[i][j][:]**2))\
            - np.average(np.absolute(raw_resampled_mag[i][j][:]))**2)/(2500*temperature[i])
    
    for i in range(raw_resampled_mag.shape[0]):
        chi_averages= []
        for j in range(raw_resampled_mag.shape[1]):
            chi_averages.append(np.average(succeptibility_resampled[i][j]))
        chi_averages= np.array(chi_averages)
        succeptibility_error.append(np.std(chi_averages))  
        magnetisation_error.append(np.std(data[i][1])/np.sqrt(data[i].shape[1]))
    
    return np.array(magnetisation_error), np.array(succeptibility_error)


def write_obs_data(flag, temperature, energy, magnetisation, succeptibility, heat_capacity,\
                    e_energy, e_cv, e_mag, e_succ):
    #===================================================
    # Write calculated obs data to txt
    header= str('temperature, avr_energy, avr_magnetisation, heat_capacity, succeptibility, E_energy, E_heat capacity, E_magnetisation, E_succeptibility')
    output= np.array([temperature, energy, magnetisation, heat_capacity, succeptibility,\
                        e_energy, e_cv, e_mag, e_succ]).T
    np.savetxt(f'{flag}_obvs_data.txt', output, delimiter= ',', header= header)

def main():
    global k,n
    n,k= 1000, 1000
    data, flag= read_raw_data()
    temp, energy, mag, chi, cv= calculate_obs(data)
    energy_resampled_data= energy_resample(data)
    magnetisation_resampled_data= magnetisation_resample(data)
    e_energy, e_cv= find_energy_errors(data, energy_resampled_data, temp)
    e_mag, e_succ= find_magnetisation_errors(data, magnetisation_resampled_data, temp)
    write_obs_data(flag, temp, energy, mag, chi, cv, e_energy, e_cv, e_mag, e_succ ) 

if __name__== '__main__':
    main()