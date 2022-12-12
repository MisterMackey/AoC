class CRT:
    def __init__(self) -> None:
        self.pixel_offset_horizontal = 0
        self.pixel_offset_vertical = 0
        self.pixels = list()
        for i in range(6):
            self.pixels.append(list())
    
    def tick(self, register_value):
        if max(self.pixel_offset_horizontal, register_value) - min(self.pixel_offset_horizontal, register_value) < 2:
            #draw lit pixel
            self.pixels[self.pixel_offset_vertical].append('#')
        else:
            self.pixels[self.pixel_offset_vertical].append('.')
        self.pixel_offset_horizontal += 1
        if self.pixel_offset_horizontal == 40:
            self.pixel_offset_horizontal = 0
            self.pixel_offset_vertical += 1
            
    def draw_screen(self):
        for i in range(6):
            x = self.pixels[i]
            s = "".join(x)
            print(s)

class CPU:
    def __init__(self, signal_set: list) -> None:
        self.cycle_num = 1 #base 1 for convenience, 1 means first tick
        self.register = 1
        self.signals = signal_set
        self.CRT = CRT()

    def emit_signal_strength(self):
        self.signals.append(self.cycle_num * self.register)
        
    def _tick(self):
        if (self.cycle_num-20) % 40 == 0:
            self.emit_signal_strength()
        self.CRT.tick(self.register)
        self.cycle_num += 1
    
    def addx(self, V):
        self._tick()
        self._tick()
        self.register += V
    
    def noop(self):
        self._tick()

    def interpret(self, instruction):
        split = instruction.split(' ')
        match split[0]:
            case 'noop':
                self.noop()
            case 'addx':
                self.addx(int(split[1]))

def test():
    x = list()
    c = CPU(x)
    with open('input') as input:
        i = input.read().splitlines()
    for instruction in i:
        c.interpret(instruction)
    print(x)
    sum =0
    for i in range(6):
        sum += x[i]
    print(sum)
    return c

def full():
    x = list()
    c = CPU(x)
    with open('input_full') as input:
        i = input.read().splitlines()
    for instruction in i:
        c.interpret(instruction)
    print(x)
    sum =0
    for i in range(6):
        sum += x[i]
    print(sum)
    return c