# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:23:18 2018

@author: gop4
"""

from State import State
from Game import Game
from MonteCarlo import MonteCarlo
from SARSA import SARSA

import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def drawForAllLambdas():
    montecarlo = MonteCarlo(100)
    print('Training Monte Carlo')
    montecarlo.train(500000)
    print('Training of Monte Carlo Completed')
    lambdas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    squareMean = []
    numberElements = montecarlo.Q.shape[0]*montecarlo.Q.shape[1]*2
    for lambdaValue in lambdas:
        sarsa = SARSA(100, lambdaValue)
        print('Training SARSA',lambdaValue)
        sarsa.train(1000)
        print('Training of SARSA Completed')
        squareMeanCalc = np.sum(np.square(sarsa.Q-montecarlo.Q))/float(numberElements)
        squareMean.append(squareMeanCalc)   
    fig = plt.figure("SARSA")
    surf = plt.plot(lambdas[1:10], squareMean[1:10])
    plt.show()

def drawForLambdaOne():
    montecarlo = MonteCarlo(100)
    print('Training Monte Carlo')
    montecarlo.train(500000)
    print('Training of Monte Carlo Completed')
    lambdaValue = 1.0
    learningRate = []
    learningRateIndex = []
    
    sarsa = SARSA(100,lambdaValue)
    for i in range(1000):
        learningRateIndex.append(i)
        sarsa.train(1)
        squareMean = np.sum(np.square(sarsa.Q-montecarlo.Q))/float(1000)
        learningRate.append(squareMean)
        
    fig = plt.figure("SARSAZERO")
    surf = plt.plot(learningRateIndex,learningRate)
    plt.show()

def drawForLambdaZero():
    montecarlo = MonteCarlo(100)
    print('Training Monte Carlo')
    montecarlo.train(500000)
    print('Training of Monte Carlo Completed')
    lambdaValue = 0
    learningRate = []
    learningRateIndex = []
    
    sarsa = SARSA(100,lambdaValue)
    for i in range(1000):
        learningRateIndex.append(i)
        sarsa.train(1)
        squareMean = np.sum(np.square(sarsa.Q-montecarlo.Q))/float(1000)
        learningRate.append(squareMean)
        
    fig = plt.figure("SARSAZERO")
    surf = plt.plot(learningRateIndex,learningRate)
    plt.show()

drawForLambdaZero()
drawForLambdaOne()