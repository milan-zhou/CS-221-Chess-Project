import sys
sys.path.extend(["../players", "../python-chess", ".."])

import player
import game
import random
import time

class minimaxPlayer(player.player):
    def moves(self,state, lm = None):
        if lm:
            yield lm
        for move in state.legal_moves:
            yield move

    def maxState(self, state, depth, stopTime, lm = None):
        self.nodes += 1
        result = game.gameOver(state)
        if result != "*":
            return (None, game.reward(state, result, self.role))
        if not depth:
            return (None, self.evaluatefn(state, self.role))

        bestMove = lm
        bestScore = float("-inf")
        
        for move in self.moves(state, lm):
            if time.time() > stopTime:
                break
            state.push(move)
            minScore = self.minState(state, depth - 1, stopTime)
            state.pop()
            if time.time() > stopTime:
                break
            if minScore > bestScore:
                bestMove = move
                bestScore = minScore
            
        return (bestMove, bestScore)
            
            
    def minState(self, state, depth, stopTime):
        self.nodes += 1
        result = game.gameOver(state)
        
        if result != "*":
            return game.reward(state, result, self.role)
        if not depth:
            return self.evaluatefn(state, self.role)
            
        moves = state.legal_moves
        bestScore = float("inf")
        for i, move in enumerate(moves):
            if time.time() > stopTime:
                break
            state.push(move)
            maxMove, maxScore = self.maxState(state, depth - 1, stopTime)
            state.pop()
            if time.time() > stopTime:
                break
            if maxScore < bestScore:
                bestScore = maxScore
        
        return bestScore
    
    def getMove(self, state, timeLimit):
        stopTime = time.time() + timeLimit
        self.nodes = 0
        depth = 1
        bestMove = None
        while (stopTime > time.time()):
            bestMove, bestScore = self.maxState(state, depth, stopTime, lm = bestMove)
            print(depth, bestMove, bestScore)
            depth +=1
            
        return bestMove if bestMove else self.randomMove(state)
    
    def getName(self):
        return "minimax"