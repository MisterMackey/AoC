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

def find_nearest_sensor(x, y, sensorlist) -> tuple[int, Sensor]:
    def manhattan(sensor):
        return (abs(x-sensor.x) + abs(y-sensor.y), sensor)
    distances = list(map(manhattan, sensorlist))
    return min(distances, key=lambda x: x[0])

def in_range_of_any_sensor(x,y, sensorlist) -> bool:
    for sensor in sensorlist:
        dist_to_sensor = abs(x-sensor.x) + abs(y-sensor.y)
        if dist_to_sensor <= sensor.manhattan_distance:
            return True
    return False

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
    sensors.sort(key= lambda x: x.manhattan_distance)
    for sensor in sensors:
        print('doing sensor at {0},{1}'.format(sensor.x, sensor.y))
        dist = sensor.manhattan_distance + 1
        x,y = sensor.x, sensor.y - dist
        for i in range(0, dist):
            if y > -1 and x > -1 and not in_range_of_any_sensor(x,y, sensors):
                print(x,y)
                answer = x*4000000+y
                print(answer)
                return
            else:
                x,y = x+1, y+1
        for i in range(0, dist):
            if y > -1 and x > -1 and not in_range_of_any_sensor(x,y, sensors):
                print(x,y)
                answer = x*4000000+y
                print(answer)
                return
            else:
                x,y = x-1, y+1
        for i in range(0, dist):
            if y > -1 and x > -1 and not in_range_of_any_sensor(x,y, sensors):
                print(x,y)
                answer = x*4000000+y
                print(answer)
                return
            else:
                x,y = x-1, y-1
        for i in range(0, dist):
            if y > -1 and x > -1 and not in_range_of_any_sensor(x,y, sensors):
                print(x,y)
                answer = x*4000000+y
                print(answer)
                return
            else:
                x,y = x+1, y-1

