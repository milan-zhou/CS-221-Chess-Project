def simpleEvaluate(state, role):
    d = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
    heuristicScore = 0
    for key in d:
        heuristicScore += d[key] * (len(state.pieces(key, role)) - len(state.pieces(key, not role)))
    return heuristicScore