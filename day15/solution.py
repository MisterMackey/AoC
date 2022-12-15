import re

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day15/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def ints(s: str) -> list[int]:
    x = re.findall('-?\d+', s)
    r = map(lambda s : int(s), x)
    return list(r)

class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y) -> None:
        self.x = x
        self.y = y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.manhattan_distance = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

def map_sensor(ints: list[int]) -> Sensor:
    return Sensor(ints[0], ints[1], ints[2], ints[3])

def find_nearest_sensor(x, y, sensorlist) -> Sensor:
    def manhattan(sensor):
        return (abs(x-sensor.x) + abs(y-sensor.y), sensor)
    distances = list(map(manhattan, sensorlist))
    return min(distances, key=lambda x: x[0])

#afterwards: if before that point (in x dim), move the diff in x twice, then move the diff in distance
#if before, move diff in distance

def part_one(test):
    input = get_input(test)
    int_input = list(map(ints, input))
    sensors = list(map(map_sensor, int_input))
    position_not_present = set()
    row_under_consideration = 10 if test else 2000000
    for sensor in sensors:
        distance_to_row = abs(sensor.y - row_under_consideration)
        if sensor.manhattan_distance >= distance_to_row:
            #this if block is for sensors that 'block' a part of the row
            #we only need to store the x values since y is pinned
            #we store every x in x plusminus the difference between manhanttan distance and row distance
            radius = sensor.manhattan_distance - distance_to_row
            for x in range(sensor.x - radius, sensor.x + radius+1):
                position_not_present.add(x)
        else:
            continue
    #answer is off-by-one (too high) so subtract 1 to get the right answer
    #reason found!, im coutning beacon positions, theres 1 on the target row so just subtract..
    print(len(position_not_present))

def part_two(test):
    input = get_input(test)
    int_input = list(map(ints, input))
    sensors = list(map(map_sensor, int_input))
    position_not_present = set()
    max_row = 20 if test else 4000000
    for row_under_consideration in range(0, max_row+1):
        if row_under_consideration % 10000 == 0:
            print('at row {0}'.format(row_under_consideration))
        for sensor in sensors:
            distance_to_row = abs(sensor.y - row_under_consideration)
            if sensor.manhattan_distance >= distance_to_row:
                #this if block is for sensors that 'block' a part of the row
                #we only need to store the x values since y is pinned
                #we store every x in x plusminus the difference between manhanttan distance and row distance
                radius = sensor.manhattan_distance - distance_to_row
                for x in range(sensor.x - radius, sensor.x + radius+1):
                    position_not_present.add((x, row_under_consideration))
            else:
                continue
    print('finding...')
    for x in range(0, max_row+1):
        for y in range(0, max_row+1):
            if (x,y) in position_not_present:
                continue
            else:
                print((x,y))
                break
