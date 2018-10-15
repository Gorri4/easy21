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
        self.N = np.zeros((10,21,2)) #Stores the number of times a state is visited
        self.Q = np.zeros((10,21,2)) #3 dimensional table containing values for each action
        self.V = np.zeros((10,21)) #The value table containing action for each state
        
        self.wins = 0 #Number of times a player has won
        self.iterations = 0 #Number of iterations
    
    '''Handles the epsilon greedy exploration stratergy. The epsilon values gets smaller as the number of 
       visits per state increases.'''
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
    
    '''This functions handles the training process of the MonteCarlo agent'''    
    def train(self, iterations):
        for rounds in range(iterations):
            pairs = [] #Stores all the states visited during each episode.
            game = Game() #Create a instance of the game
            
            
            currentState = State(game.dealerTakeFirstTurn(), game.playerTakeFirstTurn(),False)#State after the first turn
            
            while(not currentState.finished): #While the players are still playing
                
                action = self.epsilonGreedy(currentState)
                actionIndex = 0
                
                if(action == 'hit'):    
                    actionIndex = 0
                else:
                    actionIndex = 1
                
                pairs.append((currentState.player,currentState.dealer,actionIndex))
                    
                self.N[currentState.dealer-1,currentState.player-1,actionIndex] += 1 
                
                currentState,reward = game.step(currentState,action)
                
                
            self.wins = self.wins + 1 if reward == 1 else self.wins
            
            for player,dealer,action in pairs:
                dealerIndex = dealer-1 #Sum of dealer in state
                playerIndex = player-1 #Sum of player in state
                actionIndex = action #Action taken in state
                
                step = 1.0 / self.N[dealerIndex,playerIndex,actionIndex]
                rwrd = reward - self.Q[dealerIndex,playerIndex,actionIndex]
                self.Q[dealerIndex,playerIndex,actionIndex] += step*rwrd
                
                
        self.iterations += iterations
        
        print('Precentage of wins during training:',float(self.wins/self.iterations*100)) #Prints out precentage of wins during training
            
        for d in range(10):
            for p in range(21):
                self.V[d,p] = max(self.Q[d,p,:])
        
    '''Plays one game where MonteCarlo only looks up in Q table. Similar to when the agent has trained and the epsilon value
       is very low. This function was only used in development'''
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


