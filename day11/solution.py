from typing import Callable
from math import floor

class Monkey:
    def __init__(self, items: list[int],
                 operation: Callable[[int], int],
                 test: Callable[[int], bool],
                 action: Callable[[bool, int], None]) -> None:
        self.items = items
        self.operation = operation
        self.test = test
        self.action = action
        self.num_inspects = 0
    
    def _post_inspect(self, old_val):
        return floor(old_val / 3)

    def take_turn(self):
        for i_item, item in enumerate(self.items):
            new_val = self.operation(item)
            new_val = self._post_inspect(new_val)
            test_result = self.test(new_val)
            self.action(test_result, new_val)
            self.num_inspects += 1
        #after the turn we have no items
        self.items.clear()
            
def read_file(test):
    file = 'input' if test else 'input_full'
    with open(file) as f:
        txt = f.read().splitlines()
    return txt

def split_input_to_monkeys(input: list[str]):
    x = list[list[str]]()
    curr = list[str]()
    for line in input:
        if line.isspace() or line == '':
            x.append(curr)
            curr = list[str]()
        else:
            curr.append(line)
    return x

def create_monkey_from_input(input: list[str]) -> Monkey:
    #each monkey is defined in 6 lines, first line is offset (0,1,2)
    starting_items = list(input[1].split(':')[1].split(','))
    operation = lambda old : old*19

#to future self: at this point i realized that python does not have a libary to
#create expression trees and implementing it is gonna take a whole lotta time,
#so i switched to C#