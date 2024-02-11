import math
import sys
import random
import copy
from pulp import *
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

def calc_solution_cost(points_list, vars):
    solution = build_solution_from_vars(vars, len(points_list))
    total_cost = 0.0
    for route in solution:
        total_cost += calc_route_cost(points_list, route)
    total_cost += 500*len(solution)
    return total_cost

def build_solution_from_vars(vars, max):
    routes = []
    added = set()
    for n in range(1, max):
        if not (n in added):
            routes.append([n])
            added.add(n)
        for k in range(1, max):
            if k != n:
                if vars.get((n, k), True) and not (k in added):
                    routes[n - 1].append(k)
                    added.add(k)
    return routes    

def linear_programming(points_list):
    prob = LpProblem('VRP', LpMinimize)
    vars = {}
    for n in range(1, len(points_list) + 1):
        for k in range(1, len(points_list) + 1):
            if n != k:
                vars[n,k] = (LpVariable(f"Same_{n}_{k}", cat="Binary"))

    prob += calc_solution_cost(points_list, vars)
    for n in range(1, len(points_list) + 1):
        for k in range(1, len(points_list) + 1):
            if n != k:
                for p in range(1, len(points_list) + 1):
                    if p != n and p != k:
                        prob += vars[n, k] + vars[k, p] - 1 <= vars[n, p]
    prob.solve()
    for var in prob.variables():
        print(var.name, "=", var.varValue)
    
linear_programming(read_file())