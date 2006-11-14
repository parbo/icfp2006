d = """There is a bolt here.
Underneath the bolt, there is a spring.
Underneath the spring, there is a button.
Underneath the button, there is a (broken) processor.
Underneath the processor, there is a red pill.
Underneath the pill, there is a (broken) radio.
Underneath the radio, there is a cache.
Underneath the cache, there is a blue transistor.
Underneath the transistor, there is an antenna.
Underneath the antenna, there is a screw.
Underneath the screw, there is a (broken) motherboard.
Underneath the motherboard, there is a (broken) A-1920-IXB.
Underneath the A-1920-IXB, there is a red transistor.
Underneath the transistor, there is a (broken) keypad.
Underneath the keypad, there is some trash."""

import re 
import sys

from simpleparse.common import numbers, strings, comments
from simpleparse.parser import Parser
from simpleparse import dispatchprocessor
import pprint


grammar = r"""
descr := AD,T
AD    := D,WS,M,WS,D,(WS,AND,WS,D)*
AND := 'and'
<A>   := 'some'/'an'/'a'
M   := 'missing'
<T>   := '.'
<WS>  :=  [ \t]*
D     := ('(',AD,')')/SD
SD    := (A,WS,ADJ,WS,OBJ)/(A,WS,OBJ)
OBJ   := [a-zA-Z0-9], [a-zA-Z\-0-9]*
ADJ   := "blue"/"red"
"""

def getStuff(descr):
    rexp1 = re.compile("There is (some|an*) (\(.+\))*\s*(.*) here.")
    rexp2 = re.compile("Underneath the .+, there is (some|an*) (\(.+\))*\s*(.*).")
    stuff = []
    for line in descr.split("\n"):
        m = rexp1.match(line)
        if not m:
            m = rexp2.match(line)
            
        if m:
            broken = True
            if not m.group(2):
                broken = False
            stuff.append({"name" : m.group(3), "broken" : broken})
    for s in stuff:
        if s["broken"]:
            print "examine", s["name"]
##        print s
    pass
    

def parse(d):
    p = Parser(grammar, 'descr')
    try:
        success, children, next = p.parse(d)
        if not success:
            print 'fail', d
        else:
            print 'success', d, next
            pprint.pprint( children )
    except SyntaxError, err:
        print err
    
def parseList(descr):
    for d in descr:
        parse(d)

        
    
def examined(exres, stuff):
    ex = {}
    rexp1 = re.compile(">: examine (.+)")
    curr = 0
    while curr < len(exres) and not exres[curr]:
        curr += 1
    while curr < len(exres):
        m = rexp1.match(exres[curr])
        if not m:
            break
        descr = []
        curr += 1
        while curr < len(exres) and exres[curr]:
            descr.append(exres[curr])
            curr += 1
        while curr < len(exres) and not exres[curr]:
            curr += 1
        ex[m.group(1)] = " ".join(descr)
    rexp2 = re.compile(".*Also, it is broken: it is (.*)")
    descriptions = []
    for k, v in ex.items():
        m = rexp2.match(v)
        if m:
            descriptions.append(m.group(1))
    parseList(descriptions)

def main():
    print "Paste look result, finish with empty row"
    descr = []
    drow = "foo"
    while drow:
        drow = raw_input()
        descr.append(drow)
    stuff = getStuff("\n".join(descr))
    print "paste examine result, finish with three empty rows"
    descr = []
    drow = ""
    emptycount = 0
    while emptycount < 3:
        drow = raw_input()
        descr.append(drow)
        if drow:
            emptycount = 0
        else:
            emptycount += 1
    stuff = examined(descr, stuff)


if __name__=="__main__":
    if len(sys.argv) == 1:
        main()
    else:
        parse(sys.argv[1])