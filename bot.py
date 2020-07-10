from kit import Agent, Team, Direction, apply_direction
import math
import random 
import sys
from collections import deque 
import time
import itertools
import copy

# Create new agent
agent = Agent()

# initialize agent
agent.initialize()

game_map = agent.map
f = open('console.txt', 'w')

''' SEEKER FUNCTIONS '''

# Determines if the position (x,y) is within the game map
def within_map(x,y):
    return x >= 0 and y >= 0 and x < len(game_map[0]) and y < len(game_map)

# Checks if the cell is an open space and it is valid to traverse to
def check_cell(x,y,list, game_map, visited):
    if(within_map(x,y)): #SOUTHEAST
        if(game_map[y][x] != 1 and visited[x][y] == False):
            list.append((x,y))
    return
    
# Given a cell, return a list of all the valid neighbors with order
# that prioritizes south and east, then north and west
def valid_neighbors(cell, visited):
    game_map = agent.map
    neighbors = []
    x = cell[0]
    y = cell[1]
    check_cell(x,y+1, neighbors, game_map, visited) #S
    check_cell(x+1,y+1, neighbors, game_map, visited) #SE
    check_cell(x+1,y, neighbors, game_map, visited) #E
    check_cell(x+1,y-1, neighbors, game_map, visited) #NE
    check_cell(x-1,y+1, neighbors, game_map, visited) #SW
    check_cell(x,y-1, neighbors, game_map, visited) #N
    check_cell(x-1,y, neighbors, game_map, visited) #W
    check_cell(x-1,y-1, neighbors, game_map, visited) #NW

    return neighbors[::-1]

# Given a cell, return a list of all the valid neighbors with order
# that prioritizes north and west, then south and east
def valid_neighbors2(cell, visited):
    game_map = agent.map
    neighbors = []
    x = cell[0]
    y = cell[1]

    check_cell(x-1,y-1, neighbors, game_map, visited) #NW
    check_cell(x-1,y, neighbors, game_map, visited) #W
    check_cell(x+1,y-1, neighbors, game_map, visited) #NE
    check_cell(x,y-1, neighbors, game_map, visited) #N
    check_cell(x+1,y, neighbors, game_map, visited) #E
    check_cell(x,y+1, neighbors, game_map, visited) #S
    check_cell(x-1,y+1, neighbors, game_map, visited) #SW
    check_cell(x+1,y+1, neighbors, game_map, visited) #SE

    return neighbors[::-1]

# Node class to be used for A* Search
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

# Distance formula used in A* function
def distance(c, d):
     x1 = c[0]
     y1 = c[1]
     x2 = d[0]
     y2 = d[1]
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

# Finds the shortest path of the current node to the destination node 
# using A*. Core component for the bot to determine the best path to 
# the hider and seeker
def a_star(curr_unit, dest):
    game_map = agent.map
    curr = copy.deepcopy(curr_unit)

    if(curr == None or dest == None or game_map[curr[1]][curr[0]] == 1 or game_map[dest[1]][dest[0]] == 1):
        return []

    visited = [[False for i in range(len(game_map))] for j  in range(len(game_map[0]))]
    start = Node(None, curr)
    start.g = start.h = start.f = 0
    end = Node(None, dest)
    end.g = end.h = end.f = 0

    # Initialize open and closed list to track nodes visited
    open_list = []
    closed_list = []
    closed_list_pos = []
    open_list.append(start)

    while(open_list):
        curr_node = open_list[0] 
        curr_idx = 0

        # Move to the index with the best score
        for i, node in enumerate(open_list):
            if(node.f < curr_node.f):
                curr_node = node
                curr_idx = i

        open_list.pop(curr_idx)
        closed_list.append(curr_node)

        # If we have reached the destination, get the path using
        # the parent and return the path
        if(curr_node.position == end.position):
            path = []
            n = curr_node
            while n is not None:
                path.append(n.position)
                n = n.parent
            path = path[::-1]
            return path[1:]

        # Gets the next neighbors to be pushed into list
        adj = valid_neighbors(curr_node.position, visited)

        adj_nodes = []
        
        # Creates the next cells as Nodes
        for cell in adj:
            adj_node = Node(curr_node, cell)
            adj_nodes.append(adj_node)

        # Determine if the neighbor's score and add it if valid
        for neighbor in adj_nodes:
            add = True
            for node in closed_list:
                if node.position == neighbor.position:
                    add = False

            # Uses Euclidean distance as the heuristic
            neighbor.g = curr_node.g + 1
            neighbor.h = distance(neighbor.position, end.position)
            neighbor.f = neighbor.g + neighbor.h

            for open_node in open_list:
                if neighbor.position == open_node.position:
                    add = False
            if add:
                open_list.append(neighbor)

    return []

