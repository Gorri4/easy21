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
    
    def dealerTakeFirstTurn(self):
            global dealerSum
            firstCard = self.dealCard(True)
            self.dealerSum = firstCard[1]
            #print('Dealer first car: ', self.dealerSum)
            return self.dealerSum
            
    def playerTakeFirstTurn(self):
            global playerSum
            firstCard = self.dealCard(True)
            self.playerSum = firstCard[1]
            #print('Player first car: ', self.playerSum)
            return self.playerSum
            
    def didBreak(self,sum):
        if(sum > 21 or sum < 1):
            return True
        else:
            return False
        
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
            
        
    def playOneGame(self):
        self.dealerTakeFirstTurn()
        self.playerTakeFirstTurn()
        global dealerSum
        global playerSum
        currentState = State(self.dealerSum,self.playerSum,False)
        n=1
        while(not currentState.finished):
            #print('Skref nr.', n)
            #print('dealer',currentState.dealer)
            #print('player',currentState.player)
            if(currentState.player < 17):
                currentState,reward = self.step(currentState,'hit')
            else:
                currentState,reward = self.step(currentState,'stick')
            n = n + 1
        return reward       
    
    def step(self, state, action):
        nextState = copy.deepcopy(state)
        #print('Before-->player:',nextState.player,' dealer:',nextState.dealer)
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
            result = self.dealerPlay()
            nextState.finished = True
            if(result == 'dealer'):
                reward = -1
            else:
                reward = 1
    
        #print('After-->player:',nextState.player,' dealer:',nextState.dealer)
        return nextState,reward