import sys
import re
import copy

def readspec(filename):
    """
    Opens spec file and parses it
    """
    comm = re.compile("\*.*")
    sp = re.compile("(\d+)\s+->\s+\((\d+)\s*,\s*(\d+)\)")
    spec = []
    for f in open(filename):
        if comm.match(f):
            continue
        m = sp.match(f)
        if m:
            spec.append([int(m.group(2)), int(m.group(3))])
    return spec

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
    
def readsolution(filename, spec):
    r = [copy.deepcopy(spec)]
    swapix = []
    for f in open(filename):
        for ix, c in enumerate(f):
            if c == '>':
                n = copy.deepcopy(r[-1])
                swap(n, ix, ix+1)
                r.append(n)
                swapix.append((ix, ix+1))
                break    
    return r, swapix

def getplinks(spec):
    return [s[1] for s in spec]
    
def getdist(spec):
    return [s[0]-i for i, s in enumerate(spec)]

def get(seq, f):
    return [ix for ix, p in enumerate(seq) if p == f(seq)]

def main():
    spec = readspec(sys.argv[1])
    solution, swapix = readsolution(sys.argv[2], spec)
    allswaps = [(ix, ix+1) for ix in range(len(spec)-1)]
    for ix, s in enumerate(solution):
        print s
        d = getdist(s)
        p = getplinks(s)
        mind = get(d, min)
        maxd = get(d, max)
        minp = get(p, min)
        maxp = get(p, max)
            
        print mind
        print maxd
        print minp
        print maxp
        print
        possibleswaps = [(sw[0], sw[1]) for sw in allswaps if possible(s, sw[0], sw[1])]
        print possibleswaps
        if possibleswaps:
            sd = [d[sw[0]]+d[sw[1]] for sw in possibleswaps]
            sad = [abs(d[sw[0]])+abs(d[sw[1]]) for sw in possibleswaps]
            sp = [p[sw[0]]+p[sw[1]] for sw in possibleswaps]
            dp = [p[sw[0]]-p[sw[1]] for sw in possibleswaps]
                
            six = swapix[ix]
            print six
            print "Sum dist:", d[six[0]]+d[six[1]], min(sd), max(sd)
            print "Sum abs dist:", abs(d[six[0]])+abs(d[six[1]]), min(sad), max(sad)
            print "Sum plinks:", p[six[0]]+p[six[1]], min(sp), max(sp)
            print "Diff plinks:", p[six[0]]-p[six[1]], min(dp), max(dp)
            print p[six[0]]-p[six[1]]==max(dp) # or abs(d[six[0]])+abs(d[six[1]]) == min(sad)
            print
        else:
            print "No more possible swaps!"


if __name__=="__main__":
    main()