# Calculates the direction with the adjacent cell
def calculate_dir(currX, currY, nextX, nextY):
    if(currX == nextX and nextY > currY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.SOUTH.value
    elif(currX == nextX and nextY < currY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.NORTH.value
    elif(currX > nextX and nextY == currY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.WEST.value
    elif(currX < nextX and nextY == currY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.EAST.value
    elif(currX < nextX and currY < nextY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.SOUTHEAST.value
    elif(currX > nextX and currY < nextY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.SOUTHWEST.value
    elif(currX < nextX and currY > nextY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.NORTHEAST.value
    elif(currX > nextX and currY > nextY and abs(currX-nextX)<=1 and abs(currY-nextY)<=1):
        return Direction.NORTHWEST.value
    else:
        return Direction.STILL.value

# Calculates the overall direction if the cell is further away
# Used to calcualte the direction of the seeker/hider
def calculate_dir_far(currX, currY, nextX, nextY):
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

''' HIDER FUNCTIONS '''

# Determines the hiding spots based on the number of walls next to a cell
def hiding_spots(game_map):
    cells = []
    for row in range(len(game_map)):
        for col in range(len(game_map[0])):
            if game_map[row][col-1] == 1:
                cells.append((row,col))
    return cells

# Determines the number of walls adjacent to a given cell
def num_walls(cell, game_map):
    row = cell[1]
    col = cell[0]
    count = 0
    if within_map(cell[0], cell[1]+1) and game_map[row+1][col]:
        count+=1
    if within_map(cell[0], cell[1]-1) and game_map[row-1][col]:
        count+=1
    if within_map(cell[0]+1, cell[1]+1) and game_map[row+1][col+1]:
        count+=1
    if within_map(cell[0]+1, cell[1]-1) and game_map[row-1][col+1]:
        count+=1
    if within_map(cell[0]+1, cell[1]) and game_map[row][col+1]:
        count+=1
    if within_map(cell[0]-1, cell[1]) and game_map[row][col-1]:
        count+=1
    if within_map(cell[0]-1, cell[1]+1) and game_map[row+1][col-1]:
        count+=1
    if within_map(cell[0]-1, cell[1]-1) and game_map[row-1][col-1]:
        count+=1
    return count

# Determines if the wall is valid and not visited .
# Used in DFS for finding islands
def valid_walls(game_map, cell, visited):
    neighbors = []
    x = cell[0]
    y = cell[1]
    if(within_map(x+1, y)):
        if (game_map[y][x+1] == 1 and visited[y][x+1] == False):
            neighbors.append((x+1,y))
    if(within_map(x-1, y)):
        if(game_map[y][x-1] == 1 and visited[y][x-1] == False):
            neighbors.append((x-1,y))
    if(within_map(x, y+1)):
        if (game_map[y+1][x] == 1 and visited[y+1][x] == False):
            neighbors.append((x,y+1))
    if(within_map(x, y-1)):
        if (game_map[y-1][x] == 1 and visited[y-1][x] == False):
            neighbors.append((x,y-1))
            
    return neighbors

# Determines all the blind spots of a unit
# To be implemented for better seeking / hiding
def blind_spots(seeker):
    # vision lines of the hider
    return None

# Returns the opposite direction of the seeker
def opposite_direction(hider, seeker):
    #go in opposite direction of the seeker
    if(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTH.value):
        return Direction.SOUTH.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTH.value):
        return Direction.NORTH.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.EAST.value):
        return Direction.WEST.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.WEST.value):
        return Direction.EAST.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTHEAST.value):
        return Direction.NORTHWEST.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTHEAST.value):
        return Direction.SOUTHWEST.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.SOUTHWEST.value):
        return Direction.NORTHEAST.value
    elif(calculate_dir_far(hider.x,hider.y,seeker.x,seeker.y) == Direction.NORTHWEST.value):
        return Direction.SOUTHEAST.value
    else:
        return Direction.STILL.value

# Returns the direction of three points to determine whether or not
# the points are clockwise (left turn) or counter cc (right turn)
def direction(p,q,r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]) 

