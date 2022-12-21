from typing import Union

class Monkey:
    def __init__(self, name: str, value: Union[int, str]) -> None:
        self.name = name
        self.value = value
        
    def get_value(self, monkeys: list["Monkey"]) -> Union[int, bool]:
        if type(self.value) is int:
            return self.value
        else:
            monke = self.value.split(' ')
            value1 = next((x for x in monkeys if x.name == monke[0]))
            value2 = next((x for x in monkeys if x.name == monke[2]))
            x = self.value.replace(monke[0], str(value1.get_value(monkeys)))
            x = x.replace(monke[2], str(value2.get_value(monkeys)))
            self.formula = x
            return eval(x)

def get_input(test, part_two):
    filename = 'input' if test and not part_two else 'input_full' if not test and not part_two else 'input_2' if test and part_two else 'input_full_2'
    path = '/mnt/dev/Learning/AoC/Days/day21/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input
    
def part_one(test):
    x = list(get_input(test, False))
    monkeys = list[Monkey]()
    for m in x:
        parts = m.split(':')
        try:
            val = int(parts[1])
            monkeys.append(Monkey(parts[0], val))
        except:
            val = parts[1].strip()
            monkeys.append(Monkey(parts[0], val))
            
    root = next(monke for monke in monkeys if monke.name == 'root')
    print(root.get_value(monkeys))

def part_two(test):
    x = list(get_input(test, True))
    monkeys = list[Monkey]()
    for m in x:
        parts = m.split(':')
        try:
            val = int(parts[1])
            monkeys.append(Monkey(parts[0], val))
        except:
            val = parts[1].strip()
            monkeys.append(Monkey(parts[0], val))
            
    root = next(monke for monke in monkeys if monke.name == 'root')
    human = next(monke for monke in monkeys if monke.name == 'humn')
    human.value = 0
    root.get_value(monkeys)
    human.value = 1
    root.get_value(monkeys)
    diff = 0
    #ngl, i put the below in the terminal and just changed the number for human
    #value around until i got the right one
    #im sure i could put this in some goal-seek kind of loop but w/e this was easier
    #and im hungover
    human.value = 3848301405791
    print(root.get_value(monkeys))
    print(root.formula)
    newdiff = float(root.formula.split(' == ')[0]) - float(root.formula.split(' == ')[1])
    print(newdiff)
    if newdiff < diff:
        print('new diff smaller')
    diff = newdiff 
    print(human.value)