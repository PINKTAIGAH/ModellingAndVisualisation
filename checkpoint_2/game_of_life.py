import sys
import numpy as np
import matplotlib.pyplot as plt

def generate_lattice():
    global lattice
    lattice= np.random.choice([0,1], size= (N,N))

def update_cell(neighbour_population, i_x, i_y, cell_val):
    if cell_val == 1 and neighbour_population < 2 or neighbour_population > 3:
        lattice[i_y][i_x]=0
    elif cell_val == 1:
        pass
    elif cell_val == 0 and neighbour_population == 3:
        lattice[i_y][i_x] = 1



def find_local_population(i_x, i_y, cell_val):
    i_u, i_d= (i_x, i_y+1), (i_x, i_y-1)
    i_l, i_r= (i_x-1, i_y), (i_x+1, i_y)
    i_ul, i_ur= (i_x-1, i_y+1), (i_x+1, i_y+1)
    i_dl, i_dr= (i_x-1, i_y-1), (i_x+1, i_y-1)

    neighbour_population= lattice_old[i_u[1]][i_u[0]] + lattice_old[i_d[1]][i_d[1]] +\              lattice_old[i_r[1]][i_r[0]] + lattice_old[i_l[1]][i_l[0]] +\
                lattice_old[i_ur[1]][i_ur[0]] + lattice_old[i_ul[1]][i_ul[0]] +\
                lattice_old[i_dl[1]][i_dl[0]] + lattice_old[i_dr[1]][i_dr[0]]
    return neighbour_population

def update_lattice():
    global lattice_old
    lattice_old= np.copy(lattice)
    for index, val in np.ndenumerate(lattice):
        i_y= index[1]
        i_x= index[0]
        neighbour_population= find_local_population(i_x, i_y, val)
        update_cell(neighbour_population, i_x, i_y, val)

def main():
    global N
    N= sys.argv[1]    
    
if __name__== '__main__':
    main()

