# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:33:27 2018

@author: gop4
"""

class State:
    def __init__(self, dealerCard, playerCard, isGameFinished=False):
        self.dealer = dealerCard
        self.player = playerCard
        self.finished = isGameFinished