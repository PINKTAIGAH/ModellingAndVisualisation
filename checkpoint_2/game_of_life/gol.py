import sys
import time
import numpy as np
import matplotlib.pyplot as plt

def generate_lattice():
    #=======================================================
    # Generate initial latttice  
    global lattice
    if flag_init == str('r'):
        # Random lattice
        lattice= np.random.choice(np.array([0, 1]), size=(N,N))
    elif flag_init == str('gl'):
        # Generic lattice with glider
        lattice= np.loadtxt('empty_glider_lattice.txt')
    elif flag_init == str('bl'):
        # Generic lattice with blinker
        lattice= np.loadtxt('empty_blinker_lattice.txt')
    else:
        raise Exception('Input valid flag\nInit latice type: r ==> random, gl ==> glider, bl ==> blinker')

def find_tot_active_sites():
    #=======================================================
    # Find the total active sites in a lattice
    return np.sum(lattice)

def find_lattice_com():
    #=======================================================
    # Find the total active sites in a lattice
    active_sites = 0
    com_sum= np.zeros(2)
    for index, val in np.ndenumerate(lattice):
        if val == 1:
            active_sites += 1
            com_sum+= index          
    
    com_index= com_sum/active_sites
    return np.sum(com_index)/com_index.size

def steady_state_test(tot_active_sites_list):
    #=======================================================
    # Return bool representing if lattice is in steady state
    active_site_derrivative= tot_active_sites_list[-1] - tot_active_sites_list[-2]
    if active_site_derrivative == 0:
        return True
    else:
        return False
    
def periodic_boundaries(neighbours_list):
    #=======================================================
    # Apply periodic boundaries to neighbour indices if necesary
    for i in range(len(neighbours_list)):
        if (neighbours_list[i][0]) >= N:
            neighbours_list[i][0]= 0
        if (neighbours_list[i][1]) >= N:
            neighbours_list[i][1]= 0    
    return tuple(neighbours_list) 

def find_local_population(i_x, i_y):
    #=======================================================
    # Compute the local population of a cell
    i_u, i_d= [i_x, i_y+1], [i_x, i_y-1]
    i_l, i_r= [i_x-1, i_y], [i_x+1, i_y]
    i_ul, i_ur= [i_x-1, i_y+1], [i_x+1, i_y+1]
    i_dl, i_dr= [i_x-1, i_y-1], [i_x+1, i_y-1]
    
    [i_u, i_d, i_l, i_r, i_ul, i_ur, i_dl, i_dr]= periodic_boundaries([i_u, i_d, i_l, i_r, i_ul, i_ur, i_dl, i_dr])

    neighbour_population= lattice_old[i_u[1]][i_u[0]] + lattice_old[i_d[1]][i_d[0]] +\
            lattice_old[i_r[1]][i_r[0]] + lattice_old[i_l[1]][i_l[0]] +\
            lattice_old[i_ur[1]][i_ur[0]] + lattice_old[i_ul[1]][i_ul[0]] +\
            lattice_old[i_dl[1]][i_dl[0]] + lattice_old[i_dr[1]][i_dr[0]]
    
    return neighbour_population

def update_cell(neighbour_population, i_x, i_y, cell_val):
    #=======================================================
    # Modify state of cell according to rules
    if cell_val == 1 and neighbour_population < 2:
        lattice[i_y][i_x]=0
    elif cell_val == 1 and neighbour_population > 3:
        lattice[i_y][i_x]=0
    elif cell_val == 1:
        pass
    elif cell_val == 0 and neighbour_population == 3:
        lattice[i_y][i_x] = 1

def update_lattice():
    #======================================================= 
    # Update each cell in the lattice
    global lattice_old
    lattice_old= np.copy(lattice)
    # Loop for each cell i a lattice to compute update
    for index, val in np.ndenumerate(lattice_old):
        i_y= index[0]
        i_x= index[1]
        neighbour_population= find_local_population(i_x, i_y)
        update_cell(neighbour_population, i_x, i_y, val)

def initialise_plot():
    #=======================================================
    # Compute one step in lattice update 
    fig= plt.figure()
    im= plt.imshow(lattice, animated=True, vmax=1, vmin=0)
    return fig, im

def draw_image(im):
    #=======================================================
    # Draw frame of the animation
        plt.cla()
        im= plt.imshow(lattice, animated= True, vmax=1, vmin=0)
        plt.draw()
        plt.pause(0.0001)
        return im

def check_steady_state(pop, pop_old, counter):
    #=======================================================
    # Check if system is in steady state 
    if pop_old == pop:
            counter+=1
    else:
        counter= 0
    return counter

def run_simulation_vis():
    #=======================================================
    # Initialise game of life simulaiton for visualisation
    generate_lattice()
    fig, im= initialise_plot()
    im= draw_image(im)
    # Compute and plot each uptade in state
    while True:
        time.sleep(0.001)
        update_lattice()
        im= draw_image(im)

def run_simulation_steady_state():
    #=======================================================
    # Initialise game of life simulaiton for steady state calculation 
    print('Initialised steady state calculation')
    counter= 0
    sweep= 0
    collected_dp= 0
    total_dp= 1000
    pop_list= [250]
    steady_state_time=[]
    generate_lattice()
    # Compute and plot each update in state for steady state calculation
    while True:
        time.sleep(0.001)
        update_lattice()
        pop= find_tot_active_sites()
        sweep+=1
        counter= check_steady_state(pop, pop_list[-1], counter)
        pop_list.append(pop)
        if counter == 10 or sweep == 5000:
            steady_state_time.append(sweep)
            collected_dp+=1
            print(f'Equilibration time= {sweep} ### {collected_dp}/{total_dp} dp collected')
            generate_lattice()
            sweep=0
        if total_dp == collected_dp:
            break
    np.savetxt('equilibration_time_dataset', np.array([steady_state_time]).T, delimiter= ',') 
    sys.exit()

def run_simulation_com():
    #=======================================================
    # Initialise game of life simulaiton for steady state calculation 
    com_position_list= []
    time_list= []
    sweep= 0
    generate_lattice()
    # Compute and plot each uptade in state
    while True:
        time.sleep(0.001)
        update_lattice()
        com_position_list.append(find_lattice_com())
        time_list.append(sweep)
        sweep+= 1
        print(sweep)
        if sweep == 170:
            break
    com_position_list= np.array(com_position_list)
    velocity_list= np.diff(np.array(com_position_list)) 
    anomaly_index_1= np.array(np.asarray((velocity_list< 0)).nonzero())
    anomaly_index_2= np.array(np.asarray((velocity_list>1)).nonzero())
    total_anomalies_index= np.append(anomaly_index_1, anomaly_index_2)
    com_position_list= np.delete(com_position_list, total_anomalies_index)
    np.savetxt('com_dataset.txt', com_position_list.T)
    
def main():
    if len(sys.argv) != 4:
        print('Run file in command line as ==>\npython3 game_of_life.py [Lattice size] [Init lattice type] [Simulation type]')
    global N, flag_init, flag_sim
    N= int(sys.argv[1])
    flag_init= str(sys.argv[2])
    flag_sim= str(sys.argv[3])
    if flag_sim == str('vis'):
        run_simulation_vis() 
    elif flag_sim == str('ss'):
        run_simulation_steady_state()
    elif flag_sim == str('com'):
        run_simulation_com()
    else:
        raise Exception('Input valid flag\nSimulation type: vis ==> visualisation, ss ==> Steady state, com ==> Center of mass')

if __name__== '__main__':
    main()
