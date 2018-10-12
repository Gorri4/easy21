from State import *
from Game import *

class MonteCarlo:
    numGamesWonPlayer = 0
    numGamesWonDealer = 0
    
    for i in range(0,100):
        game = Game()
        result = game.playOneGame()
        if(result == 1):
            numGamesWonPlayer += 1
            numGamesWonDealer -= 1
        else:
            numGamesWonPlayer -= 1
            numGamesWonDealer += 1
    
    print('Player reward: ',numGamesWonPlayer)
    print('Dealer reward: ',numGamesWonDealer)
    