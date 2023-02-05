import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def generate_lattice_vis():
    #=======================================================
    # Function to return random latice of -1 and 1
    global lattice
    lattice= np.random.choice(np.array([1,-1]), size=(N, N))

def generate_lattice_calc():
    #=======================================================
    # Function to return a lattice with all cells in an identical state.
    global lattice
    lattice= np.ones((N,N))

def generate_rand_coord():
    #=======================================================
    # Generate random indexes within lattice array bounds
    coords= np.random.randint(0, high= N, size= 2)
    return (coords)

def ising_energy(coords, s_center, s_center_flip, J=1):
    #=======================================================
    # Find energy of unperturbed and perturbed state
    coordX, coordY= coords

    if coordX+1 == N:
        coordX= -1
    
    if coordY+1 == N:
        coordY= -1
    
    e_init= -J*s_center*(lattice[coordY +1][coordX]+\
                    lattice[coordY -1][coordX]+\
                    lattice[coordY][coordX +1]+\
                    lattice[coordY][coordX -1])

    e_final= -J*s_center_flip*(lattice[coordY +1][coordX]+\
                    lattice[coordY -1][coordX]+\
                    lattice[coordY][coordX +1]+\
                    lattice[coordY][coordX -1])

    return e_init, e_final

def find_glauber_delta_e(coordX, coordY):
    #=======================================================
    # Find change in energy between states  
    s_center= lattice[coordY][coordX]
    s_center_flip= s_center * -1

    e_init, e_final= ising_energy((coordX,coordY), s_center, s_center_flip)
    return  e_final-e_init

def apply_glauber_change(delta_e, coordX, coordY):
    #=======================================================
    # Change spin state if appropiate 
    if delta_e <= 0:
        lattice[coordY][coordX]= -1 * lattice[coordY][coordX]
    else:
        prob= np.exp(-delta_e/(kT))
        if np.random.rand() <= prob:
            lattice[coordY][coordX]= -1 * lattice[coordY][coordX]
        else:
            return

def glauber_dynamics_step(switch, sweep):
    #=======================================================
    # Compute one step in glauber dynamics  
    coordX, coordY= generate_rand_coord()
    delta_e= find_glauber_delta_e(coordX, coordY)
    apply_glauber_change(delta_e, coordX, coordY)
    switch += 1

    if switch%N**2==0:
        sweep+=1
    return switch, sweep

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

def run_simulation_visualisation(switch,sweep,time_i):
    #=======================================================
    # Run simulation and visualise when called
    i= 0
    fig, im= initialise_plot()
    while True:
        switch, sweep= glauber_dynamics_step(switch, sweep)
        
        if sweep%10==0 and sweep!=0:
            i+=1
            im, sweep= draw_image(im, sweep)
            time_f= time.time()
            print(i, time_f-time_i)
            time_i= time_f
    

def run_simulation_calculation(switch, sweep):
    #=======================================================
    # Run simulation and calculation of energy and magnetisation when called
    fig, im= initialise_plot()
    temps=np.arange(1, 3.1, 0.1)
    for temp in np.nditer(temps):   
        global kT
        kT= temp
        if os.path.isfile(f'raw_glauber_data/glauber_data({kT:.2}).txt')== True:
            os.remove(f'raw_glauber_data/glauber_data({kT:.2}).txt')
        
        collected_dp= 0
        total_dp= 20
        while True:
            switch, sweep= glauber_dynamics_step(switch, sweep)
            if sweep%10==0 and sweep!=0:
                im, sweep= draw_image(im, sweep)
                collected_dp += 1
                print(f'kT= {kT:.2} ### {collected_dp-1}/{total_dp} dp collected')
                state_energy= find_total_energy()
                state_magnetisation= find_total_magnetisation()
                dp= np.array([state_energy, state_magnetisation])

                with open(f'raw_glauber_data/glauber_data({kT:.2}).txt','a') as f:   
                    np.savetxt(f, dp.reshape(1,-1), delimiter=",", fmt= '%s')
                sweep= 1
            if collected_dp > total_dp:
                break
    sys.exit()

def main():
    
    if(len(sys.argv) != 4):
        print ("Usage python ising.animation.py {Lattice size} {Temperature} {Flag}")
        sys.exit()
    
    #=======================================================
    # Init parameters
    global N, kT
    N=int(sys.argv[1]) 
    kT=float(sys.argv[2]) 
    flag= str(sys.argv[3])
    switch=1
    sweep=0
    time_i= time.time()
    #========================================================
    if flag == str('v'):
        generate_lattice_vis()
        run_simulation_visualisation(switch, sweep, time_i)
    elif flag == str('c'):
        generate_lattice_calc()
        run_simulation_calculation(switch, sweep)
    else:
        raise Exception('Input valid flag\nSimulation flags: v ==> visualise, c ==> calculate')



    

if __name__=='__main__':
    main()