# Returns if the cells are adjacent 
def adjacent(p, q):
    return abs(p[0] - q[0] <= 1) and abs(p[1] - q[1] <= 1)


# Finds the closet cell in a path given a point 
def find_closest(curr, path):
    if not path:
        return None

    min_cell = path[0]
    min_dist = distance(curr, min_cell)

    for cell in path:
        if(distance(curr,cell) < min_dist):
            min_cell = cell
            min_dist = distance(curr,cell)
    return min_cell

# Determines all the points that lie in the outline of the cells
# This is used to determine the outer ring of the island so that
# the bot can move in circles
def convexHull(points):
    small = 0
    for i in range(1,len(points)): 
        if points[i][0] < points[small][0]: 
            small = i 
        elif points[i][0] == points[small][0]: 
            if points[i][1] > points[small][1]: 
                small = i 
    hull = []
    p = small
    q = 0
    while(True):
        hull.append(p)
        q = (p + 1) % len(points)
        for i in range(len(points)):
            if(direction(points[p],points[i],points[q]) < 0):
                q = i
        p = q
        if p == small:
            break
    hull_points = []
    for pos in hull: 
        hull_points.append((points[pos][0], points[pos][1])) 
    return hull_points

# Returns a list of all the walls in the map
def all_walls(game_map):
    walls = [] 
    for x in range(len(game_map[0])):
        for y in range(len(game_map)):
            if(game_map[y][x] == 1):
                walls.append((x,y))
    return walls

# Prints the map with the walls
def print_map(game_map):
    walls = all_walls(game_map)
    for col in range(len(game_map[0])):
        for row in range(len(game_map)):
                print('█' if (row,col) in walls else game_map[row][col], end = " ", file=f)
            
        print('', file=f)

# Determines if the cell is on the edge
def edge_pos(cell):
    x = cell[0]
    y = cell[1]
    return x == 0 or y == 0 or x == len(game_map[0])-1 or y == len(game_map)-1

# Helper function used for bfs
def bfs_walls_util(game_map, start, visited):
    island = []
    queue = []
    is_island = False

    island.append(start)
    queue.append(start)
    
    while queue:
        s = queue.pop(0) 

        if edge_pos(s):
            is_island = True

        visited[s[1]][s[0]] = True
        for neighbor in valid_walls(game_map, s, visited):
            #print(neighbor, file=f)
            if neighbor not in island:
                island.append(neighbor)
                queue.append(neighbor)
    if is_island or len(island) < 5:
        return []
    else:
        return island

# Performs BFS on the walls to find the disconnected nodes
def bfs_walls(game_map):
    visited_bfs = [[False for i in range(len(game_map[0]))] for j  in range(len(game_map))]
    print(len(visited_bfs), len(visited_bfs[0]), file=f)
    islands = []
    for cell in all_walls(game_map):
        #print(cell, file=f)
        if visited_bfs[cell[1]][cell[0]] == False:
            islands.append(bfs_walls_util(game_map, cell, visited_bfs))
    return islands

# Prints all the islands after BFS
def print_lands(game_map):
    new_map = copy.deepcopy(game_map)
    lands = bfs_walls(game_map)
    print(lands, file=f)

    for land in lands:
        for cell in land:
            new_map[cell[1]][cell[0]] = '█'
    
    corners = island_convex(game_map)
    for land in corners:
        for cell in land:
            new_map[cell[1]][cell[0]] = 'X'

    for col in range(len(new_map)):
        for row in range(len(new_map[0])):
                print(new_map[col][row], end = " ", file=f)
            
        print('', file=f)

