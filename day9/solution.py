class Knot:
    def __init__(self) -> None:
        self.x = 1
        self.y = 1

    def __str__(self) -> str:
        return '{0} : {1}'.format(self.x, self.y)

head = Knot()
knot1 = Knot()
knot2 = Knot()
knot3 = Knot()
knot4 = Knot()
knot5 = Knot()
knot6 = Knot()
knot7 = Knot()
knot8 = Knot()
knot9 = Knot()

positions = set[tuple]()
positions.add((1,1))

def diag_update(head, tail):
    #x update
    if head.x > tail.x:
        tail.x += 1
    else:
        tail.x -= 1
    #y update
    if head.y > tail.y:
        tail.y += 1
    else:
        tail.y -= 1

def y_update(head, tail):
    if head.y > tail.y:
        tail.y += 1
    else:
        tail.y -= 1

def x_update(head, tail):
    if head.x > tail.x:
        tail.x += 1
    else:
        tail.x -= 1

def append_coordinate():
    positions.add( (knot9.x, knot9.y) )

def update_tail(head, tail):
    #how far are head and tail apart?
    ydist = max(head.y, tail.y) - min(head.y, tail.y) 
    xdist = max(head.x, tail.x) - min(head.x, tail.x) 
    #if distance is 3 we move diagonally, if either (but not both) is 2 we move hor/vert, else dont move
    #part 2 introduces the possibility of total dist being 4, triggering a diagonal move
    if ydist+xdist >= 3:
        diag_update(head, tail)
    elif ydist == 2:
        y_update(head, tail)
    elif xdist == 2:
        x_update(head, tail)
    else:
        return
    
#head is moved one step, tail follows. Anything that happens as a result is dealt with here
def move_head(direction: str):
    match direction:
        case 'U':
            head.y += 1
        case 'D':
            head.y -= 1
        case 'R':
            head.x += 1
        case 'L':
            head.x -= 1
    update_tail(head, knot1)
    update_tail(knot1, knot2)
    update_tail(knot2, knot3)
    update_tail(knot3, knot4)
    update_tail(knot4, knot5)
    update_tail(knot5, knot6)
    update_tail(knot6, knot7)
    update_tail(knot7, knot8)
    update_tail(knot8, knot9)
    append_coordinate()

def read_input(test: bool):
    if test:
        with open('./input') as f:
            return f.read().splitlines()
    else:
        with open('./input_full') as f:
            return f.read().splitlines()

def process_line(direction, repeat):
    times = int(repeat)
    for i in range(times):
        move_head(direction)

def process_input(input):
    for line in input:
        direction, repeat = line.split(' ')
        process_line(direction, repeat)

def test():
    i = read_input(True)
    process_input(i)
    print('Set with positions has {0} entries'.format(len(positions)))

def full():
    i = read_input(False)
    process_input(i)
    print('Set with positions has {0} entries'.format(len(positions)))