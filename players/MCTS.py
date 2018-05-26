import player
import game
import random
import time
import UCT

class MCTSPlayer(player.player):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def getMove(self, state, timeLimit):
        self.nodes = 0
        stopTime = time.time() + timeLimit
        bestMove, total = UCT.UCT(state,stopTime)
        self.nodes = total + 1
        if (self.verbose):
            print(self.nodes)
        return bestMove if bestMove else self.randomMove(state)
        
    def getName(self):
        return "MCTS"