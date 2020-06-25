from kit import Agent, Team, Direction, apply_direction
import math
import random 
import sys
from collections import deque 
import time
import itertools

# Create new agent
agent = Agent()

# initialize agent
agent.initialize()

f = open('console.txt', 'w')


def within_map(x,y):
    return x >= 0 and y >= 0 and x < len(game_map[0]) and y < len(game_map)

def check_cell(x,y,list, game_map, visited):
    if(within_map(x,y)): #SOUTHEAST
        if(game_map[y][x] != 1 and visited[x][y] == False):
            list.append((x,y))
    return
    
#function for given a list of cells, generate the moves
def valid_neighbors(cell, visited):
    game_map = agent.map
    neighbors = []
    x = cell[0]
    y = cell[1]
    check_cell(x,y+1, neighbors, game_map, visited) #S
    check_cell(x+1,y+1, neighbors, game_map, visited) #SE
    check_cell(x,y-1, neighbors, game_map, visited) #N
    check_cell(x+1,y-1, neighbors, game_map, visited) #NE
    check_cell(x+1,y, neighbors, game_map, visited) #E
    check_cell(x-1,y, neighbors, game_map, visited) #W
    check_cell(x-1,y+1, neighbors, game_map, visited) #SW
    check_cell(x-1,y-1, neighbors, game_map, visited) #NW

    return neighbors[::-1]

def valid_neighbors2(cell, visited):
    game_map = agent.map
    neighbors = []
    x = cell[0]
    y = cell[1]
    check_cell(x,y+1, neighbors, game_map, visited) #S
    check_cell(x+1,y+1, neighbors, game_map, visited) #SE
    check_cell(x+1,y-1, neighbors, game_map, visited) #NE
    check_cell(x+1,y, neighbors, game_map, visited) #E
    check_cell(x,y-1, neighbors, game_map, visited) #N
    check_cell(x-1,y, neighbors, game_map, visited) #W
    check_cell(x-1,y+1, neighbors, game_map, visited) #SW
    check_cell(x-1,y-1, neighbors, game_map, visited) #NW

    return neighbors