# Determines all the spaces around each wall
def open_wall_spaces(game_map):
    spaces_list = []
    directions = [(0,1), (1,0), (-1,0), (0,-1)]
    islands = bfs_walls(game_map)
    for land in islands:
        spaces = []
        for (x,y) in land:
            for (i, j) in directions:
                cell = (x+i, y+j)
                if game_map[cell[1]][cell[0]] == 0 and cell not in spaces:
                    spaces.append(cell)
        if spaces:
            spaces_list.append(spaces)
    return spaces_list

# Determines all the points around the island
def island_convex(game_map):
    points = []
    island_spaces = open_wall_spaces(game_map)
    for land in island_spaces:
        points.append(convexHull(land))
    return points

# Given a cell find the closest point to the island
def find_closest_island(curr, hull_points):
    point = (None, None)
    min_dist = 1000
    for i, land in enumerate(hull_points):
        for (x, y) in land:
            dist = distance(curr, (x,y))
            if dist < min_dist:
                min_dist = dist
                point = (x,y)
    return point

# Finds the index of the closest island in the list
def find_closest_island_ind(hull_points, closest):
    for i, land in enumerate(hull_points):
        for cell in land:
            if cell == closest:
                return i
    return None

# Determines the complete circle around the island
def find_outline(island_corners):
    outline = []
    if not island_corners:
        return outline
    curr = island_corners[0]
    outline.append(curr)
    for i, cell in enumerate(island_corners):
        if i+1 > len(island_corners) - 1:
            break
        next_corner = island_corners[i+1]

        outline.extend(a_star(curr, next_corner))

        curr = next_corner
    
    return outline

# Hider function that runs in the direction that is the furthest away from the
# seeker; used for when there are no islands to run to
def hider_run(hider, seeker):
    directions = [(0,0), (0,1), (1,0), (1,1), (0,-1), (-1,0), (1,-1), (-1, 1), (-1,-1)]
    best_next = (hider.x, hider.y)
    max_score = -100
    #calculate best distance for each direction if block distance = -1
    for (i, j) in directions:
        offset = 0
        (nx, ny) = (hider.x+i, hider.y+j)
        if (abs(i) == abs(j)):
            offset += 1
        n_walls = num_walls((nx,ny), agent.map)
        if within_map(nx,ny) and game_map[ny][nx] == 0:    
            dist = distance((seeker.x, seeker.y), (nx,ny))
            #offset += n_walls * - 0.5
            if edge_pos((nx,ny)):
                offset += -1.5
            if dist + offset > max_score:
                max_score = dist + offset
                best_next = (nx, ny)
    return best_next

''' INITAL VARIABLES USED FOR HIDER AND SEEKER '''

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

