import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# 0 is Down state ======> S= +1
# 1 is Up state ========> S= -1

class ising(object):
    
    def __init__(self, kT, N, step):
        self.kT= kT
        self.J= 1
        self.N= N
        self.step= step
        self.generateLattice()
        self.switch= 1
        self.sweep=0
        self.nSweep= self.N**2
        self.timeA= time.time()


    def generateLattice(self):
        self.lattice= np.random.choice(np.array([1,-1]),size=(self.N, self.N))
        #self.lattice= np.random.choice(np.array([-1,1]),size= (self.N, self.N))
           
    def generateRandCoord(self):
        coord= np.random.randint(0, high= self.N, size= 2)
        return (coord)

    def isingEnergy(self):
        coordX= self.coordX
        coordY= self.coordY
        
        if self.coordX+1 == self.N:
            coordX= -1
        
        if self.coordY+1 == self.N:
            coordY= -1
        
        self.eInit= -self.J*self.SCenter*(self.lattice[coordY +1][coordX]+\
                        self.lattice[coordY -1][coordX]+\
                        self.lattice[coordY][coordX +1]+\
                        self.lattice[coordY][coordX -1])
    
        self.eFinal= -self.J*self.SCenterFlip*(self.lattice[coordY +1][coordX]+\
                        self.lattice[coordY -1][coordX]+\
                        self.lattice[coordY][coordX +1]+\
                        self.lattice[coordY][coordX -1])
    
    def findGlauberDeltaE(self):
        self.coordX, self.coordY= self.generateRandCoord()
        self.SCenter= self.lattice[self.coordY][self.coordX]
        self.SCenterFlip= self.SCenter * -1

        self.isingEnergy()
        self.deltaE= self.eFinal-self.eInit

    def applyGlauberChange(self):
        if self.deltaE <= 0:
            self.lattice[self.coordY][self.coordX]= -1 * self.lattice[self.coordY][self.coordX]
            #self.updateHalo()
        else:
            prob= np.exp(-self.deltaE/(self.kT))
            if np.random.rand() <= prob:
                self.lattice[self.coordY][self.coordX]= -1 * self.lattice[self.coordY][self.coordX]
                #self.updateHalo()
            else:
                return
    
    def glauberDynamicsStep(self):
        self.findGlauberDeltaE()
        self.applyGlauberChange()
        self.switch += 1

        if self.switch%self.N**2==0:
            self.sweep+=1
            time_a= time.time()
            print(time_a-self.timeA)
            self.timeA= time_a
    
    def runSimulation(self):
        self.fig = plt.figure()
        self.im=plt.imshow(self.lattice, animated=True, vmax=1, vmin=-1)
        plt.draw()
        while True:
            self.glauberDynamicsStep()
            
            if self.sweep%10==0 and self.sweep!=0:
                plt.cla()
                self.im= plt.imshow(self.lattice, animated= True, vmax=1, vmin=-1)
                plt.draw()
                plt.pause(0.0001)
                self.sweep=0


def main():
    model= ising(3,50,100)
    model.runSimulation()


if __name__ == '__main__':
    main()