def shortest_path_moves(curr, dest):
    if(curr == None or dest == None):
        return []

    game_map = agent.map
    visited = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
    destX = dest[0]
    destY = dest[1]

    queue = deque([(curr,[])])
    
    if(game_map[destY][destX] == 1):
        return []
    
    while(queue):
        cell, path = queue.popleft()
        x = cell[1]
        y = cell[0]
        print(path, file=f)
        path.append(cell)
        visited[y][x] = True
        if(cell == dest):
            return path
 
        adj = valid_neighbors(cell)
        for c in adj:
            cx = c[1]
            cy = c[0]
            newPath = path.copy()
            if(not visited[cy][cx]):
                queue.append((c,newPath))
    return []

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def a_star(curr, dest):
    if(curr == None or dest == None):
        return []
    game_map = agent.map
    visited = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
    start = Node(None, curr)
    start.g = start.h = start.f = 0
    end = Node(None, dest)
    end.g = end.h = end.f = 0

    open_list = []
    closed_list = []
    open_list.append(start)
    while(open_list):
        curr_node = open_list[0]
        curr_idx = 0
        for i, node in enumerate(open_list):
            if(node.f < curr_node.f):
                curr_node = node
                curr_idx = i
        open_list.pop(curr_idx)
        closed_list.append(curr_node)

        if(curr_node == end):
            path = []
            node = curr_node
            while node is not None:
                path.append(node.position)
                node = node.parent
            return path[::-1]

        adj = valid_neighbors(curr_node.position, visited)
        adj_nodes = []
        for cell in adj:
            adj_node = Node(curr_node, cell)
            adj_nodes.append(adj_node)
        for child in adj_nodes:
            for node in closed_list:
                if node == child:
                    continue
            child.g = curr_node.g + 1
            child.h = ((child.position[0] - end.position[0]) ** 2) + ((child.position[1] - end.position[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)

    return None

def rand_point(curr, sec):
    game_map = agent.map
    for i in range(10):
        if(sec == 1):
            point_x= random.randint(0, len(game_map[0])/2-1)
            point_y = random.randint(0, len(game_map)/2-1)
        elif(sec == 3):
            point_x = random.randint(0, len(game_map[0])/2-1)
            point_y = random.randint(len(game_map)/2, len(game_map)-1)
        elif(sec == 2):
            point_x = random.randint(len(game_map[0])/2, len(game_map[0])-1)
            point_y = random.randint(0, len(game_map)/2-1)
        elif(sec == 4):
            point_x= random.randint(len(game_map[0])/2, len(game_map[0])-1)
            point_y = random.randint(len(game_map)/2, len(game_map)-1)
        if(a_star(curr, (point_x,point_y))):
                return None
    if(not a_star(curr, (point_x,point_y))):
            return None
    
    return (point_x, point_y)

def calculate_dir(currX, currY, nextX, nextY):
    if(currX == nextX and nextY > currY):
        return Direction.SOUTH.value
    elif(currX == nextX and nextY < currY):
        return Direction.NORTH.value
    elif(currX > nextX and nextY == currY):
        return Direction.WEST.value
    elif(currX < nextX and nextY == currY):
        return Direction.EAST.value
    elif(currX < nextX and currY < nextY):
        return Direction.SOUTHEAST.value
    elif(currX > nextX and currY < nextY):
        return Direction.SOUTHWEST.value
    elif(currX < nextX and currY > nextY):
        return Direction.NORTHEAST.value
    elif(currX > nextX and currY > nextY):
        return Direction.NORTHWEST.value
    else:
        return Direction.STILL.value

# HIDER FUNCTIONS
def hiding_spots(game_map):
    cells = []
    for row in range(len(game_map)):
        for col in range(len(game_map[0])):
            if game_map[row][col-1] == 1:
                cells.append((row,col))
    return cells

def num_walls(cell, game_map):
    row = cell[1]
    col = cell[0]
    count = 0
    if game_map[row+1][col]:
        count+=1
    if game_map[row-1][col]:
        count+=1
    if game_map[row+1][col+1]:
        count+=1
    if game_map[row-1][col+1]:
        count+=1
    if game_map[row][col+1]:
        count+=1
    if game_map[row][col-1]:
        count+=1
    if game_map[row+1][col-1]:
        count+=1
    if game_map[row-1][col-1]:
        count+=1
    return count

def print_map(game_map):
    cells = hiding_spots(game_map)
    for row in range(len(game_map)):
        for col in range(len(game_map[0])):
                print(num_walls((row,col), game_map) if not game_map[row][col] else '█', end = " ", file=f)
            
        print('', file=f)

def blind_spots(seeker):
    # vision lines of the hider
    return None

def opposite_direction(hider, seeker):
    #go in opposite direction of the seeker
    if(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTH.value):
        return Direction.SOUTH.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTH.value):
        return Direction.NORTH.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.EAST.value):
        return Direction.WEST.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.WEST.value):
        return Direction.EAST.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTHEAST.value):
        return Direction.NORTHWEST.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTHEAST.value):
        return Direction.SOUTHWEST.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTHWEST.value):
        return Direction.NORTHEAST.value
    elif(calculate_dir(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTHWEST.value):
        return Direction.SOUTHEAST.value
    else:
        return Direction.STILL.value

unit = agent.units[0]
init = (unit.x, unit.y)
init2 = (0,0)
init3 = (0,0)
if len(agent.units) > 1:
    unit2 = agent.units[1]
    init2 = (unit2.x, unit2.y)

if len(agent.units) > 2:
    unit3 = agent.units[2]
    init3 = (unit3.x, unit3.y)

game_map = agent.map

#print_map(game_map)
'''
p1 = rand_point(init,1)
p2 = rand_point(init,2)
p3 = rand_point(init,3)
p4 = rand_point(init,4)
print("Point 1:", p1, file=f)
print("Point 2:", p2, file=f)
print("Point 3:", p3, file=f)
print("Point 4:", p4, file=f)
rand = [p1, p2, p3, p4]

path = []
points = []
for point in rand:
    if(point != None):
        points.append(point)

path.extend(shortest_path_moves(init, points[0]))
for i in range(len(points)):
    if i != 0:
        path.extend(shortest_path_moves(points[i-1], points[i]))

if agent.round_num == 1:
    path = []
    path.extend(a_star(init, (4,21)))
    print(game_map[21][4], path, file=f)
'''
stack = []
stack.append(init)
visited = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
chase = []
chasing = False
path = []
go_next = True


path2 = []
stack2 = []
stack2.append(init2)
visited2 = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
chase2 = []
chasing2 = False

path3 = []
stack3 = []
stack3.append(init3)
visited3 = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
chase3 = []
chasing3 = False

hide_stack = []
while True:

    commands = []
    units = agent.units # list of units you own
    opposingUnits = agent.opposingUnits # list of units on other team that you can see
    game_map = agent.map # the map
    round_num = agent.round_num # the round number
    if (agent.team == Team.SEEKER):
        # AI Code for seeker goes here
       
        for _, unit in enumerate(units):
            # unit.id is id of the unit
            # unit.x unit.y are its coordinates, unit.distance is distance away from nearest opponent
            # game_map is the 2D map of what you can see. 
            # game_map[i][j] returns whats on that tile, 0 = empty, 1 = wall, 
            # anything else is then the id of a unit which can be yours or the opponents

             # choose a random direction to move in
            #randomDirection = random.choice(list(Direction)).value
            print("aaaaaa", file=f)
            #seeds that dont work 102892
            if unit.id == units[0].id: 

                if not chase and chasing:
                    chasing = False
                    
                if opposingUnits and not chasing and unit.distance < 50:
                    chasing = True
                    path=[]
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    print("hide spot", hide.id, (hide.x,hide.y), file =f)
                    chase = a_star((unit.x,unit.y),(hide.x,hide.y))

                if chase and chasing:
                    print("chase", chase, (unit.x,unit.y), file =f)
                    next_cell= chase.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                elif path:
                    next_cell = path.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                    print(direction, (unit.x,unit.y), next_cell, file=f)
                elif stack:
                    next_cell = stack.pop()
                    if(next_cell != (unit.x,unit.y) and not next_cell in valid_neighbors((unit.x,unit.y),visited)):
                        print("NEEED TO PATH BACK", file=f)
                        start = time.time()
                        path = a_star((unit.x,unit.y), next_cell)
                        visited[next_cell[0]][next_cell[1]] = True
                        adj = valid_neighbors(next_cell, visited)
                        print("path to neighbors", adj, file=f)
                        for n in adj:
                                stack.append(n)
                        print(time.time()-start, file=f)
                    else:
                        visited[next_cell[0]][next_cell[1]] = True
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                        adj = valid_neighbors(next_cell, visited)
                        for n in adj:
                            if not visited[n[0]][n[1]] and not n in stack:
                                stack.append(n)
                    print("curr", (unit.x,unit.y), "stack", stack, file=f)
            elif unit.id == units[1].id:
                if not chase2 and chasing2:
                    chasing2 = False
                    
                if opposingUnits and not chasing2 and unit.distance < 50:
                    chasing2 = True
                    path2=[]
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    print("hide spot", hide.id, (hide.x,hide.y), file =f)
                    chase2 = a_star((unit.x,unit.y),(hide.x,hide.y))

                if chase2 and chasing2:
                    print("chase", chase2, (unit.x,unit.y), file =f)
                    next_cell2= chase2.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                elif path2:
                    next_cell2 = path2.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                    print(direction, (unit.x,unit.y), next_cell2, file=f)
                elif stack2:
                    next_cell2 = stack2.pop()
                    if(next_cell2 != (unit.x,unit.y) and not next_cell2 in valid_neighbors((unit.x,unit.y),visited2)):
                        print("NEEED TO PATH BACK", file=f)
                        start = time.time()
                        path2 = a_star((unit.x,unit.y), next_cell2)
                        adj = valid_neighbors2(next_cell2, visited2)
                        for n in adj:
                            if not visited2[n[0]][n[1]]:
                                stack2.append(n)
                        print(time.time()-start, file=f)
                    else:
                        visited2[next_cell2[0]][next_cell2[1]] = True
                        direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                        adj = valid_neighbors2(next_cell2, visited2)
                        for n in adj:
                            if not visited2[n[0]][n[1]] and not n in stack2:
                                stack2.append(n)
                else:
                    direction = random.choice(list(Direction)).value
            else:
                if opposingUnits and not chasing3 and unit.distance < 50:
                    chasing3 = True
                    path3=[]
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    chase = a_star((unit.x,unit.y),(hide.x,hide.y))
                    
                if chase3 and chasing3:
                    next_cell= chase3.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                else:
                    direction = random.choice(list(Direction)).value

            # apply direction to current unit's position to check if that new position is on the game map
            (x, y) = apply_direction(unit.x, unit.y, direction)
        
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(direction))
        
    else:
        # AI Code for hider goes here
        # hider code, which does nothing, sits tight and hopes it doesn't get 
        # found by seekers
        #print(opposingUnits, file=f)
        for _, unit in enumerate(units):
            if opposingUnits:
                direction = opposite_direction(unit, opposingUnits[0])
                print(unit.id, hide_stack, file=f)
            else:
                direction = Direction.SOUTH.value
            (x, y) = apply_direction(unit.x, unit.y, direction)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(direction))



    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()

    # wait for update from match engine
    agent.update()
