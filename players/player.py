import random
def randomMove(state):
    moves = state.legal_moves
    numMoves = moves.count()
    moveNumber = random.randint(0, numMoves-1)
    for i, move in enumerate(moves):
        if i == moveNumber:
            return move

class player():
    def __init__(self, evaluatefn, role, depth = 1, verbose = False):
        self.evaluatefn = evaluatefn
        self.depth = depth #initial depth for iterative deepening
        self.verbose = verbose
        self.role = role
        self.nodes = 0
    def randomMove(self, state):
        return randomMove(state)

class randomPlayer(player):
    def getMove(self, state, timeLimit):
        return self.randomMove(state)

    def getName(self):
        return "random"

class legalPlayer(player):
    def getMove(self, state, timeLimit):
        moves = state.legal_moves
        for move in moves:
            return move
    def getName(self):
        return "legal"
