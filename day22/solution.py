from queue import Queue
import re

def ints(s: str) -> list[int]:
    x = re.findall('-?\d+', s)
    r = map(lambda s : int(s), x)
    return list(r)

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day22/{0}'.format(filename)
    with open(path) as f:
        return f.read().splitlines()

class Tile:
    def __init__(self, x, y, char) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.left: "Tile" = None
        self.right: "Tile" = None
        self.up: "Tile" = None
        self.down: "Tile" = None

def parse_cave(input) -> Tile:
    start = None
    grid = list[list[Tile]]()

    #pad input
    colcount = len(max(input, key= lambda s: len(s)))
    for i, shorty in enumerate(input):
        paddingcount = colcount - len(shorty)
        if paddingcount == 0:
            continue
        else:
            input[i] = shorty + (paddingcount*" ")
    
    for i_row, row in enumerate(input):
        grid.append([])
        for i_col, column in enumerate(row):
            grid[i_row].append(Tile(i_col, i_row, column))
            if start is None and column == '.':
                start = grid[i_row][i_col]
    for i_row in range(len(grid)):
        for i_col in range(len(grid[i_row])):
            if grid[i_row][i_col].char != '.':
                continue
            #top
            top = i_row
            while True:
                top -= 1
                if top == -1:
                    top = len(grid) -1
                if grid[top][i_col].char == '.':
                    grid[i_row][i_col].up = grid[top][i_col]
                    break
                if grid[top][i_col].char == '#':
                    grid[i_row][i_col].up = grid[i_row][i_col]
                    break
            #other direction
            bottom = i_row
            while True:
                bottom += 1
                if bottom == len(grid):
                    bottom = 0
                if grid[bottom][i_col].char == '.':
                    grid[i_row][i_col].down = grid[bottom][i_col]
                    break
                if grid[bottom][i_col].char == '#':
                    grid[i_row][i_col].down = grid[i_row][i_col]
                    break
            left = i_col
            while True:
                left -= 1
                if left == -1:
                    left = len(grid[i_row]) -1
                if grid[i_row][left].char == '.':
                    grid[i_row][i_col].left = grid[i_row][left]
                    break
                if grid[i_row][left].char == '#':
                    grid[i_row][i_col].left = grid[i_row][i_col]
                    break
            right = i_col
            while True:
                right += 1
                if right == len(grid[i_row]):
                    right = 0
                if grid[i_row][right].char == '.':
                    grid[i_row][i_col].right = grid[i_row][right]
                    break
                if grid[i_row][right].char == '#':
                    grid[i_row][i_col].right = grid[i_row][i_col]
                    break
    return start

def split_input(input):
    cave = list[str]()
    for line in input:
        if line == '':
            break;
        cave.append(line)
    return cave, input[-1]

def parse_instructions(instruction) -> Queue:
    q = Queue()
    numbahs = ints(instruction)
    dirs = list(re.findall('L|R', instruction))
    #add one number, then a direction, repeat until empty (end on number)
    q.put(numbahs[0])
    for i in range(1, len(numbahs)):
        q.put(dirs[i-1])
        q.put(numbahs[i])
    return q

def part_one(test):
    input = get_input(test)
    cave_s, instruction_s = split_input(input)
    starting_tile = parse_cave(cave_s)
    curr_tile = starting_tile
    instructions = parse_instructions(instruction_s)
    directions = ['right', 'down', 'left', 'up']
    currdiroffset = 0
    while not instructions.empty():
        move = instructions.get()
        if type(move) is int:
            for i in range(move):
                curr_tile = getattr(curr_tile, directions[currdiroffset])
        else:
            currdiroffset = currdiroffset - 1 if move == 'L' else currdiroffset + 1
            #handle wrapping
            if currdiroffset == -1:
                currdiroffset = 3
            elif currdiroffset == 4:
                currdiroffset = 0
    print('Row number: {0}, Column number: {1}, Facing: {2}'.format(curr_tile.y +1, curr_tile.x +1, currdiroffset))
    print('Anser: {0}'.format((curr_tile.y + 1) * 1000 + (curr_tile.x + 1) * 4 + currdiroffset))
    return curr_tile

if __name__ =='__main__':
    part_one(True)