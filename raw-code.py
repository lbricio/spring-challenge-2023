import sys
import math
from collections import deque

class Cell:
    def __init__(self, _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5):
        self._type = _type
        self.initial_resources = initial_resources
        self.neighbors = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]
        self.resources = 0
        self.my_ants = 0
        self.opp_ants = 0

    def update(self, resources, my_ants, opp_ants):
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants

class Resource:
    def __init__(self, cells, index, connections):
        self._index = index
        self._type = cells[index]._type
        # connections and distances
        self.connections = get_resource_connections(cells, index, connections)

def create_map_by_depth(cells, base_index):
    visited = set()
    layers = list()
    layers.append([base_index])
    while True:
        layer_temp = []
        for current_index in list(layers[-1]):
            cell = cells[current_index]
            for neighbor_index in cell.neighbors:
                if neighbor_index != -1 and neighbor_index not in visited:
                    visited.add(neighbor_index)
                    layer_temp.append(neighbor_index)
        layers.append(layer_temp)
        if len(layer_temp) == 0:
            break
    return layers

def get_dist(cells, point_a, point_b):
    queue = deque([(point_a, 0)])
    visited = set([point_a])
    while queue:
        current_point, current_dist = queue.popleft()
        if current_point == point_b:
            return current_dist
        current_cell = cells[current_point]
        for neighbor_index in current_cell.neighbors:
            if neighbor_index != -1 and neighbor_index not in visited:
                queue.append((neighbor_index, current_dist + 1))
                visited.add(neighbor_index)
    return -1

def get_resource_connections(cells, resource_index, connections):
    paths = {}
    for other_resource in connections:
        if other_resource != resource_index:
            distance = get_dist(cells, resource_index, other_resource)
            if distance != -1:
                paths[other_resource] = distance
    return paths

def render_route(cells, path_to_render, base_indexes):
    start_indexes = base_indexes[:]
    previous_paths = [[base_indexes] for _ in base_indexes]
    paths = []

    for end_index in path_to_render:
        paths = []
        for i, start_index in enumerate(start_indexes):
            if previous_paths[i]:
                expanded_path = expand_path(cells, previous_paths[i], end_index)
                if expanded_path:
                    path = expanded_path
                else:
                    path = bfs(cells, previous_paths[i][-1], end_index)
            else:
                path = bfs(cells, start_index, end_index)
            
            if path:
                paths.append(path)

        if paths:
            shortest_path = min(paths, key=len)
            previous_paths = [shortest_path] * len(start_indexes)
            for cell_index in shortest_path[1:]:
                cells[cell_index].resources -= 1
        else:
            previous_paths = [[]] * len(start_indexes)
    
    return cells

def expand_path(cells, path, end_index):
    last_index = path[-1]
    if last_index == end_index:
        return path
    
    neighbors = cells[last_index].neighbors
    for neighbor_index in neighbors:
        if neighbor_index != -1 and neighbor_index not in path:
            expanded_path = path + [neighbor_index]
            if neighbor_index == end_index:
                return expanded_path

    return None

def bfs(cells, start_index, end_index):
    queue = deque([(start_index, [])])
    visited = set([start_index])
    
    while queue:
        current_index, path = queue.popleft()
        if current_index == end_index:
            return path
        neighbors = cells[current_index].neighbors
        for neighbor_index in neighbors:
            if neighbor_index != -1 and neighbor_index not in visited:
                if cells[neighbor_index].resources > 0:
                    return path + [neighbor_index]
                
                visited.add(neighbor_index)
                queue.append((neighbor_index, path + [neighbor_index]))

    return []


