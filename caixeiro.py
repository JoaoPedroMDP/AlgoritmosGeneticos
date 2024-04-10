#  coding: utf-8
from pygad import GA

from display_data import trace_route_between_points
from ga_caixeiro import POINTS
from ga_caixeiro.pygad_config import PYGAD_CONFIG


def main():
    ga_instance = GA(**PYGAD_CONFIG)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return solution, solution_fitness


if __name__ == '__main__':
    avg_sol_fit = 0
    min_sol_fit = 100
    max_sol_fit = -100000
    num_of_executions = 5
    sol_fit = 0
    best_sol = []
    # while sol_fit != 0:
    for i in range(num_of_executions):
        sol, sol_fit = main()
        avg_sol_fit += sol_fit
        if sol_fit < min_sol_fit:
            min_sol_fit = sol_fit
            best_sol = sol
        if sol_fit > max_sol_fit:
            max_sol_fit = sol_fit
        print("Fitness: ", sol_fit)
        solution_point_order = [POINTS[i] for i in sol]
        trace_route_between_points(solution_point_order)

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
    print("Melhor solução: ", best_sol)
    # solution_point_order = [POINTS[i] for i in best_sol]
    # trace_route_between_points(solution_point_order)
