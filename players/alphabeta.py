import player
import game
import random
import time
class alphabetaPlayer(player.player):
    def maxState(self, state, alpha, beta, depth, stopTime):
        self.nodes += 1
        result = game.gameOver(state)
        if result != "*":
            return (None, game.reward(state, result, self.role))
        if not depth:
            return (None, self.evaluatefn(state, self.role))
        moves = state.legal_moves
        bestMove = None
        bestScore = float("-inf")
        for i, move in enumerate(moves):
            if time.time() > stopTime:
                break
            state.push(move)
            minScore = self.minState(state, alpha, beta, depth, stopTime)
            state.pop()
            if minScore == float("inf"):
                break
            if minScore > bestScore:
                bestMove = move
                bestScore = minScore
            alpha = max(alpha, minScore)
            if beta <= alpha:
                break
            
        return (bestMove, bestScore)
            
            
    def minState(self, state, alpha, beta, depth, stopTime):
        self.nodes += 1
        result = game.gameOver(state)
        if result != "*":
            return game.reward(state, result, self.role)
            
        moves = state.legal_moves
        bestScore = float("inf")
        for i, move in enumerate(moves):
            if time.time() > stopTime:
                break
            state.push(move)
            maxMove, maxScore = self.maxState(state, alpha, beta, depth - 1, stopTime)
            state.pop()
            if maxScore == float("-inf"):
                break
            if maxScore < bestScore:
                bestScore = maxScore
            beta = min(maxScore, beta)
            if beta <= alpha:
                break
        return bestScore
    
    def getMove(self, state, timeLimit):
        stopTime = time.time() + timeLimit
        self.nodes = 0
        depth = self.depth
        alpha = -100
        beta = 100
        bestMove = None
        bestScore = float("-inf")
        while (stopTime > time.time()):
            maxMove, maxScore = self.maxState(state, -100, 100, depth, stopTime)
            if maxScore == 100:
                return maxMove
            if self.verbose:
                print(depth, maxMove, maxScore)
            if maxScore == float("inf"):
                break
                
            if maxScore > bestScore:
                bestMove = maxMove
                bestScore = maxScore
            depth +=1
        return bestMove if bestMove else self.randomMove(state)
    
    def getName(self):
        return "alphabeta"