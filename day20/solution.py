import re;

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day20/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def ints(s: str) -> list[int]:
    x = re.findall('-?\d+', s)
    r = map(lambda s : int(s), x)
    return list(r)
#LOL no doubly linked list in bcl