chase3 = []

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
            
            #seeds that dont work 323535
            
            if unit.id == units[0].id: 

                if not chase and chasing2:
                    chasing2 = False
                    
                if opposingUnits and not chasing2:
                    chasing2 = True
                    path=[]
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    chase = a_star((unit.x,unit.y),(hide.x,hide.y))
                elif chasing2 and opposingUnits:
                    if hide_cell[0] != opposingUnits[0].x or hide_cell[1] != opposingUnits[0].y:
                        chase = a_star((unit.x,unit.y),(opposingUnits[0].x,opposingUnits[0].y))
                if chase and chasing2:
                    next_cell= chase.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                elif path:
                    next_cell = path.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                elif stack:
                    next_cell = stack.pop()
                    if(next_cell != init and next_cell != (unit.x,unit.y) and not next_cell in valid_neighbors((unit.x,unit.y),visited)):
                        start = time.time()
                        path = a_star((unit.x,unit.y), next_cell)
                        visited[next_cell[0]][next_cell[1]] = True
                        adj = valid_neighbors(next_cell, visited)
                        for n in adj:
                                stack.append(n)
                        next_cell = path.pop(0)
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                    else:
                        visited[next_cell[0]][next_cell[1]] = True
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                        adj = valid_neighbors(next_cell, visited)
                        for n in adj:
                            if not visited[n[0]][n[1]] and not n in stack:
                                stack.append(n)
            elif unit.id == units[1].id:
                if not chase2 and not chase:
                    chasing = False
                if opposingUnits and not chasing:
                    chasing = True
                    path2=[]
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    chase2 = a_star((unit.x,unit.y),(hide.x,hide.y))


                if chase2:
                    next_cell2= chase2.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                elif path2:
                    next_cell2 = path2.pop(0)
                    direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                elif stack2:
                    next_cell2 = stack2.pop()
                    if(next_cell2 != (unit.x,unit.y) and not next_cell2 in valid_neighbors2((unit.x,unit.y),visited2)):
                        start = time.time()
                        path2 = a_star((unit.x,unit.y), next_cell2)
                        adj = valid_neighbors2(next_cell2, visited2)
                        for n in adj:
                            if n not in stack2:
                                stack2.append(n)
                        n_cell = path2.pop(0)
                        direction = calculate_dir(unit.x, unit.y, n_cell[0], n_cell[1])
                    else:
                        visited2[next_cell2[0]][next_cell2[1]] = True
                        direction = calculate_dir(unit.x, unit.y, next_cell2[0], next_cell2[1])
                        adj = valid_neighbors2(next_cell2, visited2)
                        for n in adj:
                            if n not in stack2:
                                stack2.append(n)
                else:
                    direction = random.choice(list(Direction)).value

            else:
                if opposingUnits and not chasing2:
                    chasing2 = True
                    hide = opposingUnits[0]
                    hide_cell = (hide.x, hide.y)
                    chase3 = a_star((unit.x,unit.y),(hide.x,hide.y))
                if chase3:
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
                #print(round_num, unit.id, direction, (unit.x, unit.y), (x,y), file=f)
                commands.append(unit.move(direction))
          
        
    else:
        # AI Code for hider goes here
        # hider code, which does nothing, sits tight and hopes it doesn't get 
        # found by seekers
        
        # seeds broken 419217

        if round_num == 0:
            
            all_units = copy.deepcopy(units)
            islands = island_convex(game_map)
            starting = False
            init_done = False
            pathing = False
            path = []
            no_island = False
            print_lands(game_map)
            commands.append(unit.move(8))
        else:
            
            for _, unit in enumerate(units):  
                         
                if unit.id == all_units[0].id and not no_island:

                    if (unit.x, unit.y) not in path and not starting:
                        starting = True
                        start_moves = []
                        closest = find_closest_island((unit.x,unit.y), islands)
                        if closest != (None, None):
                            start_moves = a_star((unit.x, unit.y), closest)
                            path_ind = find_closest_island_ind(islands, closest)
                            path = find_outline(islands[path_ind])
                        else:
                            no_island = True
                        
                    
                    if start_moves:
                        next_start = start_moves.pop(0)
                        direction = calculate_dir_far(unit.x, unit.y, next_start[0], next_start[1])
                        if not start_moves:
                            init_done = True
                            starting = False
                    elif init_done and opposingUnits and unit.distance < 20:
                        counter = False
                        clock = False
                        starting = True
                        curr_idx = 0
                        for i, cell in enumerate(path):
                            if cell == (unit.x, unit.y):
                                curr_idx = i
                        if distance((opposingUnits[0].x,opposingUnits[0].y), path[(curr_idx - 1) % (len(path))]) \
                            >= distance((opposingUnits[0].x,opposingUnits[0].y), path[(curr_idx + 1) % (len(path))]):
                            index = (curr_idx - 1) % (len(path))
                            counter = True
                        else:
                            index = (curr_idx + 1) % (len(path))
                            clock = True

                        next_cell = path[index] 
                        if clock:
                            path_smol = copy.deepcopy(path[index:] + path[:index])
                        elif counter:
                            path_smol = copy.deepcopy(path[:index+1][::-1] + path[index:][::-1])

                        init_done = False
                        pathing = True

                        next_cell = path_smol.pop(0)
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])

                        if not path_smol:
                            pathing = False
                            init_done = True
                    elif pathing and path_smol:
                        next_cell = path_smol.pop(0)
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])

                        if not path_smol or not opposingUnits:
                            pathing = False
                            init_done = True
                    else:
                        if(opposingUnits):
                            next_cell = hider_run(unit, opposingUnits[0])
                            direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                        else:
                            direction = Direction.STILL.value
                    
                else:
                    if(opposingUnits):
                        next_cell = hider_run(unit, opposingUnits[0])
                        direction = calculate_dir(unit.x, unit.y, next_cell[0], next_cell[1])
                    else:
                        direction = Direction.STILL.value

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
