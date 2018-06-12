import player
import sys
import game
import random
import time
import UCT

class MCTSPlayer(player.player):

    def getMove(self, state, timeLimit):
        self.nodes = 0
        stopTime = time.time() + timeLimit
        bestMove, total = UCT.UCT(state,stopTime, self.evaluatefn)
        self.nodes = total + 1
        if (self.verbose):
            print(self.nodes)
        return bestMove if bestMove else self.randomMove(state)
        
    def getName(self):
        return "MCTS"