def calculate_route(cells, base_index, resource_list, total_ants):
    possible_paths = {}
    path_to_render = []
    path_placed = []
    depth = 0

    # add only possible paths
    for resource_index, distance_from_reference in resource_list[base_index].connections.items():
        if distance_from_reference <= total_ants and cells[resource_index].resources > 0:
            possible_paths[resource_index] = distance_from_reference

    # get lowest distance
    nearest_distance = 1000
    for resource_index, distance_from_reference in possible_paths.items():
        if distance_from_reference < nearest_distance:
            nearest_distance = distance_from_reference

    # remove worst paths
    resources_to_remove = []
    for resource_index, distance_from_reference in possible_paths.items():
        if distance_from_reference > max(nearest_distance * 2, 2) or resource_index == base_index:
            resources_to_remove.append(resource_index)
    for resource_index in resources_to_remove:
        del possible_paths[resource_index]

    # put beacon on base
    path_to_render.append(base_index)

    # depth 1
    for resource_index, distance_from_reference in possible_paths.items():
        if distance_from_reference < 2 and cells[resource_index].resources > 0:
            path_to_render.append(resource_index)
            path_placed.append(resource_index)
            depth = 1
    
    #depth 2
    for resource_index, distance_from_reference in possible_paths.items():
        if distance_from_reference == 2 and cells[resource_index].resources > 0:
            if any(elem in cells[resource_index].neighbors for elem in path_placed):
                path_to_render.append(resource_index)
                path_placed.append(resource_index)
                depth = 2
            elif cells[resource_index]._type == 1:
                path_to_render.append(resource_index)
                path_placed.append(resource_index)
                depth = 2
            elif depth != 1:
                path_to_render.append(resource_index)
                path_placed.append(resource_index)
                depth = 2

    #depth 3+
    path_loop = True
    possible_paths = {}
    while path_loop == True:
        for i in path_placed:
            for resource_index, distance_from_reference in resource_list[i].connections.items():
                if (distance_from_reference <= total_ants
                and cells[resource_index].resources > 0):
                    possible_paths[resource_index] = distance_from_reference

        for resource_index, distance_from_reference in resource_list[base_index].connections.items():
            if (distance_from_reference <= total_ants 
            and cells[resource_index].resources > 0
            and resource_index not in path_placed):
                possible_paths[resource_index] = distance_from_reference
        path_loop = False
        for resource_index, distance_from_reference in possible_paths.items():
            if cells[resource_index].resources > 0 and resource_index not in path_placed:
                if any(elem in cells[resource_index].neighbors for elem in path_placed):
                    path_to_render.append(resource_index)
                    path_placed.append(resource_index)
                    path_loop = True
        if (len(possible_paths) == 0):
            return path_to_render
        min_value = min(possible_paths.values())
        #possible_paths = {i: j for i, j in possible_paths.items() if j == min_value}
        for resource_index, distance_from_reference in possible_paths.items():
            if distance_from_reference < min_value: #attention
                if (cells[resource_index].resources > 0
                and resource_index not in path_placed):
                    if depth != 1 and depth != 2:
                        path_to_render.append(resource_index)
                        path_placed.append(resource_index)
                        path_loop = True
                        depth = 3
                    elif depth == 0:
                        path_to_render.append(resource_index)
                        path_placed.append(resource_index)
        # keep lines
        for resource_index, distance_from_reference in resource_list[base_index].connections.items():
            if (resource_index not in path_placed
            and cells[resource_index].resources > 0 
            and cells[resource_index].my_ants > 0):
                path_to_render.append(resource_index)
                path_placed.append(resource_index)

    # depth 4
    possible_paths = {}
    # connection between base and resources 
    for index, distance_until_base in resource_list[base_index].connections.items():
        for i in path_placed:
            # resources to resources distance
            for resource_index, distance_from_beach in resource_list[i].connections.items():
                if (distance_from_beach <= total_ants
                and cells[resource_index].resources > 0
                and resource_index not in path_placed
                and distance_from_beach <= distance_until_base):
                    possible_paths[resource_index] = distance_from_beach
    if not possible_paths:
        return path_to_render
    # use distant beacons as entry-point
    for i, distance_from_reference in possible_paths.items():
        nearest_distance = 100
        nearest_beacon = 100
        for resource_index, distance_from_beacon in resource_list[i].connections.items():
            if (distance_from_beacon <= total_ants
            and cells[resource_index].resources > 0
            and nearest_distance > distance_from_beacon):
                nearest_beacon = resource_index
                nearest_distance = distance_from_beacon
        if nearest_beacon != 100:
            path_to_render.append(i)
    return path_to_render

number_of_cells = int(input())
cells = []
for i in range(number_of_cells):
    _type,initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = map(int, input().split())
    cells.append(Cell(_type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))
number_of_bases = int(input())

resources_locations = []
resource_list = {}

base_indexes = []
for i in input().split():
    base_indexes.append(int(i))

opp_base_indexes = []
for i in input().split():
    opp_base_indexes.append(int(i))

first_turn = True

while True:
    total_ants = 0
    for i in range(number_of_cells):
        resources, my_ants, opp_ants = map(int, input().split())
        cells[i].update(resources, my_ants, opp_ants)
        total_ants += my_ants

    if first_turn:
        maps = []
        # create a map depth reference for each base
        for i in range(number_of_bases):
            maps.append(create_map_by_depth(cells, base_indexes[i]))
        # get all resources locations in map
        for i in range(number_of_cells):
            if cells[i]._type != 0 or i in base_indexes:
                resources_locations.append(i)
        # create distance connections beetween resources
        for resource_index in resources_locations:
            resource_list[resource_index] = Resource(cells, resource_index, resources_locations)
        first_turn = False

    # actions loop
    path_to_render = []
    for i in range(number_of_bases):
        path = calculate_route(cells, base_indexes[i], resource_list, total_ants)
        path_to_render.append(path)
    render_route(cells, path_to_render, base_indexes)
    print()
