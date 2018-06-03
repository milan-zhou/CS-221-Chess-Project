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

Entry = namedtuple('Entry', 'lower upper best')
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

class mtdExtendedPlayer(player.player):
    def __init__(self, evaluatefn, role):
        self.tp_score = LRUCache(TABLE_SIZE)
        self.tp_move = LRUCache(TABLE_SIZE)
        self.nodes = 0
        self.evaluatefn = evaluatefn
        self.role = role

    def evalHelper(self, state, move):
        state.push(move)
        v = self.evaluatefn(state, self.role)
        state.pop()
        return v

    def sortedMoves(self, state, isMax):
        killer = self.tp_move.get(state)
        if killer:
            yield killer

        for m in sorted(state.legal_moves, key = lambda m: self.evalHelper(state, m), reverse = isMax):
            yield m

    def alphaBetaWithMemory(self, state, alpha, beta, depth, isMax, stopTime, root=True):
        self.nodes += 1
        
        zhash = zobrist_hash(state)
        entry = self.tp_score.get((zhash, depth, root), Entry(float("-inf"), float("inf"), None))
        if entry.lower >= beta and (not root or entry.best):
            return entry.best, entry.lower
        if entry.upper <= alpha and entry.best:
            return entry.best, entry.upper
    
        bestMove = None
        result = game.gameOver(state)
        if result != "*":
            g = game.reward(state, result, self.role)
        elif depth == 0:
            g = self.evaluatefn(state, state.turn)

        elif isMax:
            g = float("-inf")   
            a = alpha 
            

            for move in self.sortedMoves(state, isMax):
                if time.time() > stopTime:
                    break

                state.push(move)
                minMove, score = self.alphaBetaWithMemory(state, a, beta, depth-1, not isMax, stopTime, root = False)
                state.pop()
            
                if time.time() > stopTime:
                    break
                
                if score > g:
                    g = score
                    bestMove = move
                    self.tp_move[state] = move
                    
                a = max(a,g)
                    
                if g >= beta:
                    break
        else:
            g = float("inf")
            b = beta
            for move in self.sortedMoves(state, isMax):
                if time.time() > stopTime:
                    break

                state.push(move)
                maxMove, score = self.alphaBetaWithMemory(state, alpha, b, depth - 1, not isMax, stopTime, root = False)
                state.pop()

                if time.time() > stopTime:
                    break
                    
                    
                if score < g:
                    g =  score
                    self.tp_move[state] = move
                    
                b = min(b, g)

                if g <= alpha:
                    break
        
        if time.time() > stopTime:
            return bestMove, g

        if g <= alpha:
            self.tp_score[(zhash, depth, root)] = Entry(entry.lower, g, bestMove)
        elif g > alpha and g < beta:
            self.tp_score[(zhash, depth, root)] = Entry(g, g, bestMove)
        elif g >= beta:
            self.tp_score[(zhash, depth, root)] = Entry(g, entry.upper, bestMove)

        return bestMove, g

    def _mtd(self, state, maxDepth, firstGuess, stopTime):
        g = firstGuess
        upperBound = float("inf")
        lowerBound = float("-inf")
        while lowerBound < upperBound:
            if time.time() > stopTime:
                break
            if g == lowerBound:
                beta = g+1
            else:
                beta = g
            move, g = self.alphaBetaWithMemory(state, beta - 1, beta, maxDepth, True, stopTime, root=True)

            if g < beta:
                upperBound = g
            else:
                lowerBound = g
        return move, g

	#MTDf
    def getMove(self, state, timeLimit):
        self.nodes = 0
        start = time.time()
        guess = 0
        depth = 0
        stopTime = start + timeLimit
        zhash = zobrist_hash(state)

        bestScore = float("-inf")
        bestMove = None
        while (time.time() < stopTime):
            depth +=2
            move, guess = self._mtd(state, depth, guess, stopTime)
            print(depth, move, guess)

            if guess > bestScore:
                bestMove = move
                bestScore = guess


        self.tp_score.clear()
        self.tp_move.clear()

        return bestMove if bestMove else self.randomMove(state)

    def getName(self):
        return "mtd_extended"