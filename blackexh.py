import sys
import re
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


def calc(spec, path=[], tot=[]):
    path.append(spec)
    possibleswaps = [(ix, ix+1) for ix in range(len(spec)-1) if possible(spec, ix, ix+1)]
    for p in possibleswaps:
        r = copy.deepcopy(spec)
        swap(r, p[0], p[1])
        if goal(r):
            path.append(r)
            tot.append(path)
        calc(r, copy.deepcopy(path), tot)

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
    tot = []
    calc(spec, tot=tot)
    for t in tot:
        for p in t:
            print p
        print
    print len(tot)

if __name__=="__main__":
    main()