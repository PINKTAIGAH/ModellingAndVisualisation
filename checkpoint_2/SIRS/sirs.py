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

def apply_sirs_rules_S(neigbour_state, i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    if str('I') in neigbour_state and np.random.rand() <= p1:
        lattice[i_y][i_x] = 1

def apply_sirs_rules_I(i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    if np.random.rand() <= p2:
        lattice[i_y][i_x] = 2

def apply_sirs_rules_R(i_y, i_x):
    #=======================================================
    # Apply change to succeptable cell according to SIRS rules
    if np.random.rand() <= p3:
        lattice[i_y][i_x] = 0

def update_lattice():
    #=======================================================
    # Update the lattice per timestep
    i_y, i_x= generate_random_index()
    neigbour_state= find_neigbour_states(i_y, i_x)
    #print(neigbour_state)
    if lattice[i_y][i_x] == 0:
        apply_sirs_rules_S(neigbour_state, i_y, i_x)
    if lattice[i_y][i_x] == 1:
        apply_sirs_rules_I(i_y, i_x)
    if lattice[i_y][i_x] == 2:
        apply_sirs_rules_R(i_y, i_x)

def run_simulation():
    #=======================================================
    # Run SIRS simulation  
    time_steps=1
    sweeps= 0
    generate_lattice()
    fig, im= initialise_plot()
    im= draw_image(im)
    while True:
        update_lattice()
        time_steps+=1
        if time_steps% N**2 == 0:
            im= draw_image(im)
            sweeps+= 1

def main():
    global N, p1, p2, p3
    N= int(sys.argv[1])
    p1, p2, p3= (float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    global sir_key
    sir_key= {  0:'S',
            1:'I',
            2:'R'}
    run_simulation()


if __name__== '__main__':
    main()