from State import State
from Game import Game


import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class MonteCarlo:
    def __init__(self, n0):
        self.n0 = float(n0)
        self.N = np.zeros((40,40,2))
        self.Q = np.zeros((40,40,2))
        self.V = np.zeros((40,40))
        
        self.wins = 0
        self.iterations = 0
        
    def epsilonGreedy(self,state):
        
        visits = sum(self.N[state.dealer-1,state.player-1,:])
        
        epsilon = self.n0 / (self.n0 + visits)

        if(random.random() < epsilon):
            if(random.random() < 0.5):
                action = 'hit'
            else:
                action = 'stick'
        else:
            value = np.argmax(self.Q[state.dealer-1, state.player-1,:])
            
            if(self.Q[state.dealer-1, state.player-1,1]==value):
                action = 'hit'
            else:
                action = 'stick'
                
        return action
        
    def train(self, iterations):
        for rounds in range(iterations):
            pairs = []
            game = Game() 
            
            currentState = State(game.dealerTakeFirstTurn(), game.playerTakeFirstTurn(),False)
            
            while(not currentState.finished):
                action = self.epsilonGreedy(currentState)
                actionIndex = 0
                
                if(action == 'hit'):
                    actionIndex = 0
                else:
                    actionIndex = 1
                    
                #print('player:',currentState.player,'dealer:',currentState.dealer,'playerAction:',action)
                
                pairs.append((currentState.player,currentState.dealer,actionIndex))
                    
                self.N[currentState.dealer-1,currentState.player-1,actionIndex] += 1
                
                currentState,reward = game.step(currentState,action)
                
                
            self.wins = self.wins + 1 if reward == 1 else self.wins
            
            for player,dealer,action in pairs:
                dealerInx = dealer-1
                playerInx = player-1
                actionInx = action
                
                step = 1.0 / self.N[dealerInx,playerInx,actionInx]
                rwrd = reward - self.Q[dealerInx,playerInx,actionInx]
                self.Q[dealerInx,playerInx,actionInx] += step*rwrd
                
                
        self.iterations += iterations
        
        #print(float(self.wins/self.iterations*100))
            
        for d in range(10):
            for p in range(21):
                self.V[d,p] = max(self.Q[d,p,:])
                    
    
    def playGame(self):
        game = Game()
        currentState = State(game.dealerTakeFirstTurn(), game.playerTakeFirstTurn(),False)
        while(not currentState.finished):
            value = np.argmax(self.Q[currentState.dealer-1, currentState.player-1,:])
            
            if(self.Q[currentState.dealer-1, currentState.player-1,1]==value):
                action = 'hit'
            else:
                action = 'stick'
                
            currentState,reward = game.step(currentState,action)
        
        return reward
    
    def plotImage(self, b):
        X = np.arange(0, 10, 1)
        Y = np.arange(0, 21, 1)
        X, Y = np.meshgrid(X, Y)
        Z = self.V[X,Y]
        yfrb = b.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.Spectral, linewidth=0, antialiased=False)
        return yfrb
        

monti = MonteCarlo(100)

for i in range(10):
    figure = plt.figure('image'+str(i))
    b = figure.add_subplot(111, projection='3d')
    monti.train(50000)
    b.clear()
    monti.plotImage(b)
    


