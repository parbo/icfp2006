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
    
def aStar(start, goal, s):
    closed = set([start])
    q = PriorityQueue()
    swaps = s(start)
    for sw, sc in swaps: 
        n = [list(a) for a in start]
        swap(n, sw[0], sw[1])                  
        pp = [start, tuple([tuple(a) for a in n])]  
        q.push(sc, pp)
    while q:
        est, p = q.pop()
##        print est
##        for pp in p:
##            print pp
##        print
        x = p[-1]   
##        print x
        if x in closed:
            continue
        if len(closed) % 1000 == 0:
            print est, len(closed), "visited"
        if goal(x):
            print len(closed), "visited"
            return p
        closed.add(x)
        swaps = s(x)
##        print len(swaps)
        for sw, sc in swaps: 
            n = [list(a) for a in x]
            swap(n, sw[0], sw[1])   
            n = tuple([tuple(a) for a in n])   
            if n not in closed:
                pp = p + [n]          
                q.push(sc, pp)

def distance(spec):
    plinks = sum([p[1] for p in spec])
##    dist = sum([abs(i-p[0]) for i, p in enumerate(spec)])
    return len(spec) * plinks #+ dist
            
def getswaps(spec):
    p = [s[1] for s in spec]
    maxp = max(p)
    ps = [(ix, ix+1) for ix in range(len(spec)-1) if possible(spec, ix, ix+1) and (spec[ix][1] == maxp or spec[ix+1][1] == maxp)]
    dp = [sum(p)-(p[sw[0]]-p[sw[1]]) for sw in ps]
    return zip(ps, dp)

def swap(a, i1, i2):
    """Swaps columns i1 and i2 in place in a."""
    if i1 > i2:
        i1, i2 = i2, i1
    a[i1][1] -= 1
    a[i1], a[i2] = a[i2], a[i1]
    
def possible(spec, i1, i2):
    """Checks if a swap is possible, i.e. checks plinks vs. distance."""
    if 0 <= i1 < len(spec) and 0 <= i2 < len(spec) and i1 != i2:    
        if i1 > i2:
            i1, i2 = i2, i1
        if spec[i2][1] > (spec[i2][0] - i2) and spec[i1][1] > 0:
            return True
    return False

def goal(spec):
    """Checks if the spec is the same as the goal state."""
    for i, f in enumerate(spec):
        if i != f[0]:
            return False
        if f[1] > 0:
            return False
    return True
        

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
    spec = tuple(spec)
    p = aStar(spec, goal, getswaps)
    
    if p:
##        for pp in p:
##            print pp
            
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
        