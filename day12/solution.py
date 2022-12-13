from queue import PriorityQueue

class Coordinate:
    def __init__(self, x, y, h) -> None:
        self.x = x
        self.y = y
        self.height = ord(h)

class Edge:
    def __init__(self, a, b, weight=1) -> None:
        self.a = a
        self.b = b
        self.weight = weight

class Vertex:
    def __init__(self, coordinate) -> None:
        self.distance = float('inf')
        self.coordinate = coordinate
        self.edges = list[Edge]()
        self.visited = False

    def add_edge(self, edge:Edge):
        self.edges.append(edge)

    def __gt__(self, other):
        return self.distance > other.distance

    def __lt__(self, other):
        return self.distance < other.distance

class Graph:
    def __init__(self, vertices: list[list[Vertex]], root: Vertex) -> None:
        self.visited = list[Vertex]()
        self.root = root
        root.distance = 0
        self.V = PriorityQueue()
        for i in vertices:
            for x in i:
                self.V.put(x)
        
    def Dijkstra(self, target: Vertex):
        while not self.V.empty() and not target in self.visited:
            current = self.V.get()
            for edge in current.edges:
                if edge.b.visited:
                    continue
                newDist = current.distance + edge.weight
                if newDist < edge.b.distance:
                    edge.b.distance = newDist
            current.visited = True
            self.visited.append(current)
            #bleeeeh
            temp = PriorityQueue()
            while not self.V.empty():
                temp.put(self.V.get())
            self.V = temp
        return target

    def Dijkstra_No_Target(self):
        while not self.V.empty():
            current = self.V.get()
            for edge in current.edges:
                if edge.b.visited:
                    continue
                newDist = current.distance + edge.weight
                if newDist < edge.b.distance:
                    edge.b.distance = newDist
            current.visited = True
            self.visited.append(current)
            #bleeeeh
            temp = PriorityQueue()
            while not self.V.empty():
                temp.put(self.V.get())
            self.V = temp
        return self.visited
        
def get_input(test):
    filename = 'input' if test else 'input_full'
    path = 'day12/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def create_map(input: list[str]) -> tuple[list[list[Vertex]], Vertex, Vertex]:
    r = list[list[Vertex]]()
    for i in range(len(input)):
        r.append(list[Vertex]())
        for j in range(len(input[i])):
            coord = Coordinate(i, j, input[i][j].lower())
            v = Vertex(coord)
            if input[i][j] == 'S':
                start = v
                start.coordinate.height = ord('a')
            if input[i][j] == 'E':
                end = v
                end.coordinate.height = ord('z')
            r[i].append(v)
    return r, start, end

def add_edges(map: list[list[Vertex]]):
    for i in range(len(map)):
        row = map[i]
        for j in range(len(row)):
            v = map[i][j]
            if not j == 0:
                if v.coordinate.height - map[i][j-1].coordinate.height > - 2:
                    e = Edge(v, map[i][j-1], 1)
                    v.add_edge(e)
            if not j == len(row)-1:
                if v.coordinate.height - map[i][j+1].coordinate.height > - 2:
                    e = Edge(v, map[i][j+1], 1)
                    v.add_edge(e)
            if not i == 0:
                if v.coordinate.height - map[i-1][j].coordinate.height > - 2:
                    e = Edge(v, map[i-1][j], 1)
                    v.add_edge(e)
            if not i == len(map)-1:
                if v.coordinate.height - map[i+1][j].coordinate.height > - 2:
                    e = Edge(v, map[i+1][j], 1)
                    v.add_edge(e)

def add_edges_reverse(map: list[list[Vertex]]):
    for i in range(len(map)):
        row = map[i]
        for j in range(len(row)):
            v = map[i][j]
            if not j == 0:
                if v.coordinate.height - map[i][j-1].coordinate.height < 2:
                    e = Edge(v, map[i][j-1], 1)
                    v.add_edge(e)
            if not j == len(row)-1:
                if v.coordinate.height - map[i][j+1].coordinate.height < 2:
                    e = Edge(v, map[i][j+1], 1)
                    v.add_edge(e)
            if not i == 0:
                if v.coordinate.height - map[i-1][j].coordinate.height < 2:
                    e = Edge(v, map[i-1][j], 1)
                    v.add_edge(e)
            if not i == len(map)-1:
                if v.coordinate.height - map[i+1][j].coordinate.height < 2:
                    e = Edge(v, map[i+1][j], 1)
                    v.add_edge(e)

def run(test):
    input = get_input(test)
    m, r, e = create_map(input)
    add_edges(m)
    g = Graph(m,r)
    a = g.Dijkstra(e)
    print(a.distance)

def part_two(test):
    input = get_input(test)
    m, r, e = create_map(input)
    add_edges_reverse(m)
    g = Graph(m,e)
    a = g.Dijkstra_No_Target()
    filtered = [x for x in a if x.coordinate.height == ord('a')]
    filtered.sort(key= lambda x : x.distance)
    print(filtered[0].distance)


#run(True)
#run(False)

part_two(True)
part_two(False)
