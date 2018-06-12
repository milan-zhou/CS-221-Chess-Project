import player
import game
import sys
sys.path.append("../python-chess")
from chess.polyglot import zobrist_hash
import random
import time
from collections import OrderedDict, namedtuple

# The normal OrderedDict doesn't update the position of a key in the list,
# when the value is changed.
MATE_UPPER = float("inf")
TABLE_SIZE = 1e8
LOWER_BOUND = -1
UPPER_BOUND = 1
EXACT_BOUND = 0
Entry = namedtuple('Entry', 'lower upper')
class LRUCache:
    '''Store items in the order the keys were last added'''
    def __init__(self, size):
        self.d = {}
        self.size = size
        self.hits = 0
        self.notHit = 0

    def get(self, key, default=None):
        if key in self.d:
            self.hits += 1
        else:
            self.notHit += 1
        return self.d.get(key, default)

    def __setitem__(self, key, value):
        self.d[key] = value

    def clear(self):
        self.d.clear()
        self.hits = 0
        self.notHit = 0

class mtdPlayer(player.player):
    def __init__(self, evaluatefn, role):
        self.tp_score = LRUCache(TABLE_SIZE)
        self.tp_move = LRUCache(TABLE_SIZE)
        
        self.nodes = 0
        self.evaluatefn = evaluatefn
        self.role = role

    def moves(self, state, lm = None, killer = None):
        if lm:
            yield lm
        if killer:
            yield killer
        # for move in sorted(state.legal_moves, key= lambda x: self.evalHelper(state, x), reverse=isMax):
        for move in state.legal_moves:
            yield move

    def alphaBetaWithMemory(self, state, alpha, beta, depth, isMax, stopTime, lm=None, root=False):
        self.nodes += 1
        
        zhash = zobrist_hash(state)
        entry = self.tp_score.get((zhash, depth, root))
        if entry and (not root or self.tp_move.get(zhash)):
            if entry.lower >= beta:
                return entry.lower
            if entry.upper <= alpha:
                return entry.upper
            
            alpha = max(alpha, entry.lower)
            beta = min(beta, entry.upper)
            
        result = game.gameOver(state)
        if result != "*":
            g = game.reward(state, result, self.role)
        elif depth == 0:
            g = self.evaluatefn(state, self.role)
        elif isMax:
            g = float("-inf")
            a = alpha 
            for move in self.moves(state, lm, self.tp_move.get(zhash)):
                if time.time() > stopTime:
                    break

                state.push(move)
                score = self.alphaBetaWithMemory(state, a, beta, depth-1, not isMax, stopTime)
                state.pop()
            
                if time.time() > stopTime:
                    break
                
                g = max(score, g)
                a = max(a,g)
                    
                if g >= beta:
                    self.tp_move[zhash] = move
                    break
        else:
            g = float("inf")
            b = beta
            for move in self.moves(state, lm, self.tp_move.get(zhash)):
                if time.time() > stopTime:
                    break

                state.push(move)
                score = self.alphaBetaWithMemory(state, alpha, b, depth - 1, not isMax, stopTime)
                state.pop()

                if time.time() > stopTime:
                    break
                    

                g = min(score, g)
                b = min(b, g)

                #Killer
                if g <= alpha:
                    self.tp_move[zhash] = move
                    break
        
        if time.time() < stopTime:
            if g <= alpha:
                self.tp_score[(zhash, depth, root)] = Entry(entry.lower if entry else float("-inf"), g)
            elif g > alpha and g < beta:
                self.tp_score[(zhash, depth, root)] = Entry(g, g)
            elif g >= beta:
                self.tp_score[(zhash, depth, root)] = Entry(g, entry.upper if entry else float("inf"))

        return g

    def _mtd(self, state, maxDepth, firstGuess, stopTime, lm=None):
        g = firstGuess
        upperBound = float("inf")
        lowerBound = float("-inf")
        bestMove = lm
        zhash = zobrist_hash(state)
        while lowerBound < upperBound:
            if time.time() > stopTime:
                break
            if g == lowerBound:
                beta = g+1
            else:
                beta = g
            g = self.alphaBetaWithMemory(state, beta - 1, beta, maxDepth, True, stopTime, lm = bestMove, root = True)

            if g < beta:
                upperBound = g
            else:
                lowerBound = g
            bestMove = self.tp_move.get(zhash)
            
        return bestMove, g

	#MTDf
    def getMove(self, state, timeLimit):
        self.tp_score.clear()
        self.tp_move.clear()
        self.nodes = 0
        start = time.time()
        guess = 0
        depth = 0
        stopTime = start + timeLimit
        bestMove = None
        
        while (time.time() < stopTime):
            depth +=1
            bestMove, guess = self._mtd(state, depth, guess, stopTime, lm=bestMove)
            print (depth, bestMove, guess)
        return bestMove if bestMove else self.randomMove(state)

    def getName(self):
        return "mtd"