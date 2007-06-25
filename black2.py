import sys
import re
import timeit

def swap(spec, i1, i2):
    """Swaps columns i1 and i2 in place in spec."""
    if i1 > i2:
        i1, i2 = i2, i1
    spec[i1][1] -= 1
    spec[i1], spec[i2] = spec[i2], spec[i1]
    
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
    
def direction(spec, i):
    """Returns the direction a swap should be to move closer to target."""
    if spec[i][0]-i > 0:
        return 1
    return -1
    
def calc(spec):
    """Returns the next spec."""
    sp = spec[:]
    res = []
    plinks = [(s[1], i) for i, s in enumerate(sp)]
    plinks.sort()
    plinks.reverse()
    dist = [(abs(i-s[0]), i) for i, s in enumerate(sp)]
    # Prioritize candidates like this:
    # 1. Most plinks
    # 2. Shortest distance
    candidates = [(p[1], 1) for p in plinks if p[0] == max(plinks)[0]]
    candidates.extend([(d[1], direction(spec, d[1])) for d in sorted(dist) if d[1] not in candidates])
    for c, d in candidates:
        # Primarily move toward target (in direction given by d)
        if possible(sp, c, c+d):  
            print c, d          
            swap(sp, c, c+d)
            break
        # Secondarily move away from target
        elif possible(sp, c, c-d):
            print c, d
            swap(sp, c, c-d)
            break
    if sp == spec:
        # No change was made, bail!
        raise "Foo"
    return sp

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
    print "".join(res)
            
        
if __name__=="__main__":
    t = timeit.Timer("main()", "from __main__ import main")
    print t.timeit(1)
##    main()
        