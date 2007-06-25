from heapq import heappush, heappop
import sys
import re
import timeit

class PriorityQueue(object):
    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def push(self, cost, item):
        heappush(self.q, (cost, item))

    def pop(self):
        return heappop(self.q)
    
def aStar(start, goal, s, g, h):
    closed = set([start])
    q = PriorityQueue()
    neighbours = s(start)
    for n in neighbours:                   
        pp = [start, n]  
        q.push(g(pp)+h(n, goal), pp)
    while q:
        est, p = q.pop()
        print est
        for pp in p:
            print pp
        print
        x = p[-1]   
        if x in closed:
            continue
        if x == goal:
            print len(closed), "visited"
            return p
        closed.add(x)
        neighbours = s(x)
        for n in neighbours:   
            if n not in closed:
                pp = p + [n]          
                q.push(g(pp)+h(n, goal), pp)
    
            
def getNeighbours(spec):
    nb = []
##    print spec
##    print
    for s in range(len(spec)-1):
        r = [list(t) for t in list(spec)]
##        print r[s+1][0] - (s+1)
        if r[s+1][1] > (r[s+1][0] - (s+1)) and r[s][1] > 0:
            r[s][1] -= 1
            r[s], r[s+1] = r[s+1], r[s]
            nb.append(tuple([tuple(e) for e in r]))
##    for n in nb:
##        print n
##    print
    return nb

def dd(a, b):
    return b - a #a - b
    
            
def toGoal(path):
    plinks1 = sum([p[1] for p in path[0]])
    plinks2 = sum([p[1] for p in path[-1]])
    dist1 = sum([dd(i,p[0]) for i, p in enumerate(path[0])])
    dist2 = sum([dd(i,p[0]) for i, p in enumerate(path[1])])
    return len(path[0]) * (plinks1 - plinks2) + (dist1 - dist2)

def distance(spec, goal):
    plinks = sum([p[1] for p in spec])
    dist = sum([dd(i,p[0]) for i, p in enumerate(spec)])
    return len(spec) * plinks + dist
        

def main():
    fname = sys.argv[1]
    comm = re.compile("\*.*")
    sp = re.compile("(\d+)\s+->\s+\((\d+)\s*,\s*(\d+)\)")
    spec = []
    for f in open(fname):
        if comm.match(f):
            continue
        m = sp.match(f)
        if m:
            spec.append((int(m.group(2)), int(m.group(3))))
    goal = [(i, 0) for i in range(len(spec))]
    spec = tuple(spec)
    goal = tuple(goal)
    p = aStar(spec, goal, getNeighbours, toGoal, distance)
    for pp in p:
        print pp
        
    res = []
    prev = p[0]
    for pp in p:
        i = 0
        while i < len(pp):
            if pp[i] == prev[i]:
                res.append("|")
                i += 1
            else:
                res.append("><")            
                i += 2
        prev = pp
        res.append("\n")
    print "".join(res)
            
        
if __name__=="__main__":
    t = timeit.Timer("main()", "from __main__ import main")
    print t.timeit(1)
        