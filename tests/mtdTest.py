import sys
sys.path.extend(["../players", "../python-chess", ".."])
import chess
import player
import time
import evaluate
import re
import negamax
import mtd

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

p1 = mtd.mtdPlayer(evaluate.combinedEvaluate, True)
g = open("../logs_combined/%s_%d.txt" % (p1.getName(), time.time()),"w+")
h = open("../tp/%s_%d.txt" % (p1.getName(), time.time()),"w+")
for i in range(1,15):
    total = 0
    bm = 0 
    t3 = 0
    with open("../STS/STS%d.epd" % i) as f:
        g.write("STS/STS%d.epd\n" % i)
        h.write("STS/STS%d.epd\n" % i)
        
        nodes = []
        scoreHits = []
        moveHits = []
        for j, line in enumerate(f.read().splitlines()):
            position, operations, values = parseEpd(line)
            state = chess.Board()
            state.set_epd(position)
            p1.role = state.turn
            move = p1.getMove(state, 10)
            sanMove = state.san(move)
            score = values.get(sanMove, 0)
            # print(sanMove, operations['c0'], score)
            if score:
                total += int(score)
                t3 += 1
            if sanMove == operations['bm']:
                bm += 1
            nodes.append(p1.nodes)
            scoreHits.append(p1.tp_score.hits)
            moveHits.append(p1.tp_move.hits)
            g.write("%d, %d, %s, %s, %s\n" % (j, p1.nodes, values, sanMove, score))
            h.write('%d, %d, %d\n' % (j, p1.tp_score.hits, p1.tp_move.hits))
            print(sanMove, operations['c0'], score, p1.nodes, p1.tp_score.hits, p1.tp_move.hits)
            print(state)
            
        g.write(">>(Score, bm, t3, nodes): (%d, %d, %d, %f)\n" % (total, bm, t3, sum(nodes) / float(100)))
        h.write(">>(Avg Hits): (%d, %d)\n" % (sum(scoreHits) / float(100), sum(moveHits) / float(100)))


# for i, score in enumerate(scores):
#     f.write("Score, Correct, t3 = %d, %d, %d\n" % (score, correct[i], t3[i]))