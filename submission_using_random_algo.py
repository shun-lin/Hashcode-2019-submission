import copy

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
output_file_name = "b_output_random.txt"
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
        f.write(str(len(solution)) + "\n")
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

merged_nodes = [0] * (len(vertical_nodes) // 2)
for i in range(len(merged_nodes)):
    left_vertical_photo = vertical_nodes[2*i]
    right_vertical_photo = vertical_nodes[2*i + 1]
    orientation = "V"
    indexes = left_vertical_photo[2] + right_vertical_photo[2]
    tags = left_vertical_photo[1].union(right_vertical_photo[1])
    merged_nodes[i] = [orientation, tags, indexes]

list_for_tsp = merged_nodes + horizontal_nodes
random.shuffle(list_for_tsp)
solution_list = [item[2] for item in list_for_tsp]
best_list = copy.deepcopy(solution_list)
best_score = score(solution_list)
for i in range(0, 1000):
    random.shuffle(list_for_tsp)
    solution_list = [item[2] for item in list_for_tsp]
    score_i = score(solution_list)
    if (score_i > best_score):
        best_list = copy.deepcopy(solution_list)
        best_score = score_i
        print(best_score)
    if i % 50 == 0:
        write_output(output_file_name, best_list)
write_output(output_file_name, best_list)