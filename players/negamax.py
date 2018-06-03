import player
import game
import random
import time
class negamaxPlayer(player.player):
    def negamax(self, state, alpha, beta, depth, role, stopTime):
        self.nodes += 1
        result = game.gameOver(state)
        if result != "*":
            return (None, game.reward(state, result, role))
        if not depth:
            return (None, self.evaluatefn(state, role))
        moves = state.legal_moves
        bestMove = None
        bestScore = float("-inf")
        for i, move in enumerate(moves):
            if time.time() > stopTime:
                break
            state.push(move)
            testMove, v = self.negamax(state, -beta, -alpha, depth-1, not role, stopTime)
            state.pop()
            if v == float("-inf"):
                break
            v = -v
            if v > bestScore:
                bestMove = move
                bestScore = v
            alpha = max(alpha, v)
            if beta <= alpha:
                break
            
        return (bestMove, bestScore)
            
    def getMove(self, state, timeLimit):
        stopTime = time.time() + timeLimit
        self.nodes = 0
        self.depth = 2
        depth = self.depth
        alpha = -100
        beta = 100
        bestMove = None
        bestScore = float("-inf")
        while (stopTime > time.time()):
            maxMove, maxScore = self.negamax(state, -100, 100, depth, self.role, stopTime)
            if maxScore == 100:
                return maxMove
            if maxScore == float("inf"):
                break
                
            if maxScore > bestScore:
                bestMove = maxMove
                bestScore = maxScore
            depth += 2
        return bestMove if bestMove else self.randomMove(state)
    
    def getName(self):
        return "negamax"