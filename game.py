def gameOver(state):
    return state.result(True) #Check if game over, including by claim draw

def reward(state, result, role):
    if result == "1-0":
        r = 10000
    elif result == "0-1":
        r = -10000
    else:
        r = 0
    if not role:
        r = -r
    return r 