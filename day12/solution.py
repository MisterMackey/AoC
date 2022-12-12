from queue import PriorityQueue

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day12/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

class Vertex:
    def __init__(self) -> None:
        self.distance = float('inf')

class Edge:
    def __init__(self) -> None:
        self.weight = 1