import sys
import numpy as np
import matplotlib.pyplot as plt

def generate_lattice():
    # Generate initial latttice with random distribution of states 
    global lattice
    lattice=np.random.choice(np.array([0,1]), size=(N,N))

def initialise_plot():
    fig= plt.figure()
    im= plt.imshow(lattice, animated= True, vmax= 1, vmin=0, cmap= 'winter')
    plt.show()
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

def main():
    if len(sys.argv) != 2:
        print('Run file in command line as ==>\npython3 game_of_life.py N')

    global N
    N= int(sys.argv[1])
    run_simulation()

if __name__=='__main__':
    main()