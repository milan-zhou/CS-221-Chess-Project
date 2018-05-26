import player
import game
import time

class minimaxPlayer(player.player):
    def maxState(self,state, depth, stopTime):
        self.nodes += 1
        result = game.gameOver(state)
        if result != "*":
            return (None, game.reward(state, result, self.role))
        if not depth:
            return (None, self.evaluatefn(state, self.role))
        moves = state.legal_moves
        bestScore = float("-inf")
        bestMove = None
        for i, move in enumerate(moves):
            if time.time() > stopTime:
                break
            state.push(move)
            testScore = self.minState(state, depth, stopTime)
            if testScore > bestScore:
                bestMove = move
                bestScore = testScore
                if bestScore == 100:
                    state.pop()
                    break
            state.pop()
            
        return (bestMove, bestScore)
            
            
    def minState(self, state, depth, stopTime):
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
            maxMove, maxScore = self.maxState(state, depth - 1, stopTime)
            if maxScore == 100:
                return maxMove
            if maxScore == float("inf"):
                break
            if maxScore < maxScore:
                worstScore = maxScore
                if worstScore == -100:
                    state.pop()
                    break
            state.pop()
        return bestScore
    
    def getMove(self, state, timeLimit):
        stopTime = time.time() + timeLimit
        self.nodes = 0
        depth = self.depth
        bestMove = None
        bestScore = float("-inf")
        while (stopTime > time.time()):
            maxMove, maxScore = self.maxState(state, depth, stopTime)
            if maxScore == 100:
                return maxMove
            if maxScore == float("inf"):
                break
            print(depth, maxMove, maxScore)
            if maxScore > bestScore:
                bestMove = maxMove
                bestScore = maxScore
            depth +=1
        return bestMove if bestMove else self.randomMove(state)

    def getName(self):
        return "minimax"