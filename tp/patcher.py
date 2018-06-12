import re
with open("/Users/milanzhou/Files/Stanford/2017-2018/Spring/CS 221/Project/tp/mtd_1528048680_fixed.txt", "w+") as g:
    with open("/Users/milanzhou/Files/Stanford/2017-2018/Spring/CS 221/Project/tp/mtd_1528048680.txt") as f:
        for line in f.readlines():
            if re.search("STS/", line):
                g.write(line)
                continue
            l = re.search("^0, (.*?)>>\(Avg Hits\): \((\d+)\)", line)
            a = l.group(1).split(", ")
            for i in range(0, len(a)-1):
                g.write(str(i) + ", " + str(a[i][:-1 if i < 9 else -2]) + "\n")
            g.write("99, " + str(a[-1])  + "\n")
            g.write(">>(Avg Hits): (" + l.group(2) + ")\n")
