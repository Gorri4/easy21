import random
from State import State
import copy

class Game:
    dealerSum = 0
    playerSum = 0
    firstRoundDealer = True
    firstRoundPlayer = True
    isStillPlayingDealer = True
    isStillPlayingPlayer = True


    '''Dealer plays until he decides to stick or goes over 21 or under 1. Returns the result from checkResult()'''
    def dealerPlay(self):
        global dealerSum
        global isStillPlayingDealer
        while(self.isStillPlayingDealer):
            #print('dealer sum: ', self.dealerSum)
            if(self.didBreak(self.dealerSum)):
                #print('Dealer Broke!')
                self.isStillPlayingDealer = False
                break;
            else:
                if(self.dealerSum > 16):
                    self.dealerSum = self.takeTurn('dealer', 'stick', self.dealerSum)
                else:
                    self.dealerSum = self.takeTurn('dealer', 'hit', self.dealerSum)
        return self.checkResult()
        
    '''Players call this function to take turns. They send in their sum and their next action and it returns
       their new sum'''
    def takeTurn(self, player, action, orgSum):
        result = 0
        if(action == 'hit'):
            newCard = self.dealCard(False)
            if(newCard[0] == 'black'):
                result = orgSum + newCard[1]
                #print(player,' hits black',newCard[1])
            else:
                result = orgSum - newCard[1]
                #print(player,' hits red',newCard[1])
        else:
             if(player == 'dealer'):
                 #print('dealer sticks')
                 result = orgSum
                 self.isStillPlayingDealer = False
             else:
                 #print('player sticks')
                 result = orgSum
                 self.isStillPlayingPlayer = False
        return result
        
    '''Returns one card from 1-10 either black or red. If isFirstRound==true the function always returns a black card'''
    def dealCard(self,isFirstRound):
        randNumber = random.randint(1, 10)
        if(isFirstRound):
            color = 'black'
        else:
            randColor = random.randint(0, 2)
            if(randColor > 0):
                color = 'black'
            else:
                color = 'red'
        return color,randNumber
    
    '''Handles the dealers first turn'''
    def dealerTakeFirstTurn(self):
            global dealerSum
            firstCard = self.dealCard(True)
            self.dealerSum = firstCard[1]
            #print('Dealer first car: ', self.dealerSum)
            return self.dealerSum
    
    '''Handles the players first turn'''
    def playerTakeFirstTurn(self):
            global playerSum
            firstCard = self.dealCard(True)
            self.playerSum = firstCard[1]
            #print('Player first car: ', self.playerSum)
            return self.playerSum
            
    '''Checks if player did break'''    
    def didBreak(self,sum):
        if(sum > 21 or sum < 1):
            return True
        else:
            return False
        
    '''Checks which player won'''
    def checkResult(self):
        if(self.dealerSum > 21):
            #print('Player won')
            return 'player'
        elif(self.dealerSum > self.playerSum):
            #print('Dealer won')
            return 'dealer'
        else:
            #print('Player won')
            return 'player'
            
    '''Plays one game without Monte Carlo player. This function was only used in development'''
    def playOneGame(self):
        self.dealerTakeFirstTurn()
        self.playerTakeFirstTurn()
        global dealerSum
        global playerSum
        currentState = State(self.dealerSum,self.playerSum,False)
        n=1
        while(not currentState.finished):
            if(currentState.player < 17):
                currentState,reward = self.step(currentState,'hit')
            else:
                currentState,reward = self.step(currentState,'stick')
            n = n + 1
        return reward       
    
    '''Step function takes in players current state and action and returns new state and new reward.
       If player won then the reward is 1, the reward is -1 if he looses but 0 if neither player won'''
    def step(self, state, action):
        nextState = copy.deepcopy(state)
        reward = 0
        if(action == 'hit'):
            result = self.takeTurn('player',action,nextState.player)
            if(result > 21 or result < 1):
                nextState.finished = True
                reward = -1
            else:
                nextState.player = result
        else:
            self.playerSum = nextState.player
            self.dealerSum = nextState.dealer
            result = self.dealerPlay() #Dealer plays 
            nextState.finished = True
            if(result == 'dealer'):
                reward = -1
            else:
                reward = 1
    
        return nextState,reward