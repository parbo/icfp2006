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
    
def direction(spec, i):
    """Returns the direction a swap should be to move closer to target."""
    if spec[i][0]-i > 0:
        return 1
    return -1
    
    
def distance(spec):
    def dd(a, b):
        return abs(a-b) #b - a #a - b
    plinks = sum([p[1] for p in spec])
    dist = sum([dd(i,p[0]) for i, p in enumerate(spec)])
    return len(spec) * plinks + dist

def calc(spec):
    """Returns the next spec."""
    print
    print spec
    print
    nb = []
    for s in range(len(spec)-1):
        r = copy.copy(spec) #[a for a in spec]
        print spec
        print r
        if possible(r, s, s+1):            
            swap(r, s, s+1)
            print spec
            print r
            nb.append(((distance(spec)-distance(r)), r))
    nb.sort()
    nb.reverse()
    for n in nb:
        print "  ", n
    return nb[0][1]

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
    f = open(sys.argv[1]+".s.txt", "w")
    f.write("".join(res))
    f.close()
    print "".join(res)
            
        
if __name__=="__main__":
    t = timeit.Timer("main()", "from __main__ import main")
    print t.timeit(1)
        