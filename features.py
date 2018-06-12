#Adapted from Neural Chess

import chess
import chess.pgn
import numpy as np
import random
import itertools
import csv
import time

d = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
def getGlobalFeatures(state):
    # Board representations to help build the feature
    feature = np.zeros(37)
    i = 0

    # Turn - 1 value
    feature[i] = int(state.turn)
    i += 1

    # Castling rights - 4 values
    feature[i] = int(state.has_queenside_castling_rights(True))
    i += 1
    feature[i] = int(state.has_kingside_castling_rights(True))
    i += 1
    feature[i] = int(state.has_queenside_castling_rights(False))
    i += 1
    feature[i] = int(state.has_kingside_castling_rights(False))
    i += 1

    # Piece counts for both sides - 32 values
    for k in d:
        feature[i] = state.pieces(k, True)
        i += 1
        feature[i] = state.pieces(k, False)
        i += 1

    return feature


# Piece information to help build the features
pieces = {'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'p': 8}
pieceValues = {'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 25, 'p': 1}
rookMovement = [np.array([0, 1]), np.array([1, 0]), np.array([-1, 0]), np.array([0, -1])]
bishopMovement = [np.array([1, 1]), np.array([-1, 1]), np.array([1, -1]), np.array([-1, -1])]
sliding = {'r': rookMovement, 'b': bishopMovement, 'q': rookMovement + bishopMovement}


# Build a simple array to represent a board from a fen position
def buildBoardArray(fen):
    boardArray = np.chararray((8, 8))
    boardArray[:] = '-'
    i = 0
    j = 0
    for c in fen:
        if c.isalpha():
            boardArray[i, j] = c
            j += 1
        elif c.isdigit():
            j += int(c)
        elif c == '/':
            j = 0
            i += 1
        elif c == ' ':
            break
    return boardArray


# Get how far a sliding piece can move in each direction
def getPieceMobility(boardArray, index, p):
    feature = np.zeros(len(sliding[p.lower()]))
    i = 0

    # Calculate mobility in each dir
    for dir in sliding[p.lower()]:
        count = 0
        while True:
            nextIndex = index + (count + 1) * dir
            if np.any(nextIndex < 0) \
                    or np.any(nextIndex >= 8) \
                    or boardArray[nextIndex[0], nextIndex[1]] != '-':
                break
            count += 1
        # Add the mobility
        feature[i] = count / float(8)
        i += 1

    return feature

# Get the value of the lowest valued attacker and defender of the square depending on the
# color if specified, or the piece color on the sqIndex
def getLowestAttackerDefender(board, sqIndex, color=None):
    sqUci = chr(sqIndex[1] + ord('a')) + str(8 - sqIndex[0])
    sqID = chess.Move.from_uci(sqUci + 'a1').from_square
    color = color if color is not None else board.piece_at(sqID).color

    # Get the lowest valued attacker and defender
    lowAtt = 100
    lowDef = 100
    for attSq in board.attackers(not color, sqID):
        piece = board.piece_at(attSq)
        lowAtt = min(pieceValues[piece.symbol().lower()], lowAtt)
    for defSq in board.attackers(color, sqID):
        piece = board.piece_at(defSq)
        lowDef = min(pieceValues[piece.symbol().lower()], lowDef)

    # Make 0 no att/def, 0.04 king att/def, .., 1 pawn att/def
    lowAtt = 0 if lowAtt == 100 else 1.0 / lowAtt
    lowDef = 0 if lowDef == 100 else 1.0 / lowDef

    return lowAtt, lowDef


# Get features of the board relating to  pieces
def getPieceCentricFeatures(board):
    # Board representations to help build the feature
    fen = board.fen()
    boardArray = buildBoardArray(fen)
    feature = np.zeros(208)
    i = 0

    # Info for each pieces
    # 5 for each of the 32 pieces (exists, x and y position, and attkr and defndr) - 160
    # 4 for each of the 8 rooks and bishops mobility - 32
    # 8 for each of the 2 queens mobility - 16
    # 208 features total
    for piece, c in pieces.iteritems():
        for p in (piece.lower(), piece.upper()):
            # Get a list of indices of each piece of type p
            indices = np.argwhere(boardArray == p)
            # For each of the piece type
            for n in xrange(c):
                # Exists
                exists = len(indices) > n
                feature[i] = int(exists)
                i += 1

                # Position
                feature[i] = 0 if not exists else indices[n][0] / float(8)
                i += 1
                feature[i] = 0 if not exists else indices[n][1] / float(8)
                i += 1

                # Attacker and defender
                if exists:
                    attacker, defender = getLowestAttackerDefender(board, indices[n])
                    feature[i] = attacker
                    i += 1
                    feature[i] = defender
                    i += 1
                else:
                    feature[i] = 0
                    i += 1
                    feature[i] = 0
                    i += 1

                # Mobility
                if p.lower() in sliding:
                    feature[i:i+len(sliding[p.lower()])] = 0 if not exists else \
                        getPieceMobility(boardArray, indices[n], p)
                    i += len(sliding[p.lower()])

    return feature


# Get the highest value attacker for white and black for each square on the board
# 8*8*2 = 128 features total
def getSquareCentricFeatures(board):
    feature = np.zeros(128)
    i = 0
    for r in xrange(8):
        for c in xrange(8):
            attacker, defender = getLowestAttackerDefender(board, [r, c], True)
            feature[i] = attacker
            i += 1
            feature[i] = defender
            i += 1
    return feature

# Get a 373 tuple feature representing a chess board
def getBoardFeature(board):
    feature = np.zeros(373)
    i = 0

    feature[i:i+37] = getGlobalFeatures(board)
    i += 37
    feature[i:i+208] = getPieceCentricFeatures(board)
    i += 208
    feature[i:i+128] = getSquareCentricFeatures(board)
    i += 128

    return feature



# Build a feature database of fen positions with one random move using a list of pgn files
# THIS IS INCREDIBLY SLOW!  5.5 hours for a million games.
# The slow speed is from the odd ObjOriented format of the parsed pgn games.  It could be
# significantly improved my doing the parsing myself, but I was going to sleep anyway...
def buildFenDB(files, output):

    count = 0
    output = file(output, 'wb')
    writer = csv.writer(output)

    start_time = time.time()
    for f in files:
        # Open the file
        with open(f) as pgn:
            game = chess.pgn.read_game(pgn)
            while game is not None:

                # Get the number of moves
                moveCount = 0
                node = game
                while not node.is_end():
                    node = node.variation(0)
                    moveCount += 1

                # Get a random turn before checkmate
                randomTurn = random.randint(1, moveCount - 1)
                node = game
                for i in xrange(randomTurn):
                    node = node.variation(0)
                board = node.board()

                # Apply a random legal move
                randomMove = random.randint(0, len(board.legal_moves)-1)
                move = next(itertools.islice(board.legal_moves, randomMove, randomMove + 1))
                board.push(move)

                # Save the fen
                writer.writerow([board.fen()])

                # Get the next game
                game = chess.pgn.read_game(pgn)

                if count % 1000 == 0:
                    print('Saved game', count)
                    print('Time:', time.time()-start_time)
                count += 1

    output.close()


# Shuffle a csv file
def shuffleCSV(inputFile, outputFile):
    lines = open(inputFile, 'rb').readlines()
    random.shuffle(lines)
    open(outputFile, 'wb').writelines(lines)

# Build a feature DB from a file of fen positions
def buildFeatureDB(fenFile, output):
    with open(fenFile, "rb") as f:
        fenstrings = np.array(f.readlines())
        featArray = np.empty((len(fenstrings), 373))
        for index, s in enumerate(fenstrings):
            featArray[index,:] = getBoardFeature(chess.Board(s))
            if index % 1000 == 0:
                print(index)
    np.save(output, featArray)

# Build a database of evaluation tags for a fen database using an evaluation function
def buildLabelDB(fenFile, output, evalFunc):
    start_time = time.time()
    with open(fenFile, "rb") as f:
        fenstrings = np.array(f.readlines())
        labelArray = np.empty((len(fenstrings), 1))
        for index, s in enumerate(fenstrings):
            labelArray[index, :] = evalFunc(chess.Board(s))
            if index % 1000 == 0:
                print(index)
                print('Time:', time.time() - start_time)
    np.save(output, labelArray)

# Slice a database into test and train sets using the provided ratio
def sliceTestData(db, trainOut, testOut, testRatio):
    data = np.load(db)
    cutoff = int(data.shape[0] * testRatio)
    np.save(trainOut, data[:-cutoff])
    np.save(testOut, data[-cutoff:])

# Slice a csv file into test and train sets as aboved, saved as .npy files
def sliceTestBoards(boardDB, trainOut, testOut, testRatio):
    with open(boardDB, "rb") as f:
        fenstrings = np.array(f.readlines())
        cutoff = int(fenstrings.shape[0] * testRatio)
        np.save(trainOut, fenstrings[:-cutoff])
        np.save(testOut, fenstrings[-cutoff:])
        print(fenstrings[0])



# Database object for a fen objects
class BoardDB(object):

    # Load the database and shuffle it
    def __init__(self, boardDB):
        self.db = np.load(boardDB)
        self.n = self.db.shape[0]
        self.index = 0
        np.random.shuffle(self.db)

    # Get the next random batch from the database
    def getNextBatch(self, size):
        if size > self.n:
            raise IndexError

        # If we will reach the end of the DB, reshuffle and start over
        if self.index + size >= self.n:
            np.random.shuffle(self.db)
            self.index = 0

        feats = self.db[self.index: self.index + size]
        self.index += size
        return feats

    def size(self):
        return self.n

# Database object for features
class FeatDB(object):

    # Load the database and shuffle it
    def __init__(self, featureDB, labelsDB=None):
        self.db = np.load(featureDB)
        self.n = self.db.shape[0]
        self.index = 0

        self.labels = labelsDB is not None
        if self.labels:
            self.db = np.hstack((self.db, np.load(labelsDB)))
        np.random.shuffle(self.db)

    # Get the next random batch from the database
    def getNextBatch(self, size):
        if size > self.n:
            raise IndexError

        # If we will reach the end of the DB, reshuffle and start over
        if self.index + size >= self.n:
            np.random.shuffle(self.db)
            self.index = 0



        # Return either just the features or both the features and labels
        if self.labels:
            feats = self.db[self.index: self.index + size, 0:-1]
            labels = self.db[self.index: self.index+size, -1]
            labels.shape = (-1, 1)
            self.index += size
            return feats, labels
        else:
            feats = self.db[self.index: self.index + size, :]
            self.index += size
            return feats

    # Return the features in the database
    def getFeats(self):
        if self.labels:
            return self.db[:,:-1]
        else:
            return self.db

    # Return the labels in the database
    def getLabels(self):
        if self.labels:
            labels = self.db[:,-1]
            labels.shape = (-1, 1)
            return labels
        else:
            return None

    def size(self):
        return self.n