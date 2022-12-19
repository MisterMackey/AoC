import re;
import copy

def get_input(test):
    filename = 'input' if test else 'input_full'
    path = '/mnt/dev/Learning/AoC/Days/day19/{0}'.format(filename)
    with open(path) as f:
        input = f.read().splitlines()
    return input

def ints(s: str) -> list[int]:
    x = re.findall('-?\d+', s)
    r = map(lambda s : int(s), x)
    return list(r)

def get_blueprints(test: bool):
    numbers = map(ints, get_input(test))
    blueprints = []
    for bluepr in numbers:
        blueprints.append({
            "ore_robot": {"ore": bluepr[1]},
            "clay_robot": {"ore": bluepr[2]},
            "obsidian_robot": {"ore": bluepr[3], "clay": bluepr[4]},
            "geode_robot": {"ore": bluepr[5], "obsidian": bluepr[6]}
            })
    return blueprints

def can_afford(resourcetype, blueprint, resources):
    costs = blueprint['{0}_robot'.format(resourcetype)]
    return all(map(lambda x: costs[x] <= resources[x] ,costs))

def buy_robot(resourcetype, blueprint, resources, peons):
    costs = blueprint['{0}_robot'.format(resourcetype)]
    new_peons = copy.deepcopy(peons)
    for cost in costs:
        resources[cost] -= costs[cost]
    new_peons[resourcetype] += 1
    wdbg("I build a {0} robot, it will be ready next minute".format(resourcetype))
    return new_peons

DEBUG = True    
def wdbg(text):
    if DEBUG:
        print(text)

def partone(test: bool):
    limits = {
        "ore" : 1,
        "clay": 4,
        "obsidian": 2,
        "geode": 100,
    }
    peons = {
        "ore" : 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
    resources = {
        "ore" : 0,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
    time_limit = 24
    all_blueprints = get_blueprints(test)
    blueprints = all_blueprints[0]
    
    for i_minute in range(1,time_limit+1):
        wdbg('== Minute {0} =='.format(i_minute))
        #build robots i guess
        #lets just define some limits somewhere
        boughtRobot = False
        for resource_type in limits:
            if peons[resource_type] < limits[resource_type]:
                if can_afford(resource_type, blueprints, resources):
                    newpeons = buy_robot(resource_type, blueprints, resources, peons)
                    boughtRobot = True
        for peon in peons:
            resources[peon] += peons[peon]
            wdbg('{0} {1}-collecting robot(s) collect {0} {1}. You now have {2} {1}'.format(
                peons[peon], peon, resources[peon]
            ))
        if boughtRobot:
            peons = newpeons
    
    print('I end up with {0} geodes in my inventory'.format(resources["geode"]))