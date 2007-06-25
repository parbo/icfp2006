import sys
import array

class Halt(Exception):
    pass



def interpret(boot):
    r = array.array("L", [0,0,0,0,0,0,0,0])
    pa = [boot]
    ef = 0
    while True:
        op = pa[0][ef]
        optype = op >> 28
##        print optype, (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7, r
        if optype == 0:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            if r[c]:
                r[a] = r[b]
            ef += 1
        elif optype == 1:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            r[a] = pa[r[b]][r[c]]
            ef += 1
        elif optype == 2:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            pa[r[a]][r[b]] = r[c]
            ef += 1
        elif optype == 3:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            r[a] = (r[b] + r[c]) & 0xFFFFFFFF
            ef += 1
        elif optype == 4:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            r[a] = (r[b] * r[c]) & 0xFFFFFFFF
            ef += 1
        elif optype == 5:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            r[a] = ((r[b] & 0xFFFFFFFF) / (r[c] & 0xFFFFFFFF))
            ef += 1
        elif optype == 6:
            a, b, c = (op >> 6) & 0x7, (op >> 3) & 0x7, op & 0x7
            r[a] = ~(r[b] & r[c]) & 0xFFFFFFFF
            ef += 1        
        elif optype == 7:
            raise Halt
        elif optype == 8:
            b, c = (op >> 3) & 0x7, op & 0x7
            pa.append(array.array("L", [0]*r[c]))
            r[b] = len(pa)-1
            ef += 1
        elif optype == 9:
            c = op & 0x7
            pa[r[c]] = None
            ef += 1
        elif optype == 10:
            c = op & 0x7
            sys.stdout.write(chr(r[c]))
            sys.stdout.flush()
            ef += 1
        elif optype == 11:
            c = op & 0x7
            sys.stdin.flush()
            r[c] = sys.stdin.read()
            ef += 1
        elif optype == 12:
            b, c = (op >> 3) & 0x7, op & 0x7
            if r[b] != 0:
                pa[0] = pa[r[b]][:]
            ef = r[c]
        elif optype == 13:
            a, b = (op >> 25) & 0x7, op & 0x1ffffff
            r[a] = b
            ef += 1
        else:
            raise "Unknown op"
        
    
def init(boot):
    i = 0
    while True:
        try:
            A = ord(boot[i])
            B = ord(boot[i+1])
            C = ord(boot[i+2])
            D = ord(boot[i+3])
            p = (A << 24) + (B << 16) + (C << 8) + D
            yield p
        except:
            return
        i += 4

def run(boot):        
    b = array.array("L", boot)
    b.byteswap()
##    for i in range(30):
##        print hex(b[i])
    interpret(b)
    
def main(arg):
    f = open(arg, "rb")
    run(f.read())
        
if __name__=="__main__":
    main(sys.argv[1])

    