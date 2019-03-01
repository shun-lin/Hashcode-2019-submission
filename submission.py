from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

file_names = dict()
file_names["a"] = "a_example.txt"
file_names["b"] = "b_lovely_landscapes.txt"
file_names["c"] = "c_memorable_moments.txt"
file_names["d"] = "d_pet_pictures.txt"
file_names["e"] = "e_shiny_selfies.txt"

# get txt file
input_path = "inputs/"
fname = input_path + file_names["b"]
input_file_name = "b_to_input.txt"
output_file_name = "b_output.txt"
with open(fname) as f:
    content = f.readlines()
    content = [x.strip() for x in content]

# prase through input file and put content in a list
N = int(content[0])

# storage is a list of tuples of (orientation, [attributes], [id])
storage = [0] * N
for i in range(1, N+1):
    line = content[i].split()
    orientation = line[0]
    attributes = set(line[2:])
    item = (orientation, attributes, [i - 1])
    storage[i-1] = item

# give the score of the output list
# ex: [[1], [0,2]]
def score(output_list):
    score = 0
    M = len(output_list)
    for i in range(M-1):
        S_left = output_list[i]
        S_right = output_list[i+1]
        
        attributes_left = set()
        attributes_right = set()
        
        for photo_id in S_left:
            photo_attributes = storage[photo_id][1]
            attributes_left = attributes_left.union(photo_attributes)
            
        for photo_id in S_right:
            photo_attributes = storage[photo_id][1]
            attributes_right = attributes_right.union(photo_attributes)
            
        num_intersection = len(attributes_left.intersection(attributes_right))
        num_left = len(attributes_left.difference(attributes_right))
        num_right = len(attributes_right.difference(attributes_left))
        
        score += min(num_intersection, num_left, num_right)
        
    return score

# helper function ot write the solution list to a txt file
def write_output(filename, solution):
    complete_file_name = filename + ".txt"
    with open(filename, "w+") as f:
        for photo_ids in solution:
            line = " ".join([str(num) for num in photo_ids])
            line += "\n"
            f.write(line)

# approach 1, randomly assign vertical pairing and then optimize/finefune
vertical_nodes = []
horizontal_nodes = []
for i in range(len(storage)):
    photo = storage[i]
    if photo[0] == "V":
        vertical_nodes.append(photo)
    else:
        horizontal_nodes.append(photo)

import random
# randomly shuffle the list 
random.shuffle(vertical_nodes)
print(vertical_nodes)

merged_nodes = [0] * (len(vertical_nodes) // 2)
for i in range(len(merged_nodes)):
    left_vertical_photo = vertical_nodes[2*i]
    right_vertical_photo = vertical_nodes[2*i + 1]
    orientation = "V"
    indexes = left_vertical_photo[2] + right_vertical_photo[2]
    tags = left_vertical_photo[1].union(right_vertical_photo[1])
    merged_nodes[i] = [orientation, tags, indexes]

list_for_tsp = merged_nodes + horizontal_nodes

M = len(list_for_tsp)
print(M)
weights = [ [0]*M for _ in range(M) ]

# set of ints
nodes_used = set()

# list of tuples (start, end)
weights_indexes = []
max_weight = 0
for i in range(M):
    left_node = list_for_tsp[i]
    attributes_left = left_node[1]
    for j in range(i+1, M):
        right_node = list_for_tsp[j]
        attributes_right = right_node[1]
        
        num_intersection = len(attributes_left.intersection(attributes_right))
        num_left = len(attributes_left.difference(attributes_right))
        num_right = len(attributes_right.difference(attributes_left))
        
        weight = min(num_intersection, num_left, num_right)
        weights[i][j] = weight
        
        if weight > 0:
            nodes_used.add(i)
            nodes_used.add(j)
            weights_indexes.append((i, j))
        
        if max_weight < weight:
            max_weight = weight

# Distance callback
def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

  def distance_callback(from_node, to_node):
    return int(dist_matrix[from_node][to_node])

  return distance_callback

max_weight += 1
for i in range(M):
    for j in range(i+1, M):
        weights[i][j] = max_weight - weights[i][j]

dist_matrix = weights
city_names = [node[2] for node in list_for_tsp]

tsp_size = len(city_names)
num_routes = 1
depot = 0
solution_list = []

print("solving now")
  # Create routing model
if tsp_size > 0:
    routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Create the distance callback.
    dist_callback = create_distance_callback(dist_matrix)
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        # Solution distance.
        print("Total distance: " + str(assignment.ObjectiveValue()) + " miles\n")
        # Display the solution.
        # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
        route_number = 0
        index = routing.Start(route_number) # Index of the variable for the starting node.
        route = ''
        while not routing.IsEnd(index):
            # Convert variable indices to node indices in the displayed route.
            route_i = city_names[routing.IndexToNode(index)]
            solution_list.append(route_i)
            route += str(route_i) + ' -> '
            index = assignment.Value(routing.NextVar(index))
        route += str(city_names[routing.IndexToNode(index)])
        print("Route:\n\n" + route)
    else:
        print('No solution found.')
else:
    print('Specify an instance greater than 0.')

print(score(solution_list))

write_output(output_file_name, solution_list)