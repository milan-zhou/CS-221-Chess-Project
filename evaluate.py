import sys
sys.path.append('../python-chess')
import numpy as np
import chess
import chess.uci

d = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
def simpleEvaluate(state, role):
    heuristicScore = 0
    for key in d:
        heuristicScore += d[key] * (len(state.pieces(key, role)) - len(state.pieces(key, not role)))
    return heuristicScore

def mobilityEvaluate(state, role):
    mobility1 = state.legal_moves.count()
    state.turn = not state.turn
    mobility2 = state.legal_moves.count()
    state.turn = not state.turn
    return mobility1 - mobility2 if state.turn == role else mobility2 - mobility1


def getNeighborFiles(file):
    if file == chess.BB_FILES[0]:
        nFile = file << 1
    elif file == chess.BB_FILES[7]:
        nFile = file >> 1
    else:
        nFile = (file << 1) | (file >> 1)
    return nFile
        
def pawnEvaluate(state, role):
    wPawns = state.pawns & state.occupied_co[True]
    bPawns = state.pawns & state.occupied_co[False]
    
    wDoubled = wIsolated = wBlocked = 0
    bDoubled = bIsolated = bBlocked = 0
    for from_square in chess.scan_reversed(wPawns):
        file = chess.BB_FILES[chess.square_file(from_square)]
        
        wPawnsOnFile = file & wPawns
        if (wPawnsOnFile & (wPawnsOnFile-1)):
            wDoubled +=1
        if getNeighborFiles(file) & wPawns == 0:
            wIsolated += 1
        if not any(chess.scan_reversed(chess.BB_PAWN_ATTACKS[True][from_square] & state.occupied_co[False])) and state.occupied & chess.BB_SQUARES[from_square + 8]:
            wBlocked +=1
        
    for from_square in chess.scan_reversed(bPawns):
        file = chess.BB_FILES[chess.square_file(from_square)]
        bPawnsOnFile = file & bPawns
        if(bPawnsOnFile & (bPawnsOnFile-1)):
            bDoubled +=1
        if getNeighborFiles(file) & bPawns == 0:
            bIsolated += 1
            
        if not any(chess.scan_reversed(chess.BB_PAWN_ATTACKS[False][from_square] & state.occupied_co[True])) and state.occupied & chess.BB_SQUARES[from_square - 8]:
            bBlocked +=1
            
    score = bDoubled + bIsolated + bBlocked - wDoubled - wIsolated - wBlocked
    if (not role):
        score = -score
    return score
    

def combinedEvaluate(state, role):
    return simpleEvaluate(state, role) + .1 * mobilityEvaluate(state, role) + .25 *pawnEvaluate(state,role)

handler = chess.uci.InfoHandler()
engine = chess.uci.popen_engine("stockfish")
engine.info_handlers.append(handler)

def stockFishEvaluate(state,role):
    engine.position(state)
    move = engine.go(movetime=0)[0]  # Gets a tuple of bestmove and ponder move
    score = handler.info["score"][1][0]
    if not score:
        return 0
    if role != state.turn:
        score = -score
    return score