import math
import sys
import random
import copy
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
def getPointFromPointStr(pointStr):
    pointStr = pointStr.replace("(","").replace(")","")
    splits = pointStr.split(",")
    return Point(float(splits[0]), float(splits[1]))

def read_file():
    file = sys.argv[1]
    points_list = []
    header = False
    try:
        with open(file, 'r') as file:
            for line in file:
                if not header:
                    header = True
                    continue
                pair = line.split()
                num = pair[0]
                pickup = getPointFromPointStr(pair[1])
                drop = getPointFromPointStr(pair[2])
                coordinates = (pickup,drop)
                points_list.append((num, coordinates))
    except FileNotFoundError:
        print("File not found:", file)
    return points_list


def gen_naive_solution(points_list):
    num_drivers = len(points_list)
    solution = []
    for i in range (1, num_drivers + 1):
        list = [int(i)]
        solution.append(list)
    return solution

def gen_starting_solution(points_list):
    initial = gen_naive_solution(points_list)
    initial = sorted(initial, key = lambda x: calc_route_cost(points_list, x)) 
    print(initial)

def distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def calc_route_cost(points_list, route):
    total_distance = 0.0
    home = Point(0.0,0.0)
    current_point = home

    for stop in route:
        pickup = points_list[stop - 1][1][0]
        drop = points_list[stop - 1][1][1]
        distance_to_pickup = distance(current_point, pickup)
        distance_for_load = distance(pickup, drop)
        total_distance += distance_to_pickup + distance_for_load
        current_point = drop
    
    total_distance += distance(current_point, home)
    return total_distance

def calc_solution_cost(points_list, solution):
    total_cost = 0.0
    for route in solution:
        total_cost += calc_route_cost(points_list, route)
    total_cost += 500*len(solution)
    return total_cost


def swap_and_shift_elements(points_list, solution):
    # pick a set of two arrays, randomly add one element of one to another
    solution_copy = copy.deepcopy(solution)
    array1, array2 = random.sample(solution_copy, 2)
    pair_to_move = random.choice(array1)
    array2.append(pair_to_move)
    array1.remove(pair_to_move)

    if annealing_constraint(points_list, array2):
        array1.append(pair_to_move)
        array2.remove(pair_to_move)

    solution_copy = [route for route in solution_copy if route]
    return solution_copy

def annealing_constraint(points_list, route):
    if calc_route_cost(points_list, route) <= 720:
        return False
    return True

def simulated_annealing(points_list):
    initial_temp = 200.0
    cooling_rate = 0.01
    num_iter = 30000
    current_state = gen_naive_solution(points_list)
    current_score = calc_solution_cost(points_list, current_state)

    best_state = current_state
    best_score = current_score

    for i in range(num_iter):
        new_state = swap_and_shift_elements(points_list, current_state)
        new_score = calc_solution_cost(points_list, new_state)


        p_acceptance = math.exp((-1 * abs(current_score - new_score)) / initial_temp)
        
        if new_score < current_score or p_acceptance >= random.random():
            current_state = new_state
            current_score = new_score
        if new_score < best_score:
            best_state = new_state
            best_score = new_score
    
        initial_temp *= (1 - cooling_rate)
    for item in best_state:
        print(item)
    return 0
simulated_annealing(read_file())
