# Adapted from mcts.ai

from math import *
import random
import time
import evaluate
import game
import math
import sys
sys.path.append("players")
import player

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = set([])
        self.wins = 0
        self.visits = 0
        self.untriedMoves = set(state.legal_moves) # future child nodes
        self.playerJustMoved = not state.turn if state else not parent.playerJustMoved # the only part of the state that the Node needs later
        
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

def UCT(rootstate, stopTime, evaluatefn = evaluate.simpleEvaluate):
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
        
        # r = evaluatefn(state, node.playerJustMoved) /100
        # rs = [1/(1+math.exp(-r)), 1/(1+math.exp(r))]
        while True: # while state is non-terminal
            result = game.gameOver(state)
            if (result != "*"):
                break
            if (time.time() > stopTime):
                break
            state.push(player.randomMove(state))
        r = game.reward(state, result, node.playerJustMoved) / 10000
        rs = [r, -r]
        # Backpropagate
        i= 0
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(rs[i]) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
            i = int(not i)
        total += 1  
    # Output some information about the tree - can be omitted
    # if (verbose): print rootnode.TreeToString(0)
    # else: print rootnode.ChildrenToString()

    return (sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move, total) # return the move that was most visited