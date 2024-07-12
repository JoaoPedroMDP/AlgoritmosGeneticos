#  coding: utf-8
from math import sqrt

from numpy import ndarray
from pygad import GA

from display_data import Point
from ga_caixeiro import POINTS, POINT_COUNT


def calculate_distance_between_points(a: Point, b: Point):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def fit(solution: ndarray, debug=False):
    dist = 0
    for i in range(POINT_COUNT):
        a = POINTS[solution[i]]
        b = POINTS[solution[(i+1) % POINT_COUNT]]
        dist += calculate_distance_between_points(a, b)

    not debug or print(dist)
    return 1 / dist


def fitness_func(ga_instance: GA, solution: ndarray, solution_idx: int):
    return fit(solution)
