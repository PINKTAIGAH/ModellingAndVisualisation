import sys
import time
import numpy as np
import matplotlib.pyplot as plt

def generate_lattice():
    # Generate initial latttice with random distribution of states 
    global lattice
    #lattice= np.random.choice(np.array([0, 1]), size=(N,N))
    lattice= np.loadtxt('empty_glider_lattice.txt')

def periodic_boundaries(neighbours):
    # Apply periodic boundaries to neighbour indices if necesary
    for i in range(len(neighbours)):
        if (neighbours[i][0]) >= N:
            neighbours[i][0]= 0
        if (neighbours[i][1]) >= N:
            neighbours[i][1]= 0    
    return tuple(neighbours) 

def update_cell(neighbour_population, i_x, i_y, cell_val):
    # Modify state of cell according to rules
    if cell_val == 1 and neighbour_population < 2:
        lattice[i_y][i_x]=0
    elif cell_val == 1 and neighbour_population > 3:
        lattice[i_y][i_x]=0
    elif cell_val == 1:
        pass
    elif cell_val == 0 and neighbour_population == 3:
        lattice[i_y][i_x] = 1

def find_local_population(i_x, i_y, cell_val):
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

def update_lattice():
    # Update each cell in the lattice
    global lattice_old
    lattice_old= np.copy(lattice)
    # Loop for each cell i a lattice to compute update
    for index, val in np.ndenumerate(lattice_old):
        i_y= index[1]
        i_x= index[0]
        neighbour_population= find_local_population(i_x, i_y, val)
        print(index, val, neighbour_population)
        update_cell(neighbour_population, i_x, i_y, val)

def initialise_plot():
    #=======================================================
    # Compute one step in lattice update 
    fig = plt.figure()
    im=plt.imshow(lattice, animated=True, vmax=1, vmin=0)
    return fig, im


def draw_image(im):
    #=======================================================
    # Draw frame of the animation
        plt.cla()
        im= plt.imshow(lattice, animated= True, vmax=1, vmin=0)
        plt.draw()
        plt.pause(0.0001)
        return im

def run_simulation():
    # Initialise game of life simulaiton
    generate_lattice()
    fig, im= initialise_plot()
    im= draw_image(im)
    # Compute and plot each uptade in state
    while True:
        time.sleep(0.001)
        update_lattice()
        im= draw_image(im)
        plt.cla()


def main():
    """
    if len(sys.argv) != 2:
        print('Run file in command line as ==>\npython3 game_of_life.py N')
    """
    global N
    N= 50
    #N= int(sys.argv[1])
    run_simulation()    
    
if __name__== '__main__':
    main()