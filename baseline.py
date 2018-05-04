def valueHeuristic(state, result = None, role = None):
    d = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
    heuristicScore = 0
    for i in range(1, 6):
        heuristicScore += d[i] * (len(state.pieces(i, True)) - len(state.pieces(i, False)))
    if (state.is_check()):
        heuristicScore += .5
    if not state.turn:
        heuristicScore = -heuristicScore
    return heuristicScore

class player():
    def __init__(self, depth = 1, heuristic = simpleHeuristic, verbose = False):
        self.depth = depth
        self.heuristic = heuristic
        self.verbose = verbose

class minimaxPlayer(player):
    def maxScore(self,state, depth):
        result = gameOver(state)
        if result != "*":
            return (None, reward(state, result, state.turn))
        if not depth:
            return (None, self.heuristic(state))
        moves = state.legal_moves
        bestScore = float("-inf")
        for i, move in enumerate(moves):
            state.push(move)
            testScore = self.minScore(state, depth)
            if testScore > bestScore:
                bestMove = move
                bestScore = testScore
                if bestScore == 100:
                    state.pop()
                    break
            state.pop()
            
        return (bestMove, bestScore)

        def minScore(self, state, depth):
        result = gameOver(state)
        if result != "*":
            return reward(state, result, state.turn)
            
        moves = state.legal_moves
        worstScore = float("inf")
        for i, move in enumerate(moves):
            state.push(move)
            testMove, testScore = self.maxScore(state, depth - 1)
            if testScore < worstScore:
                worstScore = testScore
                if worstScore == -100:
                    state.pop()
                    break
            state.pop()
        return worstScore
    
    def getMove(self, state):
        bestMove, bestScore = self.maxScore(state, self.depth)
        return bestMove

return minimaxPlayer(heuristic = valueHeuristic)