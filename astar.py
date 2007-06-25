from heapq import heappush, heappop

class PriorityQueue(object):
    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def push(self, cost, item):
        heappush(self.q, (cost, item))

    def pop(self):
        return heappop(self.q)[1]
    
def aStar(start, goal, s, g, h):
    closed = set([start])
    q = PriorityQueue()
    neighbours = s(start)
    for n in neighbours:                   
        pp = [start, n]  
        q.push(g(pp)+h(n, goal), pp)
    while q:
        p = q.pop()
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
    
class Maze:
    def __init__(self, size, walls, allowDiagonal = True):
        self.size = size
        self.walls = walls
        self.allowDiagonal = allowDiagonal
        
    def inside(self, pos):
        return (0 <= pos[0] < self.size[0]) and (0 <= pos[1] < self.size[1]) and pos not in self.walls
        
    def getNeighbours(self, pos):
        if self.allowDiagonal:
            neighbours = [(pos[0]-1, pos[1]-1), (pos[0], pos[1]-1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1)]
        else:
            neighbours = [(pos[0], pos[1]-1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]+1)]
        return [n for n in neighbours if self.inside(n)]            
        
    def distance(self, start, goal):
        if self.allowDiagonal:
            return max(abs(start[0]-goal[0]), abs(start[1]-goal[1]))
        else:
            return abs(start[0]-goal[0]) + abs(start[1]-goal[1])
    
    def getPath(self, start, goal):
        return aStar(start, goal, self.getNeighbours, lambda x: len(x), self.distance)

    def printPath(self, start, goal):
        p = self.getPath(start, goal)
        print p
        print "-"*(2*self.size[0]+1)
        for y in range(self.size[1]):
            s = []
            for x in range(self.size[0]):
                if (x, y) in p:
                    s.append("|*")
                elif (x, y) in self.walls:
                    s.append("|X")
                else:
                    s.append("| ")
            s.append("|")
            print "".join(s)
            print "-"*(2*self.size[0]+1)
            
if __name__=="__main__":
    walls = [(3,3), (3,4), (3,5), (3,6), (3,7), (4,3), (5,3), (6,3), (7,3), 
             (4,7), (5,7), (6,7), (7,7), (7,4), (7,5), (6,5), (5,5)]
    
    m = Maze((11,11), walls)    
    m.printPath((0,0), (6,4))
    
    m = Maze((11,11), walls, False)    
    m.printPath((0,0), (6,4))
    