# Adapted from mcts.ai
# 
# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a 
# state.GetRandomMove() or state.DoRandomRollout() function.
# 
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in 
# the UCTPlayGame() function at the bottom of the code.
# 
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
# 
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
# 
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai

from math import *
import random
import time
import evaluate
import game

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = set([])
        self.wins = 0
        self.visits = 0
        self.untriedMoves = set(state.legal_moves) # future child nodes
        self.playerJustMoved = not state.turn # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
      
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.add(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def randomMove(state):
        moves = state.legal_moves
        numMoves = len(moves)
        moveNumber = random.randint(0, numMoves-1)
        for i, move in enumerate(moves):
            if i == moveNumber:
                return move
def reward(result, role):
    if result == "1-0":
        r = 1
    elif result == "0-1":
        r = 0
    else:
        r = .5
    if not role:
        r = -r
    return r 

def UCT(rootstate, stopTime, verbose = False):
    rootnode = Node(state = rootstate)
    total = 0

    
    while (time.time() < stopTime):
        
        node = rootnode
        state = rootstate.copy()

        # Select
        while not node.untriedMoves and node.childNodes: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.push(node.move)

        # Expand
        if node.untriedMoves: # if we can expand (i.e. state/node is non-terminal)
            m = random.sample(node.untriedMoves,1)[0] 
            state.push(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        num = 0
        while True: # while state is non-terminal
            result = game.gameOver(state)
            if (result != "*"):
                break
            if (time.time() > stopTime):
                break
            state.push(randomMove(state))
            num += 1
        r = reward(result, node.playerJustMoved)
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(r) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
        total += 1
    # Output some information about the tree - can be omitted
    # if (verbose): print rootnode.TreeToString(0)
    # else: print rootnode.ChildrenToString()

    return (sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move, total) # return the move that was most visited
                
                          
            

