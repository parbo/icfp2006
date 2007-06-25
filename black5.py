import sys
import re
import timeit
import copy

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
    
def distance(spec):
    def dd(a, b):
        return abs(a-b) #b - a #a - b
    plinks = sum([p[1] for p in spec])
    dist = sum([dd(i,p[0]) for i, p in enumerate(spec)])
    return len(spec) * plinks + dist

def getplinks(spec):
    return [s[1] for s in spec]
    
def getdist(spec):
    return [s[0]-i for i, s in enumerate(spec)]

def get(seq, f):
    return [ix for ix, p in enumerate(seq) if p == f(seq)]

def calc(spec):
    """Returns the next spec."""
    print spec
    allswaps = [(ix, ix+1) for ix in range(len(spec)-1)]
    d = getdist(spec)
    p = getplinks(spec)
    mind = get(d, min)
    maxd = get(d, max)
    minp = get(p, min)
    maxp = get(p, max)
    possibleswaps = [(sw[0], sw[1]) for sw in allswaps if possible(spec, sw[0], sw[1]) and (sw[0] in maxp or sw[1] in maxp)]
    print possibleswaps
    if possibleswaps:
        sd = [d[sw[0]]+d[sw[1]] for sw in possibleswaps]
        sad = [abs(d[sw[0]])+abs(d[sw[1]]) for sw in possibleswaps]
        sp = [p[sw[0]]+p[sw[1]] for sw in possibleswaps]
        dp = [p[sw[0]]-p[sw[1]] for sw in possibleswaps]
        print sorted(dp)
        sw = possibleswaps[dp.index(max(dp))]
        r = copy.deepcopy(spec)
        swap(r, sw[0], sw[1])
        return r

def main():
    # Open spec file and parse it
    fname = sys.argv[1]
    comm = re.compile("\*.*")
    sp = re.compile("(\d+)\s+->\s+\((\d+)\s*,\s*(\d+)\)")
    spec = []
    for f in open(fname):
        if comm.match(f):
            continue
        m = sp.match(f)
        if m:
            spec.append([int(m.group(2)), int(m.group(3))])

    # The spec has the form:
    # [(goal, plinks), ...] 
    # where the index of a tuple indicates current position
            
    p = [spec]
    while 1:
        spec = calc(spec)
        p.append(spec)
        if goal(spec):
            break
    for pp in p:
        print pp
        
    # Given the path p, print it in the format used by umix
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
    f = open(sys.argv[1]+".s.txt", "w")
    f.write("".join(res))
    f.close()
    print "".join(res)
            
        
if __name__=="__main__":
    t = timeit.Timer("main()", "from __main__ import main")
    print t.timeit(1)
        