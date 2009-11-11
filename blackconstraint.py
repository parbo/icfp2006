import re
from constraint import *

def main(fname):
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
    plinks = sum([s[1] for s in spec])
    
    problem = Problem()
    for i in range(plinks):
        problem.addVariable
    
    
if __name__=="__main__":
    import sys
    main(sys.argv[1])