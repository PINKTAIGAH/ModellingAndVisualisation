"""
Script that will simul;ate a SIRS model with a variary of outputs depeding on the inputs
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import time

def initialise_plot():
    #=======================================================
    # Compute one step in lattice update 
    fig= plt.figure()
    im= plt.imshow(lattice, animated=True, vmax=2, vmin=0, cmap='cool')
    fig.colorbar(im)
    return fig, im

def draw_image(im):
    #=======================================================
    # Draw frame of the animation
        plt.cla()
        im= plt.imshow(lattice, animated= True, vmax=2, vmin=0, cmap='cool')
        plt.draw()
        plt.pause(0.001)
        return im

def generate_lattice():
    #=======================================================
    # Generate initial latttice  
    global lattice
    lattice= np.random.choice(np.array([0, 1, 2]), size=(N,N))

def generate_random_index():
    #=======================================================
    # Return a random index within the lattice
    coords= np.random.randint(0, high= N, size= 2)
    return (coords)

def periodic_boundaries(neighbours_list):
    #=======================================================
    # Apply periodic boundaries to neighbour indices if necesary
    for i in range(len(neighbours_list)):
        if (neighbours_list[i][0]) >= N:
            neighbours_list[i][0]= 0
        if (neighbours_list[i][1]) >= N:
            neighbours_list[i][1]= 0    
    return tuple(neighbours_list) 


def find_nearest_neigbours(i_y, i_x):
    #=======================================================
    # Return indices of nearest neighbours of a lattice points
    i_d, i_u= [i_y+1, i_x], [i_y-1, i_x]
    i_l, i_r= [i_y, i_x-1], [i_y, i_x+1]
    [i_u, i_d, i_l, i_r]= periodic_boundaries([i_u, i_d, i_l, i_r])
    return i_u, i_d, i_l, i_r

def find_neigbour_states(i_y, i_x):
    #=======================================================
    # Return list containing state of neighbour cells
    i_u, i_d, i_l, i_r= find_nearest_neigbours(i_y, i_x)
    neigbour_vals= [lattice[i[0]][i[1]] for i in [i_u, i_d, i_l, i_r]]
    neigbour_states= [sir_key[i] for i in tuple(neigbour_vals)]
    return np.array(neigbour_states)


def find_infected_number():
    #=======================================================
    # Compute the infected number of an array
    n_infected= lattice[lattice == 2].size
    return n_infected

def apply_sirs_rules_S(neigbour_state, i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    # S ==> I
    if str('I') in neigbour_state and np.random.rand() <= p1:
        lattice[i_y][i_x] = 2

def apply_sirs_rules_I(i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    # I ==> R
    if np.random.rand() <= p2:
        lattice[i_y][i_x] = 0

def apply_sirs_rules_R(i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    # R ==> S
    if np.random.rand() <= p3:
        lattice[i_y][i_x] = 1

def update_lattice():
    #=======================================================
    # Update the lattice per timestep
    i_y, i_x= generate_random_index()
    neigbour_state= find_neigbour_states(i_y, i_x)
    if sir_key[lattice[i_y][i_x]] == str('S'):
        apply_sirs_rules_S(neigbour_state, i_y, i_x)
    if sir_key[lattice[i_y][i_x]] == str('I'):
        apply_sirs_rules_I(i_y, i_x)
    if sir_key[lattice[i_y][i_x]] == str('R'):
        apply_sirs_rules_R(i_y, i_x)

def run_simulation_vis():
    #=======================================================
    # Run SIRS simulation in visualisation mode 
    time_steps=1
    sweeps= 0
    generate_lattice()
    fig, im= initialise_plot()
    im= draw_image(im)
    while True:
        update_lattice()
        print(find_infected_number())
        time_steps+=1
        if time_steps% N**2 == 0:
            sweeps+= 1
            time_steps=1
            im= draw_image(im)

def run_simulation_ph():
    #=======================================================
    # Run SIRS simulation in phase diagram mode
    p1_vals= np.arange(0, 1.05, 0.05)
    p3_vals= np.arange(0, 1.05, 0.05) 
    time_steps=1
    sweeps= 0
    dp_total= 1100
    for i in range(p1_vals.size):
        global p1
        p1= p1_vals[i]
        p1_const_data= []
        for j in range(p3_vals.size):
            generate_lattice()
            global p3
            p3= p3_vals[j]
            p1_p3_const_data= []
            while True:
                update_lattice()
                time_steps+=1
                if time_steps% N**2 == 0:
                    sweeps+= 1
                    time_steps=1
                    infected_number= find_infected_number()
                    p1_p3_const_data.append(infected_number)
                    print(f'p1={p1:.2} ## p3={p3:.2} ## Data points collected: {sweeps}/{dp_total}')
                if sweeps == dp_total:
                    sweeps= 0
                    break
            p1_const_data.append(p1_p3_const_data)
        np.savetxt(f'Data/{p1_vals[i]:.2}_contour_data.txt', np.array(p1_const_data).T) 

def run_simulation_wv():
    #=======================================================
    # Run SIRS simulation in phase diagram mode
    p1_vals= np.arange(0.2, 0.51, 0.01)  
    time_steps=1
    sweeps= 0
    dp_total= 10000
    data_total= []
    for i in range(p1_vals.size):
        p1_const_data= []
        global p1
        p1= p1_vals[i]
        generate_lattice()
        while True:
            update_lattice()
            time_steps+=1
            if time_steps% N**2 == 0:
                sweeps+= 1
                time_steps=1
                infected_number= find_infected_number()
                p1_const_data.append(infected_number)
                print(f'p1={p1_vals[i]:.2} ## Data points collected: {sweeps}/{dp_total}')
            if sweeps == dp_total:
                sweeps= 0
                break        
        data_total.append(p1_const_data)
    np.savetxt(f'Data/wave_contour_data.txt', np.array(data_total).T) 
    

def main():
    global N, p1, p2, p3
    N= int(sys.argv[1])
    p1, p2, p3= (float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    global flag
    flag= str(sys.argv[5])
    global sir_key
    sir_key= {  1:'S',
            2:'I',
            0:'R'}
    if flag == str('vis'):
        # Run visualisation of SIRS model with given parameters
        run_simulation_vis()
    elif flag == str('ph'):
        # Compute the phase contour diagram of infection fraction for p_2 constant
        run_simulation_ph()
    elif flag == str('wv'):
        # Compute the wave location of infection fraction for p_2 constant
        run_simulation_wv()

if __name__== '__main__':
    main()