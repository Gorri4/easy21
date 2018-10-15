# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:25:49 2018

@author: gop4
"""
import random
import numpy as np
from Game import Game
from State import State

class SARSA:
    def __init__(self,n0,lambdaValue):
        self.n0 = float(n0)
        self.lambdaValue = lambdaValue
        
        self.N = np.zeros((10,21,2))
        self.Q = np.zeros((10,21,2))
        self.V = np.zeros((10,21))
        self.E = np.zeros((10,21,2))
        
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
    
    
    def train(self,iterations):

        for rounds in range(iterations):

            game = Game() 
            
            self.E = np.zeros((10,21,2))
            
            state = State(game.dealerTakeFirstTurn(), game.playerTakeFirstTurn(),False)
             
            action = self.epsilonGreedy(state)
                        
            if(action == 'hit'):
                    actionIndex = 0
            else:
                    actionIndex = 1
             
            nextAction = action
            
             
            while not state.finished:
                
                if(action == 'hit'):
                    actionIndex = 0
                else:
                    actionIndex = 1
                
                self.N[state.dealer-1,state.player-1,actionIndex] += 1

                nextState, reward = game.step(state,action)
                
                #print(nextState.player)
                q = self.Q[state.dealer-1,state.player-1,actionIndex]


                if not nextState.finished:
                    nextAction = self.epsilonGreedy(nextState)
                    
                    if(nextAction == 'hit'):
                        nextActionIndex = 0
                    else:
                        nextActionIndex = 1
                        

                    nextQ = self.Q[nextState.dealer-1,nextState.player-1,nextActionIndex]
                    delta = reward + nextQ - q
                else:
                    delta = reward - q
                
                self.E[state.dealer-1,state.player-1, actionIndex] += 1
                
                
                alpha = 1.0 / (self.N[state.dealer-1,state.player-1,actionIndex])

                    
                update = alpha * delta * self.E
                #print(alpha)
                self.Q += update
                
                self.E *= self.lambdaValue
                
                state = nextState
                action = nextAction
                
            if(reward == 1):
                self.wins = self.wins + 1
            else:
                self.wins = self.wins
                
                
        self.iterations += iterations
        
        for d in range(10):
            for p in range(21):
                self.V[d,p] = max(self.Q[d,p,:])


    def plotImage(self, b):
        X = np.arange(0, 10, 1)
        Y = np.arange(0, 21, 1)
        X, Y = np.meshgrid(X, Y)
        Z = self.V[X,Y]
        yfrb = b.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.Spectral, linewidth=0, antialiased=False)
        return yfrb
                
                
sarsa = SARSA(100,0.9)
for i in range(10):
    sarsa.train(50000)