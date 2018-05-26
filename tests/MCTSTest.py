import MCTS
import sys
sys.path.append('python-chess')
import chess
import re
import time

def parseEpd(rawLine):
    # 4-field FEN
    line = rawLine.strip().split(' ', 4)
    pos = ' '.join(line[0:4])
    if len(line) < 5:
        line.append('')

    # EPD fields
    operations = {'bm': '', 'am': '', 'dm': ''}
    fields = [op for op in line[4].split(';') if len(op) > 0]
    fields = [op.strip().split(' ', 1) for op in fields]
    operations.update(dict(fields))

    match = re.search("; c0 \"(.*?)\"", rawLine)
    if not match:
        print(rawLine)
    else:
        values = [a.split("=") for a in match.group(1).split(", ")]

    return pos, operations, dict(values)

p1 = MCTS.MCTSPlayer()
state = chess.Board()
g = open("logs/%s_%d.txt" % (p1.getName(), time.time()),"w+")
for i in range(1,15):
    total = 0
    bm = 0 
    t3 = 0
    with open("STS/STS%d.epd" % i) as f:
        g.write("STS/STS%d.epd\n" % i)
        nodes = []
        for j, line in enumerate(f.read().splitlines()):
            position, operations, values = parseEpd(line)
            state = chess.Board()
            state.set_epd(position)
            p1.role = state.turn
            move = p1.getMove(state, 10)
            sanMove = state.san(move)
            score = values.get(sanMove, 0)
            print(sanMove, operations['c0'], score, p1.nodes)
            print(state)
            if score:
                total += int(score)
                t3 += 1
            if sanMove == operations['bm']:
                bm += 1
            nodes.append(p1.nodes)
            g.write("%d, %d, %s, %s, %s\n" % (j, p1.nodes, values, sanMove, score))
        g.write(">>(Score, bm, t3, nodes): (%d, %d, %d, %f)\n" % (total, bm, t3, sum(nodes) / float(100)))