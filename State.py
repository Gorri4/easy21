class State:
    def __init__(self, dealerCard, playerCard, isGameFinished=False):
        self.dealer = dealerCard
        self.player = playerCard
        self.finished = isGameFinished