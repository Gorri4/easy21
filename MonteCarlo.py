from State import State
from Game import Game


import numpy as np
import random

class MonteCarlo:
    def __init__(self, n0):
        self.n0 = float(n0)
        self.N = np.zeros((40,40,2))
        self.Q = np.zeros((40,40,2))
        self.V = np.zeros((40,40))
        
        self.wins = 0
        self.it = 0
        
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
                
                pairs.append((currentState,actionIndex))
                    
                    
                self.N[currentState.dealer-1,currentState.player-1,actionIndex] += 1
                
                currentState,reward = game.step(currentState,action)
                
            self.wins = self.wins + 1 if reward == 1 else self.wins
            
            for state,action in pairs:
                dealerInx = state.dealer-1
                playerInx = state.player-1
                actionInx = action
                
                step = 1.0 / self.N[dealerInx,playerInx,actionInx]
                rwrd = reward - self.Q[dealerInx,playerInx,actionInx]
                self.Q[dealerInx,playerInx,actionInx] += step*rwrd
                
                
            iterations += iterations
            
            for d in range(10):
                for p in range(21):
                    self.V[d,p] = max(self.Q[d,p,:])
            
        for p in range(21):
            print(self.Q[1,p,1],':',self.Q[1,p,0])
               
                
                
monti = MonteCarlo(100)
monti.train(50000)