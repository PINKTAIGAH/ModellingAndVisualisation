import sys
import matplotlib.animation as animation
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

def main():
    
    if(len(sys.argv) != 3):
        print ("Usage python ising.animation.py {Lattice size} {Temperature}")
        sys.exit()
    
    #=======================================================
    # Init parameters
    global N, kT
    N=int(sys.argv[1]) 
    kT=float(sys.argv[2]) 
    switch=1
    sweep=0
    #time_i= time.time()
    #========================================================

    generate_lattice()
    fig, im= initialise_plot()
    while True:
        switch, sweep, i= glauber_dynamics_step(switch, sweep, i)
        
        if sweep%10==0 and sweep!=0:
            im, sweep= draw_image(im, sweep)
            #time_f= time.time()
            #print(time_f-time_i)
            #time_i= time_f

    

if __name__=='__main__':
    main()