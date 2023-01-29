import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def generate_lattice():
    #=======================================================
    # Function to return random latice of -1 and 1
    global lattice
    lattice= np.random.choice(np.array([1,-1]), size=(N, N))

def generate_rand_coord():
    #=======================================================
    # Generate random indexes within lattice array bounds
    coords_1= np.random.randint(0, high= N, size= 2)
    coords_2= np.random.randint(0, high= N, size= 2)
    return (coords_1), (coords_2)

def ising_energy(coordX_1, coordY_1, coordX_2, coordY_2, s_center_1, s_center_2, J=1):
    #=======================================================
    # Find the energy of the two swapped states 
    
    if coordX_1 +1 == N:
        coordX_1= -1
    if coordY_1 +1 == N:
        coordY_1= -1 
    if coordX_2 +1 == N:
        coordX_2= -1
    if coordY_2 +1 == N:
        coordY_2= -1
   
    #elif abs(coordX_1-coordX_2)== 1 or abs(coordY_1-coordY_2)== 1:
    
    e_init= (-J*s_center_1*\
            lattice[coordY_1 +1][coordX_1]+\
            lattice[coordY_1 -1][coordX_1]+\
            lattice[coordY_1][coordX_1 +1]+\
            lattice[coordY_1][coordX_1 -1])\
            +(-J*s_center_2*\
            lattice[coordY_2 +1][coordX_2]+\
            lattice[coordY_2 -1][coordX_2]+\
            lattice[coordY_2][coordX_2 +1]+\
            lattice[coordY_2][coordX_2 -1])
    e_final= (-J*s_center_2*\
            lattice[coordY_1 +1][coordX_1]+\
            lattice[coordY_1 -1][coordX_1]+\
            lattice[coordY_1][coordX_1 +1]+\
            lattice[coordY_1][coordX_1 -1])\
            +(-J*s_center_1*\
            lattice[coordY_2 +1][coordX_2]+\
            lattice[coordY_2 -1][coordX_2]+\
            lattice[coordY_2][coordX_2 +1]+\
            lattice[coordY_2][coordX_2 -1])
    return e_init, e_final


def find_kawazaki_delta_e(coords_1, coords_2):
    #=======================================================
    # Compute change in energy between permutations 
    (coordX_1, coordY_1), (coordX_2, coordY_2)= coords_1, coords_2
    s_center_1= lattice[coordY_1][coordX_1]
    s_center_2= lattice[coordY_2][coordX_2]

    if s_center_1 == s_center_2:
        return
    else:
        e_init, e_final= ising_energy(coordX_1, coordY_1, coordX_2, coordY_2,\
                            s_center_1, s_center_2)
    return e_final-e_init

def apply_kawazaki_change(delta_e, coords_1, coords_2, s_center_1, s_center_2):
    #=======================================================
    # Change spin state if appropiate 
    (coordX_1, coordY_1), (coordX_2, coordY_2)= coords_1, coords_2
    
    if delta_e <= 0:
        lattice[coordY_1][coordX_1]= s_center_2
        lattice[coordY_2][coordX_2]= s_center_1
    else:
        prob= np.exp(-delta_e/(kT))
        if np.random.rand() <= prob:
            lattice[coordY_1][coordX_1]= s_center_2
            lattice[coordY_2][coordX_2]= s_center_1
        else:
            return

def kawazaki_dynamic_step(swap, sweep):
    #=======================================================
    # Compute step for kawazaki dynamics
    coords_1, coords_2= generate_rand_coord()
    s_center_1= lattice[coords_1[1]][coords_1[0]]
    s_center_2= lattice[coords_2[1]][coords_2[0]]
    
    if s_center_1 == s_center_2:
        return swap, sweep
    else:
        delta_e= find_kawazaki_delta_e(coords_1, coords_2)
        apply_kawazaki_change(delta_e, coords_1, coords_2, s_center_1, s_center_2)
    swap += 1

    if swap%N**2==0:
        sweep+=1
    return swap, sweep

def initialise_plot():
    #=======================================================
    # Compute one step in glauber dynamics 
    fig = plt.figure()
    im=plt.imshow(lattice, animated=True, vmax=1, vmin=-1)
    return fig, im

def draw_image(im, sweep):
    #=======================================================
    # draw frame of the animation
        plt.cla()
        im= plt.imshow(lattice, animated= True, vmax=1, vmin=-1)
        plt.draw()
        plt.pause(0.0001)
        sweep=0
        return im, sweep

def run_simulation_vis(swap, sweep, time_i= None):
    #=======================================================
    # Run simulation when called   
    generate_lattice()
    fig, im= initialise_plot()
    while True:
        swap, sweep= kawazaki_dynamic_step(swap, sweep)
        
        if sweep%10==0 and sweep!=0:
            im, sweep= draw_image(im, sweep)
            time_f= time.time()
            print(time_f-time_i)
            time_i= time_f

def main():
    if(len(sys.argv) != 4):
        print ("Usage python ising.animation.py {Lattice size} {Temperature} {Flag}")
        print('Simulation flags: v ==> visualise, c ==> calculate')
        sys.exit()
    
    #=======================================================
    # Init parameters
    global N, kT
    N=int(sys.argv[1]) 
    kT=float(sys.argv[2]) 
    flag= str(sys.argv[3])
    swap=1
    sweep=0
    time_i= time.time()
    #========================================================
    if flag == str('v'):
        run_simulation(swap, sweep, time_i)
    elif flag == str('c'):
        print('CALCULATING')
    else:
        raise Exception('Input valid flag\nSimulation flags: v ==> visualise, c ==> calculate')

if __name__ == '__main__':
    main()