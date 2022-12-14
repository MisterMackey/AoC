import re

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day14/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def ints(s: str) -> list[int]:
    x = re.findall('\d+', s)
    r = map(lambda s : int(s), x)
    return list(r)

def c_tuples(ints):
    tuples = list[(int,int)]()
    for i in range(int(len(ints)/2)):
        offset = i*2
        tuples.append( (ints[offset], ints[offset+1]) )
    return tuples

def tuple_dims(tuples) -> tuple[int, int, int, int]:
    x = [c[0] for c in tuples]
    y = [c[1] for c in tuples]
    left = min(x)
    right = max(x)
    top = min(y)
    bottom = max(y)
    return left,right,top,bottom

def max_dims(tuple_dims):
    xmin = [c[0] for c in tuple_dims]
    xmax = [c[1] for c in tuple_dims]
    ymin = [c[2] for c in tuple_dims]
    ymax = [c[3] for c in tuple_dims]
    left = min(xmin)
    right = max(xmax)
    top = min(ymin)
    bottom = max(ymax)
    return left,right, 0,bottom #0 hardcoded

class GridLocation:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.is_air = True
        self.is_rock = False
        self.is_sand = False
        self.is_void = False
    
    def rock(self):
        self.is_air = False
        self.is_rock = True
        
    def sand(self):
        self.is_air = False
        self.is_sand = True
        
    def air(self):
        self.is_air = True
        self.is_sand = False
        
    def void(self):
        self.is_air = False
        self.is_rock = False
        self.is_sand = False
        self.is_void = True
        return self
        
    def __str__(self) -> str:
        return 'X' if self.is_rock else 'O' if self.is_sand else '.'
    
def create_grid(dims):
    left, right, top, bottom = dims
    grid = list[list[GridLocation]]()
    for y in range(top, bottom+1):
        grid.append(list[GridLocation]())
        for x in range(left, right+1):
            grid[y].append(GridLocation(x,y))
    return grid

def draw_rocks(grid, tuple_list, max_dims):
    xTranslation = -max_dims[0]
    for i, tupleset in enumerate(tuple_list):
        for j, tuple in enumerate(tupleset):
            x = tuple[0]+xTranslation
            y = tuple[1]
            grid[y][x].rock()
            if j == len(tupleset)-1:
                break
            next = tupleset[j+1]
            drawleft = True if next[0]+xTranslation < x else False
            drawup = True if next[1] < y else False
            for xco in range(x, next[0]+xTranslation, -1 if drawleft else 1):
                grid[y][xco].rock()
            for yco in range(y,next[1], -1 if drawup else 1):
                grid[yco][x].rock()
    
def draw_cave(grid):
    for r in grid:
        x = list(map(lambda x: x.__str__(), r))
        r =""
        for c in x:
            r += c
        print(r)

def produce_sand(grid, max_dims):
    xTranslation = -max_dims[0]
    sandblock = grid[0][500+xTranslation]
    sandblock.sand()
    return sandblock
    
#returns next send block, if its the same block we are at rest
#throws on void
def sand_update(sand_block, grid, max_dims):
    xTranslation = -max_dims[0]
    x, y = sand_block.x+xTranslation, sand_block.y
    #check the three blocks it might fall to and move it if possible
    # halt in some way for void blocks
    blockBelow = grid[y+1][x] if not y == max_dims[3] else GridLocation(y+1, x).void()
    if blockBelow.is_void:
        sand_block.air()
        raise Exception('void reached')
    elif blockBelow.is_air:
        blockBelow.sand()
        sand_block.air()
        return blockBelow 
    blockLeft = grid[y+1][x-1] if not (y == max_dims[3] or x == 0) else GridLocation(y+1, x-1).void()
    blockRight = grid[y+1][x+1] if not (y == max_dims[3] or x == max_dims[1]+xTranslation) else GridLocation(y+1, x-1).void()
    if blockLeft.is_void:
        sand_block.air()
        raise Exception('void reached')
    elif blockLeft.is_air:
        blockLeft.sand()
        sand_block.air()
        return blockLeft 
    if blockRight.is_void:
        sand_block.air()
        raise Exception('void reached')
    elif blockRight.is_air:
        blockRight.sand()
        sand_block.air()
        return blockRight
    return sand_block

def run(grid, maxdim):
    iterations = 0
    running = True
    try:
        newblock = None
        while running:
            iterations += 1
            if iterations % 1000 == 0:
                print(iterations)
            sandblock = produce_sand(grid, maxdim)
            if sandblock is newblock:
                raise Exception('void reached') #lol filthy
            while True:
                iterations += 1
                if iterations % 1000 == 0:
                    print(iterations)
                newblock = sand_update(sandblock, grid, maxdim)
                if newblock is sandblock:
                    #at rest, break to produce new block
                    break
                else:
                    sandblock = newblock
    except Exception as e:
        if str(e) == 'void reached':
            running = False
        else:
            raise

def partone(test):
    input = get_input(test)
    intlist = list(map(lambda x: ints(x), input))
    tuplelist = list(map(lambda x: c_tuples(x), intlist))
    dims = list(map(lambda x: tuple_dims(x), tuplelist))
    maxdim = max_dims(dims)
    grid = create_grid(maxdim)
    draw_rocks(grid, tuplelist, maxdim)
    draw_cave(grid)
    run(grid, maxdim)
    #grid is now in final state
    draw_cave(grid)
    #blows my mind
    sand = [block for row in grid for block in row if block.is_sand]
    print(len(sand))
  
def parttwo(test):
    input = get_input(test)
    intlist = list(map(lambda x: ints(x), input))
    tuplelist = list(map(lambda x: c_tuples(x), intlist))
    #dims of cave
    dims = list(map(lambda x: tuple_dims(x), tuplelist))
    maxdim = max_dims(dims)
    #adding the floor
    ylevel = maxdim[3]+2
    xradius = ylevel+1 #+1 needed? dunno but is safer
    minx = (500-xradius)
    maxx = (500+xradius)
    tuplelist.append([(minx, ylevel), (maxx,ylevel)])
    dims = list(map(lambda x: tuple_dims(x), tuplelist))
    maxdim = max_dims(dims)

    grid = create_grid(maxdim)
    draw_rocks(grid, tuplelist, maxdim)
    draw_cave(grid)
    run(grid, maxdim)
    #grid is now in final state
    draw_cave(grid)
    #blows my mind
    sand = [block for row in grid for block in row if block.is_sand]
    print(len(sand))
    
     