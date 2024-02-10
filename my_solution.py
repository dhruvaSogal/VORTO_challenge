import math
import sys

def read_file():
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


def gen_naive_solution(points_list):
    num_drivers = len(points_list)
    solution = []
    for i in range (1, num_drivers):
        list = [int(i)]
        solution.append(list)

    for item in solution:
        print(item)

gen_naive_solution(read_file())  

    