def simpleEvaluate(state, role):
    d = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
    heuristicScore = 0
    for key in d:
        heuristicScore += d[key] * (len(state.pieces(key, role)) - len(state.pieces(key, not role)))
    return heuristicScore

def mobilityEvaluate(state, role):
    mobility1 = len(state.legal_moves)
    state.turn = not state.turn
    mobility2 = len(state.legal_moves)
    state.turn = not state.turn
    return mobility1 - mobility2 if state.turn == role else mobility2 - mobility1

def combinedEvaluate(state, role):
    w1 = .5
    w2 = .5
    return .5 * simpleEvaluate(state, role) + .5 * mobilityEvaluate(state, role)