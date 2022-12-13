import json

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day13/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def split_into_pairs(input):
    r = list[(str,str)]()
    for i in range(int((len(input)+ 1) / 3)):
        offset = i * 3
        r.append( (input[offset], input[offset+1]) )
    return r

def make_packets(pairs):
    r = list()
    for pair in pairs:
        left,right = (json.loads(pair[0]), json.loads(pair[1]))
        r.append((Packet(left), Packet(right)))
    return r

class Packet:
    def __init__(self, data: list) -> None:
        self.data = data
        
    def _compare_array(self, left, right):
        i = -1
        left_len = len(left)
        right_len = len(right)
        while (True):
            i += 1
            if i == left_len and not i == right_len:
                return 1
            elif i == right_len and not i == left_len:
                return -1
            elif i == right_len and i == left_len:
                print('warning, edge case')
                return 0
            #other case should not occur, consider raise error if they do
            element_left = left[i]
            element_right = right[i]
            #both int?
            if type(element_left) == int and type(element_right) == int:
                if element_left == element_right:
                    continue
                elif element_left < element_right:
                    return 1
                elif element_left > element_right:
                    return -1
            
            if type(element_right) == int:
                tmp = element_right
                element_right = list()
                element_right.append(tmp)
            if type(element_left) == int:
                tmp = element_left
                element_left = list()
                element_left.append(tmp)
            x = self._compare_array(element_left, element_right)
            if x == 0:
                continue
            else:
                return x
    
    def __lt__(self, other):
        left, right = (self.data, other.data)
        x = self._compare_array(left, right)
        return x == 1
    
    def __gt__(self, other):
        left, right = (self.data, other.data)
        x = self._compare_array(left, right)
        return x == -1

    def __eq__(self, other):
        left, right = (self.data, other.data)
        x = self._compare_array(left, right)
        return x == 0

def part_one(test):
    x = get_input(test)
    y = split_into_pairs(x)
    z = make_packets(y)
    indices = list()
    for i, pair in enumerate(z):
        if pair[0] < pair[1]:
            indices.append(i+1)
    print(sum(indices))

def part_two(test):
    x = get_input(test)
    y = split_into_pairs(x)
    z = make_packets(y)
    flatlist = list[Packet]()
    for pair in z:
        flatlist.append(pair[0])
        flatlist.append(pair[1])
    divider1 = Packet([[2]])
    divider2 = Packet([[6]])
    flatlist.append(divider1)
    flatlist.append(divider2)
    flatlist.sort()
    for packet in flatlist:
        print(packet.data)
    index1 = flatlist.index(divider1)
    index2 = flatlist.index(divider2)
    print('divider 1 at offset (not idx): {0}'.format(index1))
    print('divider 2 at offset (not idx): {0}'.format(index2))
    print((index1+1) * (index2+1))

#part_one(True)
#part_one(False)

part_two(True)
part_two(False)