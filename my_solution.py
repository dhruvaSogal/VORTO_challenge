import math
import sys
def read_file_to_dict():
    file = sys.argv[1]
    points_list = []
    try:
        with open(file, 'r') as file:
            for line in file:
                pair = line.split()
                num = pair[0]
                pickup = pair[1]
                drop = pair[2]
                coordinates = (pickup,drop)
                points_list.append((num, coordinates))
    except FileNotFoundError:
        print("File not found:", file)
    return points_list


print(read_file_to_dict())
    