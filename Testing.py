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
    fig.savefig('lambdaALL.png')
    plt.show()

def drawForLambdaOne():
    montecarlo = MonteCarlo(100)
    print('Training Monte Carlo')
    montecarlo.train(500000)
    print('Training of Monte Carlo Completed')
    lambdaValue = 1.0
    learningRate = []
    learningRateIndex = []
    print('Training SARSA and plotting graph')
    sarsa = SARSA(100,lambdaValue)
    for i in range(1000):
        learningRateIndex.append(i)
        sarsa.train(1)
        squareMean = np.sum(np.square(sarsa.Q-montecarlo.Q))/float(1000)
        learningRate.append(squareMean)
        
    fig = plt.figure("SARSAZERO")
    surf = plt.plot(learningRateIndex,learningRate)
    fig.savefig('lambdaOne.png')
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
    print('Training SARSA and plotting graph')
    for i in range(1000):
        learningRateIndex.append(i)
        sarsa.train(1)
        squareMean = np.sum(np.square(sarsa.Q-montecarlo.Q))/float(1000)
        learningRate.append(squareMean)
        
    fig = plt.figure("SARSAZERO")
    surf = plt.plot(learningRateIndex,learningRate)
    fig.savefig('lambdaZero.png')
    plt.show()
    
def plotMonte(b, monti):
    b.clear()
    X = np.arange(0, 10, 1)
    Y = np.arange(0, 21, 1)
    X, Y = np.meshgrid(X, Y)
    Z = monti.V[X,Y]
    yfrb = b.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.PuOr, linewidth=0, antialiased=False)
    return yfrb

def drawMonteCarlo():
    iterations = [10, 100, 1000, 10000, 100000, 500000,1000000]
    for iteration in iterations:
        print('Creating Monte Carlo Agent...')
        monti = MonteCarlo(100)
        print('Monte Carlo created')
        print('Training Monte Carlo for', iteration, 'iterations.')
        monti.train(iteration)
        print('Training completed, plotting image')
        figure = plt.figure('Monte'+str(iteration))
        b = figure.add_subplot(111, projection='3d')
        resultfig = plotMonte(b, monti)
        figure.savefig('MonteCarlo'+ str(iteration) + '.png')
        plt.show()
        
def run():
    print("Solution for Question 1 (Monte Carlo Optimal Value Function")
    drawMonteCarlo()
    print('Solution for Question 2 (Report mean-squared error for different lambdas)')
    drawForAllLambdas()
    print('Solution for Question 3 (Plot the learning curve of mean-squared error against episode number for lambda=1 and lambda=0.')
    print('Lambda=1')
    drawForLambdaOne()
    print('Lambda=0')
    drawForLambdaZero()
    
run()