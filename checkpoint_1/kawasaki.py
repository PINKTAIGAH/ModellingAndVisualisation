import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

"""
Script that will simulate a two state system of the ising model according to 
kawasaki dynamics. c flag will compute and print total energy and magnetisation for 
temperature ranges between kT= 1 to 3. v flag will visualize the system at specified
temperature
Input ==> python kawasaki.py [N] [kT] [flag]
"""

def generate_lattice_vis():
    #=======================================================
    # Function to return random latice of -1 and 1
    global lattice
    lattice= np.random.choice(np.array([1,-1]), size=(N, N))

def generate_lattice_calc():
    #=======================================================
    # Function to return a lattice with all cells in near ground state
    global lattice
    lattice= np.ones((N,N))
    lattice[int(N/4):int(3*N/4), int(N/4):int(3*N/4)]= -1

def generate_rand_coord():
    #=======================================================
    # Generate random indexes within lattice array bounds
    coords_1= np.random.randint(0, high= N, size= 2)
    coords_2= np.random.randint(0, high= N, size= 2)
    return (coords_1), (coords_2)

def ising_energy(coordX_1, coordY_1, coordX_2, coordY_2, s_center_1, s_center_2, J=1):
    #=======================================================
    # Find the energy of the two swapped states 
    state_ajacent= (False, ())

    if coordX_1 +1 == N:
        coordX_1= -1
    if coordY_1 +1 == N:
        coordY_1= -1 
    if coordX_2 +1 == N:
        coordX_2= -1
    if coordY_2 +1 == N:
        coordY_2= -1
    
    e_init= (-J*s_center_1*\
            (lattice[coordY_1 +1][coordX_1]+\
            lattice[coordY_1 -1][coordX_1]+\
            lattice[coordY_1][coordX_1 +1]+\
            lattice[coordY_1][coordX_1 -1]))\
            +(-J*s_center_2*\
            (lattice[coordY_2 +1][coordX_2]+\
            lattice[coordY_2 -1][coordX_2]+\
            lattice[coordY_2][coordX_2 +1]+\
            lattice[coordY_2][coordX_2 -1]))
    e_final= (-J*s_center_2*\
            (lattice[coordY_1 +1][coordX_1]+\
            lattice[coordY_1 -1][coordX_1]+\
            lattice[coordY_1][coordX_1 +1]+\
            lattice[coordY_1][coordX_1 -1]))\
            +(-J*s_center_1*\
            (lattice[coordY_2 +1][coordX_2]+\
            lattice[coordY_2 -1][coordX_2]+\
            lattice[coordY_2][coordX_2 +1]+\
            lattice[coordY_2][coordX_2 -1]))
    
    if abs(coordX_1-coordX_2)== 1 or abs(coordY_1-coordY_2)== 1:
        e_final+=2
        e_init+=2

    return e_init, e_final


def find_kawazaki_delta_e(coords_1, coords_2):
    #=======================================================
    # Compute change in energy between permutations 
    (coordX_1, coordY_1), (coordX_2, coordY_2)= coords_1, coords_2
    s_center_1= lattice[coordY_1][coordX_1]
    s_center_2= lattice[coordY_2][coordX_2]

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

def find_total_magnetisation():
    #=======================================================
    # Compute total magnetisation of lattice
    return lattice.sum()

def kawazaki_dynamic_step(swap, sweep):
    #=======================================================
    # Compute step for kawazaki dynamics
    coords_1, coords_2= generate_rand_coord()
    s_center_1= lattice[coords_1[1]][coords_1[0]]
    s_center_2= lattice[coords_2[1]][coords_2[0]]
    
    if s_center_1 == s_center_2:
        pass
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

def run_simulation_visualisation(swap, sweep, time_i= None):
    #=======================================================
    # Run simulation when called   
    fig, im= initialise_plot()
    while True:
        swap, sweep= kawazaki_dynamic_step(swap, sweep)
        # Visualise current state
        if sweep%10==0 and sweep!=0:
            im, sweep= draw_image(im, sweep)
            time_f= time.time()
            print(time_f-time_i)
            time_i= time_f

def find_total_energy(J=1):
    #=======================================================
    # Find total energy of lattice    
    total_energy=[]
    for inx, val in np.ndenumerate(lattice):
        iy,ix= inx

        if ix+1 == N:
            ix= -1
    
        if iy+1 == N:
            iy= -1
    
        e_cell= -J*val*(lattice[iy +1][ix]+\
                    lattice[iy -1][ix]+\
                    lattice[iy][ix +1]+\
                    lattice[iy][ix -1])
        total_energy.append(e_cell)
    return sum(total_energy)/2


def find_total_magnetisation():
    #=======================================================
    # Compute total magnetisation of lattice
    return lattice.sum()

def run_simulation_calculation(swap, sweep):
    #=======================================================
    # Run simulation and calculation of energy and magnetisation when called
    fig, im= initialise_plot()
    temps=np.arange(1, 3.1, 0.1)
    # Loop for desired temperature ranges    
    for temp in np.nditer(temps):   
        global kT
        kT= temp
        # Check if raw data file exists and deleat if it does        
        if os.path.isfile(f'raw_kawasaki_data/kawasaki_data({kT:.2}).txt')== True:
            os.remove(f'raw_kawasaki_data/kawasaki_data({kT:.2}).txt')
        collected_dp= 0
        total_dp= 1000
        while True:
            swap, sweep= kawazaki_dynamic_step(swap, sweep)
            # Write out data of current state and visualise it            
            if sweep%10==0 and sweep!=0:
                im, sweep= draw_image(im, sweep)
                collected_dp += 1
                print(f'kT= {kT:.2} ### {collected_dp-1}/{total_dp} dp collected')
                state_energy= find_total_energy()
                state_magnetisation= find_total_magnetisation()
                dp= np.array([state_energy, state_magnetisation])
                
                with open(f'raw_kawasaki_data/kawasaki_data({kT:.2}).txt','a') as f:   
                    np.savetxt(f, dp.reshape(1,-1), delimiter=",", fmt= '%s')
                sweep= 1 
            if collected_dp > total_dp:
                break
    sys.exit()

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
        generate_lattice_vis()
        run_simulation_visualisation(swap, sweep, time_i)
    elif flag == str('c'):
        generate_lattice_calc()
        run_simulation_calculation(swap, sweep)
    else:
        raise Exception('Input valid flag\nSimulation flags: v ==> visualise, c ==> calculate')

if __name__ == '__main__':
    main()